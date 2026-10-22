#!/usr/bin/env python3
"""Emit battery pack health (remaining design capacity) for waybar.

The built-in `battery` module reports `{capacity}` (charge left in the pack) and
exposes `{health}` as a raw number, but its `states` are keyed to *capacity* --
so a worn-out pack reporting 24% health would still be painted healthy green.

This module reports the health figure itself with its own state class, so the
bar can colour it by how much of the original capacity is actually left:

    health = charge_full / charge_full_design * 100   (µAh, or µWh fallback)

The worst pack wins, matching waybar's own behaviour for multi-battery systems.
"""
import glob
import json
import os
import sys

POWER_SUPPLY = "/sys/class/power_supply"

HEALTHY = 80.0   # >= 80% of the original design capacity
WORN = 50.0      # >= 50% of the original design capacity

# Material Design Icons: battery_high / battery_medium / battery_low.
ICONS = {
    "good": "\U000f12a3",
    "warning": "\U000f12a2",
    "critical": "\U000f12a1",
    "error": "\U000f0083",
}


def read(path):
    """Read a sysfs file, returning None when it is missing or unreadable."""
    try:
        with open(path) as f:
            return f.read().strip()
    except OSError:
        return None


def packs():
    """Yield (name, full, design, unit, cycles) for every system battery."""
    for d in sorted(glob.glob(os.path.join(POWER_SUPPLY, "*"))):
        if read(os.path.join(d, "type")) != "Battery":
            continue
        full = read(os.path.join(d, "charge_full"))
        design = read(os.path.join(d, "charge_full_design"))
        unit = "\u00b5Ah"
        if full is None or design is None:
            full = read(os.path.join(d, "energy_full"))
            design = read(os.path.join(d, "energy_full_design"))
            unit = "\u00b5Wh"
        if not full or not design:
            continue
        try:
            full, design = float(full), float(design)
        except ValueError:
            continue
        if design <= 0:
            continue
        yield (os.path.basename(d), full, design, unit,
               read(os.path.join(d, "cycle_count")))


def main():
    found = list(packs())
    if not found:
        print(json.dumps({
            "text": ICONS["error"] + " n/a",
            "class": "error",
            "tooltip": "Battery health unavailable",
        }))
        sys.exit(0)

    health = min(full / design * 100 for _, full, design, _, _ in found)

    if health >= HEALTHY:
        cls = "good"
    elif health >= WORN:
        cls = "warning"
    else:
        cls = "critical"

    tooltip = ["Health: {:.1f}% of design capacity".format(health)]
    for name, full, design, unit, cycles in found:
        tooltip.append("{}: {:.0f} / {:.0f} {}".format(name, full, design, unit))
        if cycles:
            tooltip.append("Cycles: {}".format(cycles))

    print(json.dumps({
        "text": "{} {:.0f}%".format(ICONS[cls], health),
        "class": cls,
        "tooltip": "\n".join(tooltip),
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
