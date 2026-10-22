<div align="center">

# ⚡ Minimalist Waybar Rice

A sleek, ultra-compact Waybar configuration (26px min-height) designed for **Hyprland** with a Deep Dark Blue palette, neon glow & ambient bloom, split center cluster (backlight · date · bold yellow time · volume), a left vitals cluster (battery % · SSD free %), value-reactive color indicators, custom GTK3 App Drawer, and instant hardware polling.

[![Waybar](https://img.shields.io/badge/Waybar-0.9+-blue?style=flat-square&logo=wayland&logoColor=white)](https://github.com/Alexays/Waybar)
[![Hyprland](https://img.shields.io/badge/WM-Hyprland-00c8ff?style=flat-square&logo=arch-linux&logoColor=white)](https://hyprland.org/)
[![Theme](https://img.shields.io/badge/Theme-Deep%20Night%20Blue-1f2335?style=flat-square&colorA=050a1f&colorB=5b9dff)](#-palette)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## 📸 Layout Overview

> Synced with `config.jsonc:7-9` — `modules-left` / `modules-center` / `modules-right`.

```text
┌── LEFT ──────────────────────┬─── CENTER ────────────────────────────────────────┬─── RIGHT ─────────────────────────────────────────────────────────┐
│ 󰡗 │ 󱊡 24% │ 󰔏 63°C │ 󰋊 27% 63G │ 1 2 3 │ code README.md │ 󰏠 60% │ Sat 23 Aug │ 08:15 PM │ 󰅟 55% │ 󰆃 29°C │ RAM 40% │ CPU 12% │ 88% 󰂀 │ 󰆩 72% │ 󰢱 │ ● │
└───┴───────┴────────┴───────────┴───────┴────────────────┴───────┴────────────┴──────────┴───────┴────────┴─────────┴─────────┴───────┴───────┴───┴───┘
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   │
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ NumLock LED (custom/numlock)
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ Bluetooth (bluetooth)
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ Wi-Fi / Ethernet (network)
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ Battery Capacity & State (battery)
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ CPU Usage (cpu)
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ Memory / RAM (memory)
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ Weather & Notification (custom/weather)
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ Volume Level & Mute (pulseaudio)
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ Time Bold Yellow (#clock.time)
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ Date & Calendar (#clock.date)
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ Brightness Control (backlight)
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ Focused Window Title (hyprland/window)
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ Workspaces (hyprland/workspaces)
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ SSD Free Space (disk) - free % + free GB
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ Average CPU Temperature (custom/cpu-temp)
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ Battery Health (custom/battery-health)
    │   │       │        │           │       │                │       │            │          │       │        │         │         │       │       │   │   └─ App Drawer Launcher (custom/logo)
```

**Zone mapping (as configured):**
- **Left:** `custom/logo` → `custom/battery-health` → `custom/cpu-temp` → `disk` → `hyprland/workspaces` → `hyprland/window`
- **Center:** `backlight` → `clock#date` → `clock#time` → `pulseaudio`
- **Right:** `custom/weather` → `memory` → `cpu` → `battery` → `network` → `bluetooth` → `custom/numlock`

---

## ✨ Features

- **🚀 Custom GTK3 App Drawer (`scripts/appdrawer.py`):**
  - Grouped & color-coded by package manager source (`[pacman]`, `[yay]`, `[paru]`, `[flatpak]`, `[snap]`).
  - Search filter input with instant live query.
  - Dedicated quick power actions (Reboot, Shutdown, Logout).
- **📊 Value-Reactive Hardware Monitoring & Clean Text Layout:**
  - Explicit and legible format for `CPU {usage}%` and `RAM {}%` with optimal module spacing.
  - Dynamic color thresholds for CPU, RAM, and Battery (Normal ➔ Warning ➔ Critical).
  - Smooth blinking CSS animation when battery hits critical level without charging.
  - Responsive subtle hover highlight on interactive modules.
- **💾 Left Vitals Cluster (battery health + disk):**
  - Two compact chips sitting between the app-drawer logo and the workspace list.
  - `custom/battery-health` (`scripts/battery_health.py`) — **pack health**: how much of the
    *original design capacity* is still there (`charge_full / charge_full_design`). Currently
    **24%** on this machine, i.e. the pack holds a quarter of its rated capacity.
  - `custom/cpu-temp` (`scripts/cpu_temp.py`) — **average CPU temperature** across the CPU's
    per-core sensors, e.g. `󱃂 55°C`. Waybar's own `temperature` module can only ever read a
    single sensor file, so it cannot average.
  - The package aggregate (`Package id 0` / `x86_pkg_temp`) is deliberately **excluded** from
    the average: on Intel it tracks the *hottest* core rather than being a peer reading, so
    including it double-weights the peak and pushes the number above what btop, `sensors` and
    every other monitoring tool show. It is still listed in the tooltip as `(peak)`.
  - `disk` — SSD free space as free % + free GB (`󰊊 27% 63G`) from the native Waybar `disk` module on `/` (NVMe).
  - The right-hand `battery` module keeps its own job: **charge remaining** (`88% 󰂀`).
  - Shared chip shell (subtle translucent fill + 1px inner border) so the pair reads as one unit next to the logo.
  - Health colour and glyph both track the value: green `󱊣` (≥80%) ➔ gold `󱊢` (≥50%) ➔
    crimson `󱊡` (<50%), so a worn pack can never be mistaken for a healthy one.
  - Disk colour escalates with utilisation: teal ➔ gold (`warning`) ➔ apricot (`critical`) ➔ crimson (`full`).
  - Click the disk chip to open `df -h /` in Kitty.
- **🌤 Live Weather & Desktop Notification (`scripts/weather.py`):**
  - Weather fetched and cached from WeatherAPI.
  - Condition-aware styling (Day/Night, Rainy, and Error states).
  - Click to display a formatted rich notification via `notify-send`.
- **⚡ Instant NumLock LED Indicator (`scripts/numlock.py`):**
  - Fast sysfs brightness polling for real-time NumLock LED state without latency.
  - Green (`#8cd867`) active and Red (`#f7768e`) inactive indicators with subtle green background glow when ON.
- **✨ Neon Glow & Ambient Bloom (`style.css`):**
  - Outer bar glow via `window#waybar` — `border-top: 1px solid rgba(91,157,255,0.28)` + layered `box-shadow: 0 -2px 14px rgba(91,157,255,0.32), 0 -4px 32px rgba(91,157,255,0.14)` for upward bloom.
  - Per-module `text-shadow: 0 0 8px currentColor` in matching hue (aqua, terracotta, rose, green, sky, gold, violet, sapphire) + `box-shadow` bloom on `#custom-logo`, `#workspaces button.active`, and tooltip.
  - Symmetrical center cluster: **Backlight** (soft gold) and **PulseAudio** (violet) frame the split clock.
  - Split center clock: **Date** (`#clock.date`) in muted lavender `#a9b1d6` (flat with calendar tooltip), **Time** (`#clock.time`) in vivid bold yellow (`#ffeb3b`, `font-weight: 800`, borderless transparent styling with glowing `text-shadow: 0 0 8px rgba(255,235,59,0.5)`).
- **🎛 Integrated Controls & Quick Menus:**
  - Left-click on network opens `nmtui` in Kitty.
  - Left-click on bluetooth opens `bluetoothctl` in Kitty.
  - Scroll on volume to adjust levels (±5%), click to toggle mute via `pactl`.
  - Scroll on date or time to navigate calendar months.
  - Left-click on weather triggers rich `notify-send` popup.

---

## 🧩 Modules & Interaction Reference

| Zone | Module | Icon & Label | Click Action | Scroll Action | Hover Tooltip |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Left** | `custom/logo` | `󰣇` **App Drawer** | Launch GTK3 App Drawer (`scripts/launch_drawer.sh`) | — | `App drawer` |
| | `custom/battery-health` | `󱊡` `{health}%` **Battery Health** | — | — | `Health: 24.2% of design capacity` + actual/design charge + cycles |
| | `custom/cpu-temp` | `󱃂` `{avg}°C` **CPU Temp** | — | — | Average of the per-core sensors + the package peak |
| | `disk` | `󰊊` `{percentage_free}% {specific_free}G` **SSD Free** | Open `df -h /` in Kitty | — | Free/total, free % and used % |
| | `hyprland/workspaces` | `1` `2` `3` **Workspaces** | Switch workspace (`activate`) | — | — |
| | `hyprland/window` | **Window Title** (max 45 chars) | — | — | Full window title |
| **Center** | `backlight` | `󰃠` `{percent}%` (icons `󰃚`–`󰃠`) | — | — | — (`tooltip: false`) |
| | `clock#date` | `Sat 23 Aug` (`{:%a %d %b}`) | — | Shift calendar month up/down | Calendar (`<tt><big>{calendar}</big></tt>`, today `#f7768e`) |
| | `clock#time` | `08:15 PM` (`{:%I:%M %p}`, 1s) | — | Shift calendar month up/down | — |
| | `pulseaudio` | `󰕾` `{volume}%` / `󰖁` muted | Toggle mute (`pactl`) | Volume ±5% | — (`tooltip: false`) |
| **Right** | `custom/weather` | `{text}` (e.g. `29°C Kolkata` / `🌧 29°C Kolkata`) | Rich `notify-send` weather popup | — | Detailed weather report (`tooltip: true`) |
| | `memory` | `RAM {percent}%` | — | — | `used {used} GiB / {total} GiB` |
| | `cpu` | `CPU {usage}%` | — | — | `load: {load}` / `freq (max): {max_frequency} GHz` |
| | `battery` | `{capacity}% {icon}` (`󰁺`–`󰁹`) | — | — | Time remaining (`format-alt: {time} {icon}`) |
| | `network` | `󰖩`/`` `{signal}%` / `{ifname}` / `off` | Launch `kitty nmtui` | — | SSID/IP/CIDR + `↓{bandwidthDownBytes} ↑{bandwidthUpBytes}` |
| | `bluetooth` | `󰂯` on / `󰂲` off/disabled / `󰂱` connected | Launch `kitty bluetoothctl` | — | Controller + `num_connections` / `{device_enumerate}` |
| | `custom/numlock` | `●` **NumLock** | — | — | `ON` / `OFF` (polled `0.2s` via `scripts/numlock.py`) |

---

## 🎨 Color Palette & Theming

The bar uses a custom **Deep Night Blue** theme with refined Tokyo-Night inspired pastel accents:

| Swatch | Color Name | Hex Code | Purpose / Affected Elements |
| :---: | :--- | :---: | :--- |
| ⬛ | **Extreme Dark Blue** | `#050a1f` | Main Waybar background (`window#waybar`) |
| ⬜ | **Soft Lavender** | `#c0caf5` | Default foreground text and tooltip text |
| 🟦 | **Accent Blue** | `#5b9dff` | Arch logo (`#custom-logo`), Active workspace button, Outer bar glow (`window#waybar`) |
| 🪻 | **Muted Lavender** | `#a9b1d6` | Date text (`#clock.date`) in center cluster |
| 💛 | **Vivid Yellow** | `#ffeb3b` | Time text (`#clock.time`) — bold 800, transparent bg, text-shadow `0 0 8px rgba(255,235,59,0.5)` glow |
| 🩵 | **Soft Aqua / Seafoam** | `#5eead4` | Weather module normal/day state (`#custom-weather`) |
| 🟢 | **Mint Teal** | `#73daca` | SSD free-space indicator (`#disk`) in the left vitals cluster |
| 🌧️ | **Rain Blue** | `#70c0e8` | Weather rainy state (`#custom-weather.rainy`) |
| 🌙 | **Night Blue** | `#89b4fa` | Weather night state (`#custom-weather.night`) |
| 🟧 | **Warm Terracotta** | `#ea9978` | CPU usage normal state (`#cpu`), CPU temperature normal state (`#custom-cpu-temp.normal`) |
| 🌸 | **Dusty Rose** | `#e89bbd` | Memory (RAM) normal state (`#memory`) |
| 🟩 | **Leaf Green** | `#8cd867` | Battery normal state (`#battery`), Battery health OK (`#custom-battery-health.good`), NumLock active (`#custom-numlock.on`) |
| 🟢 | **Mint Green** | `#6ee7b7` | Battery charging & plugged state (`#battery.charging`, `#battery.plugged`) |
| 🟨 | **Warm Sunbeam / Gold** | `#ffd166` | Center Backlight (`#backlight`), Battery warning (`#battery.warning`), Battery health worn (`#custom-battery-health.warning`), Disk warning (`#disk.warning`) |
| 🟠 | **Apricot Coral** | `#ff8c5a` | CPU warning (`#cpu.warning`), Memory warning (`#memory.warning`), Disk critical (`#disk.critical`) |
| 🟥 | **Tokyo Red / Crimson** | `#f7768e` | Critical alerts (`#cpu.critical`, `#memory.critical`, `#battery.critical`), Weather error, Urgent workspaces, NumLock inactive (`#custom-numlock.off`), Disk full (`#disk.full`), Battery health worn out (`#custom-battery-health.critical`) |
| 🌐 | **Ice Sky Blue** | `#60cdff` | Network signal indicator (`#network`) |
| 🟣 | **Lavender-Indigo** | `#a78bfa` | Center PulseAudio volume level (`#pulseaudio`) |
| 🔵 | **Periwinkle / Sapphire** | `#7287fd` | Bluetooth active / connected (`#bluetooth`) |
| 🔘 | **Muted Slate** | `#565f89` | Inactive workspaces, Muted audio, Offline network, Bluetooth off |
| ⬛ | **Deep Indigo** | `#3b4261` | Bluetooth disabled state (`#bluetooth.disabled`) |

---

## 📦 Prerequisites & Dependencies

To ensure all custom scripts and interactive modules function properly, install the following packages:

```bash
# Core Waybar & System Tools (Arch / Hyprland)
sudo pacman -S waybar hyprland kitty pulseaudio-utils networkmanager bluez-utils jq libnotify

# Python & GTK3 (for App Drawer, Weather & NumLock)
sudo pacman -S python python-requests python-gobject gtk3

# Fonts (Required for glyphs and icons)
sudo pacman -S ttf-nerd-fonts-symbols noto-fonts noto-fonts-cjk
# (Optional fallback: ttf-font-awesome, ttf-jetbrains-mono-nerd)
```

---

## 🚀 Installation & Setup

1. **Clone or Copy** this repository into your user config folder:
   ```bash
   git clone <repo-url> ~/.config/waybar
   # or copy into ~/.config/waybar
   ```

2. **Make Scripts Executable**:
   ```bash
   chmod +x ~/.config/waybar/scripts/*.sh ~/.config/waybar/scripts/*.py
   ```

3. **Verify Script Paths**:
   Ensure `config.jsonc` paths point to your home directory:
   ```bash
   # Check path references in config.jsonc
   sed -i "s|/home/prithwijit|$HOME|g" ~/.config/waybar/config.jsonc
   sed -i "s|/home/prithwijit|$HOME|g" ~/.config/waybar/scripts/launch_drawer.sh
   ```

4. **Launch or Reload Waybar**:
   ```bash
   pkill -x waybar; waybar > /tmp/waybar.log 2>&1 &
   ```

---

## ⚙️ Customization Guide

### 1. Change Weather Location or API Key
Open `scripts/weather.py` and modify lines 9–12:
```python
URL = (
    "http://api.weatherapi.com/v1/current.json"
    "?key=YOUR_API_KEY&q=your_city&aqi=yes"
)
```

### 2. Adjust Module Thresholds (Warning / Critical)
In `config.jsonc`, adjust the threshold percentage for CPU, RAM, or Battery:
```jsonc
"cpu": {
    "states": {
        "normal": 40,
        "warning": 70,
        "critical": 90
    }
},
"memory": {
    "states": {
        "normal": 40,
        "warning": 65,
        "critical": 85
    }
}
```

The disk indicator uses **utilisation** thresholds (percentage *used*), so its
colours escalate as the SSD fills up:
```jsonc
"disk": {
    "path": "/",
    "unit": "GiB",
    "format": "󰋊 {percentage_free}% {specific_free:.0f}G",
    "states": {
        "warning": 85,
        "critical": 90,
        "full": 95
    }
}
```
> [!NOTE]
> `disk` is a native Waybar module (v0.15+). Point `path` at any mount to track a
> different filesystem, e.g. `"/home/prithwijit/HDD"` for the secondary SATA disk.
> Available placeholders: `{percentage_free}`, `{percentage_used}`, `{free}`,
> `{used}`, `{total}`, `{path}`, `{specific_free}`, `{specific_used}`,
> `{specific_total}`.

The battery health indicator uses its own thresholds in
`scripts/battery_health.py`:
```python
HEALTHY = 80.0   # >= 80% of the original design capacity -> good  (green)
WORN = 50.0      # >= 50% of the original design capacity -> warning (gold)
```
Below `WORN` the pack is flagged `critical` (crimson). Raise `HEALTHY` if you
consider a pack worn earlier, and refresh faster by lowering `interval` in the
`custom/battery-health` block of `config.jsonc` (default: 60s).

The CPU temperature indicator uses its own thresholds in `scripts/cpu_temp.py`:
```python
WARM = 70.0    # >= 70C -> warning (apricot)
HOT = 85.0     # >= 85C -> critical (crimson)
```
Both scripts accept any driver the kernel exposes — `coretemp` (Intel),
`k10temp`/`zenpower` (AMD) — and fall back to the CPU thermal zone
(`x86_pkg_temp`, `TCPU`) when no hwmon driver is present.

The temperature chip polls every 5s (the `interval` in the `custom/cpu-temp`
block). Raise it if you want a lower wake-up rate; lower it towards 1s to
track a live `btop` reading as closely as possible.

### 3. Change Bar Height or Position
In `config.jsonc` (lines 2–4):
```jsonc
{
    "layer": "bottom",       // "top" or "bottom"
    "position": "bottom",    // "top", "bottom", "left", "right"
    "height": 25             // Configured bar height in pixels
}
```
And in `style.css` (lines 8–12):
```css
window#waybar {
    background-color: #050a1f;
    color: #c0caf5;
    padding: 0 8px;
    min-height: 26px;        /* Minimum height styling */
}
```

### 4. Customize Colors & Appearance
Edit `style.css`:
- **Bar background & outer glow**: `window#waybar { background-color: #050a1f; border-top: 1px solid rgba(91,157,255,0.28); box-shadow: 0 -2px 14px rgba(91,157,255,0.32), 0 -4px 32px rgba(91,157,255,0.14); }` — lower alphas for subtler bloom, raise for stronger neon.
- **Center cluster & clock highlight**:
  - `#clock.date`: `color: #a9b1d6; font-weight: 600; padding: 0 6px;` (flat muted lavender date).
  - `#clock.time`: `color: #ffeb3b; font-weight: 800; padding: 0 6px; text-shadow: 0 0 8px rgba(255,235,59,0.5);` (vivid bold yellow neon text, clean borderless styling with transparent background).
  - `#backlight`: `color: #ffd166; text-shadow: 0 0 8px rgba(255,209,102,0.6);` (soft gold glow).
  - `#pulseaudio`: `color: #a78bfa; text-shadow: 0 0 8px rgba(167,139,250,0.6);` (violet glow).
- **Module glow**: Each module has `text-shadow: 0 0 8px <matching-color>` (e.g. `#cpu: rgba(234,153,120,0.6)`) — adjust blur `8px → 12px` for stronger neon or remove for flat look. Active workspace (`#workspaces button.active`) and logo (`#custom-logo`) use layered `box-shadow` bloom.
- **Hover effects**: Configured under `#custom-weather:hover, #cpu:hover, ... { background-color: rgba(255, 255, 255, 0.06); box-shadow: 0 0 10px rgba(255,255,255,0.08); }`.
- **Module colors & state classes**: Individual module and sub-state selectors (`#custom-weather.rainy`, `#custom-weather.night`, `#battery.warning`, `#custom-numlock.on`, etc.).

---

## 📂 File Architecture

```text
~/.config/waybar/
├── 📄 config.jsonc            # Module selection, layouts, actions, and intervals
├── 🎨 style.css               # Tokyo-night dark blue theme, neon glow/bloom, CSS transitions & animations
├── 📁 cache/
│   └── 📄 weather.json        # Cached response for weather module
└── 📁 scripts/
    ├── 🐍 appdrawer.py        # GTK3 app launcher with package manager categorization
    ├── 📜 gen_applist.sh      # Scans .desktop files and classifies source (pacman/AUR/flatpak/snap)
    ├── 📜 launch_drawer.sh    # Background detached launcher for app drawer
    ├── 🐍 battery_health.py   # Pack health (charge_full / charge_full_design) emitter
    ├── 🐍 cpu_temp.py         # Average CPU temperature (package + per-core sensors) emitter
    ├── 🐍 numlock.py          # Real-time /sys/class/leds NumLock state emitter
    └── 🐍 weather.py          # WeatherAPI parser with tooltip & notification payload
```

---

## 🛠 Developer Notes & Insights

> [!TIP]
> **Waybar Custom Exec Execution Model:**
> Waybar's `custom/exec` modules update when the executed script **exits** (it does not stream persistent stdout). Scripts like `numlock.py` poll quickly for a small interval, output JSON, and exit immediately so Waybar re-runs them cleanly at the specified interval.

> [!TIP]
> **Native Waybar Modules over Custom Scripts:**
> The disk chip uses Waybar's built-in `disk` module — no script needed. Waybar
> splits a module name on `#` to allow multiple instances of the same type —
> the part after `#` becomes an extra CSS class, so `clock#date` is styled with
> `#clock.date`. The same trick would give you `battery#left` for a second
> battery readout.
>
> [!NOTE]
> **Why CPU temperature needs a script:**
> Waybar's `temperature` module reads a single sensor file, so it reports one
> reading (usually `Package id 0`) and cannot average. `scripts/cpu_temp.py`
> averages the per-core sensors and emits its own state class so the bar can
> colour the reading by how hot the CPU is.
>
> [!TIP]
> **Pick the right sensors to average:**
> Intel's `coretemp` exposes `Package id 0` alongside `Core 0`, `Core 1`, ....
> The package sensor is an *aggregate* that tracks the hottest core — on an
> i3-1115G4 it measured `>= max(core)` in 25 out of 25 samples. Averaging it in
> alongside the cores therefore counts the peak twice: it inflated the reading
> by ~1°C on average (up to 1.8°C) and made the bar disagree with btop, which
> shows per-core values only. The script prefers the peer (per-core) sensors
> and falls back to the aggregate only when a CPU exposes nothing else.
>
> [!NOTE]
> **Why battery health needs a script:**
> The built-in `battery` module does expose `{health}` (= `charge_full /
> charge_full_design`), but its `states` are keyed to *capacity*, not health.
> A pack at 24% health but 80% charged would therefore be painted healthy
> green. `scripts/battery_health.py` emits the health figure with its own
> state class so the bar can colour it by how worn the pack actually is.

> [!NOTE]
> **Sysfs & Inotify:**
> The Linux kernel does not emit standard `inotify` events for changes in `/sys/class/leds/*`. Fast micro-polling (e.g. `0.2s`) is the standard, reliable method to capture LED toggle events instantaneously.

---

## 📜 License

Distributed under the MIT License. Feel free to fork, customize, and adapt for your own desktop rice!
