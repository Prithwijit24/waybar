#!/usr/bin/env bash
# Detached launcher for the GTK app drawer, so it survives waybar and logs errors.
export GDK_BACKEND=wayland
cd "$HOME"
setsid /usr/bin/python3 /home/prithwijit/.config/waybar/scripts/appdrawer.py \
    >> /tmp/drawer.log 2>&1 < /dev/null &
