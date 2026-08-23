#!/usr/bin/env python3
"""Emit NumLock state as a colored circle, then exit.

waybar's exec module only displays output when the process exits (it does not
stream a long-running command), so we poll the LED briefly, print the current
state on change or timeout, then exit. waybar re-runs us at `interval`, giving
near-instant updates.
"""
import os
import glob
import sys
import time


def state():
    on = False
    for f in glob.glob("/sys/class/leds/*numlock/brightness"):
        try:
            if open(f).read().strip() == "1":
                on = True
        except OSError:
            pass
    if on:
        return '{"text":"\\u25cf","class":"on","tooltip":"NumLock: ON"}'
    return '{"text":"\\u25cf","class":"off","tooltip":"NumLock: OFF"}'


last = state()
deadline = time.time() + 0.25
while time.time() < deadline:
    cur = state()
    if cur != last:
        print(cur, flush=True)
        sys.exit(0)
    time.sleep(0.05)

print(last, flush=True)
sys.exit(0)
