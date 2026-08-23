# Waybar — Prithwijit's Rice

A compact (25px) Hyprland status bar with a dark-blue theme, value-reactive icons,
a clickable app drawer, and a live NumLock indicator.

```
┌─ left ───────────────┬──── center ────┬────────────────────────── right ──────────────────────────┐
│ 󰣇 | 1 2 3 | firefox │    Sat 23 Aug │  󰖃 29°C  󰲋 12%  󰻟 40%  󰚥 88%  󰖩 72%  󰔆 60%  󰕾 55%  󰂱  ●  │
└──────────────────────┴────────────────┴───────────────────────────────────────────────────────────┘
   logo  ws  window          clock          weather cpu ram bat net lite vol  bt   numlk
```

---

## Layout (where things live)

| Zone | Modules | What it shows |
|------|---------|---------------|
| **Left** | `custom/logo` · `hyprland/workspaces` · `hyprland/window` | App-launcher button, workspace IDs, focused window title |
| **Center** | `clock` | Date + time (scroll to change month) |
| **Right** | `custom/weather` · `cpu` · `memory` · `battery` · `network` · `backlight` · `pulseaudio` · `bluetooth` · `custom/numlock` | System stats, ordered left→right |

Reorder anything by editing `modules-left` / `modules-center` / `modules-right`
in `config.jsonc` (line 7–9).

---

## Module Legend — what each icon means

| Icon | Module | Meaning | Color states |
|------|--------|---------|--------------|
| 󰣇 | `custom/logo` | Click → app drawer | 🔵 `#5b9dff` |
| `1 2 3` | `hyprland/workspaces` | Workspace switcher (click to activate) | active 🔵, urgent 🔴 `#ff5470` |
| `firefox` | `hyprland/window` | Title of the focused window | ⚪ `#9aa5ce` |
| 🕐 | `clock` | Date + time, calendar on hover | box 🔵 `#5b9dff` |
| 🌡 | `custom/weather` | Temp + city (Kolkata), click for full report | 🟢 `#2dd4bf` |
| 󰲋 | `cpu` | CPU usage % (scroll/click for load) | 🟠 normal `#ffa726` · 🟠 warn · 🔴 crit `#ff5470` |
| 󰻟 (fa-memory) | `memory` | RAM usage % | 🩷 `#ff5cf0` · 🔴 warn/crit |
| 󰚥 / 󰁹 | `battery` | Capacity + icon; charging shows 󰂄 / plugged 󰚥 | 🟢 `#4ade80` · 🟢 charging `#2dd4bf` · 🟠 warn · 🔴 crit (blinks) |
| 󰖩 / 󰖮 | `network` | Wi-Fi signal % or ethernet; click → `nmtui` | 🔵 `#22d3ee` · 🔴 disconnected |
| 󰔆 | `backlight` | Screen brightness % (scroll to change) | 🟡 `#facc15` |
| 󰕾 / 󰖁 | `pulseaudio` | Volume %; BT headset 󰥰; muted 󰖁; click → mute | 🟣 `#b388ff` · 🔴 muted |
| 󰂱 / 󰂲 | `bluetooth` | On/connected 󰂱 · off 󰂲; click → `bluetoothctl` | 🔵 on · ⚪ off `#565f89` · ⬛ disabled `#3b4261` |
| ● | `custom/numlock` | NumLock state | 🟢 on `#4ade80` · 🔴 off `#ff5470` |

---

## How to change things (quick reference)

### 🎨 Bar background & global look
`style.css` → `window#waybar` (line 8):
```css
window#waybar { background-color: #050a1f; color: #c0caf5; padding: 0 8px; }
```
- `#050a1f` = extreme dark blue · change to taste (e.g. `#0a1124` lighter, `#03060f` near-black).
- Bar **height** is set in `config.jsonc` `"height": 25` (line 4).

### 🔤 Change an icon
Icons are **Nerd Font** glyphs. Edit the `format` / `format-icons` field for the
module in `config.jsonc`. Example — battery icons (line 85):
```jsonc
"format-icons": ["󰁺","󰁼","󰁾","󰂀","󰂂","󰁹"]
```
Find glyphs with `nerd-fonts` picker or `gucharmap` (search "battery").

### 🌈 Change a module's color
In `style.css`, target the module id (e.g. `#cpu`, `#custom-weather`). To add a
state (warning/critical), add a `.warning` / `.critical` rule like `cpu` does
(lines 106–116).

### 🔢 Change thresholds (warn/crit)
In `config.jsonc`, each module has a `states` block:
```jsonc
"cpu": { "states": { "normal": 40, "warning": 70, "critical": 90 } }
```

### ⏱ Change update frequency
Set `"interval"` (seconds; **floats work**, e.g. `0.2`). Higher = less CPU.
- `cpu`/`memory`: `2` · `weather`: `1800` (30 min) · `numlock`: `0.2`.

### ➕ Add a new module
1. Append its name to the right `modules-*` array in `config.jsonc`.
2. Add a config block (see any existing block) — built-in (e.g. `"disk"`)
   or `custom/x` with an `exec`.
3. (Optional) add styling in `style.css` under `#custom-x`.

### 🧩 Custom scripts (see [Scripts](#scripts))
`custom/*` modules run a command and print either plain text or JSON
(`return-type: "json"` → `{"text": "...", "class": "...", "tooltip": "..."}`).

---

## Theme palette

| Role | Color | Hex |
|------|-------|-----|
| Bar background | 🔵 extreme dark blue | `#050a1f` |
| Default text | ⚪ soft lavender | `#c0caf5` |
| Accent / logo / clock / active ws / BT-on | 🔵 blue | `#5b9dff` |
| Weather | 🟢 teal | `#2dd4bf` |
| CPU | 🟠 orange | `#ffa726` |
| Memory | 🩷 magenta | `#ff5cf0` |
| Battery / NumLock-on | 🟢 green | `#4ade80` |
| Network | 🔵 cyan | `#22d3ee` |
| Backlight | 🟡 yellow | `#facc15` |
| Pulseaudio | 🟣 purple | `#b388ff` |
| Danger / muted / critical / urgent | 🔴 red | `#ff5470` |

---

## Scripts (`scripts/`)

| File | Role | Notes |
|------|------|-------|
| `numlock.py` | Prints NumLock state as a colored ●, then **exits** | Polls `/sys/class/leds/*numlock/brightness`; re-run by waybar every `0.2s` |
| `weather.py` | Fetches weather, caches to `cache/weather.json` | Exits after one print (waybar re-runs every 1800s) |
| `appdrawer.py` | GTK3 app launcher window | Groups apps by source (pacman/yay/snap/flatpak…), power buttons pinned bottom-right |
| `gen_applist.sh` | Builds `~/.cache/waybar/appdrawer.{list,map}` | Classifies installed apps; run by `appdrawer.py` on open |
| `launch_drawer.sh` | Detached launcher for the drawer | `setsid` + Wayland backend, logs to `/tmp/drawer.log` |

The app drawer opens from the 󰣇 logo (left). Apps are colored per source:
pacman 🔵 `#7dcfff`, yay 🟡 `#ffc777`, paru 🟣 `#bb9af7`, flatpak 🟢 `#9ece6a`,
snap 🟢 `#73daca`. Power buttons: 󰍣 reboot · 󰐥 shutdown · 󰗽 logout.

---

## Developer gotchas (learned the hard way)

- **⚠️ waybar only displays a `custom/exec` module when the process *exits*.**
  It does **not** stream a long-running command. So `numlock.py` must print once
  and `sys.exit(0)`; updates come from waybar re-running it at `interval`.
  (This is why a persistent poll left the indicator blank.)
- **📛 `inotify` does not fire on sysfs.** Watching
  `/sys/class/leds/*numlock/brightness` with `inotify` never emits events, so the
  script must *poll* (every ~0.1–0.25s) instead of blocking on a watch.
- **🔣 JSON `\u` escapes are exactly 4 hex digits.** A 5-digit codepoint
  (e.g. many Nerd Font glyphs) written as `\u1F#####` corrupts the JSON — insert
  the literal glyph character instead, or use a 4-digit Private-Use codepoint
  like `\uefc5` (fa-memory).

---

## Reloading

waybar auto-reloads CSS on change (`reload_style_on_change: true`). For config
changes, restart it:
```bash
pkill -x waybar; sleep 1; waybar > /tmp/waybar.log 2>&1 &
# or just log out / reload your Hyprland config
```
Check `/tmp/waybar.log` for errors.

---

## Files

```
config.jsonc   ← module layout, icons, thresholds, intervals
style.css      ← colors, spacing, bars, animations
scripts/       ← custom module logic + app drawer
cache/         ← weather cache
```
