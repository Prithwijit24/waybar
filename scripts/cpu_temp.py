#!/usr/bin/env python3
"""Emit the average CPU temperature for waybar.

Waybar's built-in `temperature` module reads a single sensor file, so it can
only ever report one reading (e.g. "Package id 0"). This module averages the
CPU's *per-core* sensors and emits its own state class, so the bar can colour
the reading by how hot the CPU actually is.

A note on which sensors to average: Intel's "Package id 0" (and the
`x86_pkg_temp` thermal zone) are *aggregates* -- they track the hottest core
rather than being a peer reading of one. Averaging them alongside the per-core
sensors double-weights the peak and pushes the number above what every other
monitoring tool reports (btop, `sensors`, `mission-center` all show per-core
values). So the per-core sensors are preferred, and the package aggregate is
only used when a CPU exposes nothing else.

Intel CPUs expose `coretemp`, AMD CPUs `k10temp`/`zenpower`. When no driver is
present the script falls back to the matching CPU thermal zone.
"""
import glob
import json
import os
import sys

HWMON = "/sys/class/hwmon"
THERMAL = "/sys/class/thermal"

# hwmon drivers that expose CPU package/core temperatures.
CPU_DRIVERS = ("coretemp", "k10temp", "zenpower", "cpu_thermal", "cpuss")

# thermal zone types that describe the CPU package.
CPU_ZONES = ("x86_pkg_temp", "TCPU", "cpu-thermal", "soc_thermal")

# Sensor labels that are aggregates of the whole package rather than a single
# core. These are excluded from the average when peer readings exist.
AGGREGATES = ("package id", "x86_pkg_temp", "tcpu", "cpu-thermal", "soc_thermal")

WARM = 70.0    # >= 70C -> warning
HOT = 85.0     # >= 85C -> critical

# Material Design Icons: thermometer / thermometer_high.
ICONS = {
    "normal": "\U000f050f",
    "warning": "\U000f10c2",
    "critical": "\U000f10c2",
    "error": "\U000f050f",
}


def read(path):
    """Read a sysfs file, returning None when it is missing or unreadable."""
    try:
        with open(path) as f:
            return f.read().strip()
    except OSError:
        return None


def is_aggregate(label):
    """True for package-wide readings that track the hottest core."""
    low = label.lower()
    return any(low.startswith(a) for a in AGGREGATES)


def _collect(paths, kind_of, label_of):
    """(driver, label, millidegrees) for every readable sensor in paths."""
    found = []
    for path in paths:
        raw = read(path)
        if not raw:
            continue
        try:
            milli = float(raw)
        except ValueError:
            continue
        found.append((kind_of(path), label_of(path), milli))
    return found


def hwmon_sensors():
    """Every CPU temperature sensor exposed by the kernel's hwmon driver."""
    out = []
    for d in sorted(glob.glob(os.path.join(HWMON, "hwmon*"))):
        driver = read(os.path.join(d, "name"))
        if driver not in CPU_DRIVERS:
            continue
        paths = sorted(glob.glob(os.path.join(d, "temp*_input")))

        def label_of(path):
            explicit = read(path[: -len("_input")] + "_label")
            return explicit or os.path.basename(path)[: -len("_input")]

        out += _collect(paths, lambda _p, _d=driver: _d, label_of)
    return out


def thermal_sensors():
    """CPU thermal zones, used when no hwmon driver is present."""
    paths, kinds = [], {}
    for z in sorted(glob.glob(os.path.join(THERMAL, "thermal_zone*"))):
        ztype = read(os.path.join(z, "type"))
        if ztype not in CPU_ZONES:
            continue
        path = os.path.join(z, "temp")
        paths.append(path)
        kinds[path] = ztype
    return _collect(paths, lambda p: kinds.get(p, "cpu"), lambda p: kinds.get(p, "cpu"))


def pick(sensors):
    """Split sensors into (averaged, aggregates) -- peers win over aggregates."""
    peers = [s for s in sensors if not is_aggregate(s[1])]
    aggregates = [s for s in sensors if is_aggregate(s[1])]
    if peers:
        return peers, aggregates
    for pref in ("x86_pkg_temp", "tcpu", "cpu-thermal", "soc_thermal"):
        for s in sensors:
            if s[1].lower() == pref:
                return [s], [a for a in aggregates if a is not s]
    return sensors, []


def main():
    sensors = hwmon_sensors() or thermal_sensors()
    if not sensors:
        print(json.dumps({
            "text": ICONS["error"] + " n/a",
            "class": "error",
            "tooltip": "CPU temperature unavailable",
        }))
        sys.exit(0)

    used, aggregates = pick(sensors)
    avg = sum(milli / 1000.0 for _, _, milli in used) / len(used)

    if avg >= HOT:
        cls = "critical"
    elif avg >= WARM:
        cls = "warning"
    else:
        cls = "normal"

    tooltip = ["Average CPU temperature: {:.1f}°C".format(avg)]
    for driver, label, milli in used:
        tooltip.append("{} {}: {:.1f}°C".format(driver, label, milli / 1000))
    for driver, label, milli in aggregates:
        tooltip.append("{} {} (peak): {:.1f}°C".format(driver, label, milli / 1000))

    print(json.dumps({
        "text": "{} {:.0f}°C".format(ICONS[cls], avg),
        "class": cls,
        "tooltip": "\n".join(tooltip),
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
