#!/usr/bin/env bash
# Generate the grouped app list + action map used by the drawer.
# Groups are detected dynamically: official repos = pacman, foreign packages
# get the name of the installed AUR helper (yay/paru/...), plus flatpak/snap
# when those desktop files are present.
set -uo pipefail

CACHE_DIR="$HOME/.cache/waybar"
LIST="$CACHE_DIR/appdrawer.list"
MAP="$CACHE_DIR/appdrawer.map"
mkdir -p "$CACHE_DIR"

# Detect which AUR helper to tag foreign packages with.
AUR_HELPER=""
for h in yay paru aura trizen pikaur; do
    if command -v "$h" >/dev/null 2>&1; then AUR_HELPER="$h"; break; fi
done
[ -z "$AUR_HELPER" ] && AUR_HELPER="aur"

pacman -Qnq 2>/dev/null > "$CACHE_DIR/_qn"
pacman -Qmq 2>/dev/null > "$CACHE_DIR/_qm"

: > "$LIST"
: > "$MAP"

classify() {
    local d="$1" pkg group
    case "$d" in
        */flatpak/*exports/*) group="flatpak" ;;
        */snapd/*)            group="snap" ;;
        *)
            pkg=$(pacman -Qoq "$d" 2>/dev/null || true)
            if grep -qxF "$pkg" "$CACHE_DIR/_qm" 2>/dev/null; then
                group="$AUR_HELPER"
            else
                group="pacman"
            fi
            ;;
    esac
    echo "$group"
}

for d in \
    /usr/share/applications/*.desktop \
    "$HOME"/.local/share/applications/*.desktop \
    /var/lib/flatpak/exports/share/applications/*.desktop \
    "$HOME"/.local/share/flatpak/exports/share/applications/*.desktop \
    /var/lib/snapd/desktop/applications/*.desktop
do
    [ -f "$d" ] || continue
    grep -q '^NoDisplay=true' "$d" && continue
    grep -q '^Terminal=true' "$d" && continue
    name=$(grep -m1 '^Name=' "$d" | cut -d= -f2-)
    [ -z "$name" ] && continue
    group=$(classify "$d")
    id=$(basename "$d" .desktop)
    disp="[$group] $name"
    echo "$disp" >> "$LIST"
    echo -e "$disp\tapp:$id" >> "$MAP"
done

sort -uo "$LIST" "$LIST"

{
    echo -e " Reboot\tpower:reboot"
    echo -e " Shutdown\tpower:shutdown"
    echo -e " Logout\tpower:logout"
} >> "$LIST"
{
    echo -e " Reboot\tpower:reboot"
    echo -e " Shutdown\tpower:shutdown"
    echo -e " Logout\tpower:logout"
} >> "$MAP"

rm -f "$CACHE_DIR/_qn" "$CACHE_DIR/_qm"
