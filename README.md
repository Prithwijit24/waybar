<div align="center">

# ⚡ Minimalist Waybar Rice

A sleek, ultra-compact (25px) Waybar configuration designed for **Hyprland** with a Deep Dark Blue palette, neon glow & ambient bloom, soft-pink center clock, value-reactive color indicators, custom GTK3 App Drawer, and instant hardware polling.

[![Waybar](https://img.shields.io/badge/Waybar-0.9+-blue?style=flat-square&logo=wayland&logoColor=white)](https://github.com/Alexays/Waybar)
[![Hyprland](https://img.shields.io/badge/WM-Hyprland-00c8ff?style=flat-square&logo=arch-linux&logoColor=white)](https://hyprland.org/)
[![Theme](https://img.shields.io/badge/Theme-Deep%20Night%20Blue-1f2335?style=flat-square&colorA=050a1f&colorB=5b9dff)](#-palette)
[![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)](LICENSE)

</div>

---

## 📸 Layout Overview

```text
┌── LEFT ──────────────────────────────┬────── CENTER ──────┬────────────────────────────────── RIGHT ──────────────────────────────────┐
│  󰣇  │ 1 2 3 │  code README.md        │   Sat 23 Aug 08:15 │  󰖃 29°C  󰲋 12%  󰻟 40%  󰚥 88%  󰖩 72%  󰔆 60%  󰕾 55%  󰂱 90%  ●   │
└──┴───────────────────────────────────┴────────────────────┴───────────────────────────────────────────────────────────────────────────┘
   │     │        │                         │                  │        │      │      │      │      │      │      │      │
   │     │        └─ Focused Window         └─ Clock/Calendar  │        │      │      │      │      │      │      │      └─ NumLock (LED)
   │     └─ Workspaces                                         │        │      │      │      │      │      │      └─ Bluetooth & Battery
   └─ App Drawer Launcher                                      │        │      │      │      │      │      └─ Volume (PulseAudio)
                                                               │        │      │      │      │      └─ Brightness (Backlight)
                                                               │        │      │      │      └─ Wi-Fi / Ethernet (Network)
                                                               │        │      │      └─ Battery Capacity & State
                                                               │        │      └─ RAM Usage
                                                               │        └─ CPU Usage
                                                               └─ Weather & Notification
```

---

## ✨ Features

- **🚀 Custom GTK3 App Drawer (`scripts/appdrawer.py`):**
  - Grouped & color-coded by package manager source (`[pacman]`, `[yay]`, `[paru]`, `[flatpak]`, `[snap]`).
  - Search filter input with instant live query.
  - Dedicated quick power actions (Reboot, Shutdown, Logout).
- **📊 Value-Reactive Hardware Monitoring:**
  - Dynamic color thresholds for CPU, RAM, and Battery (Normal ➔ Warning ➔ Critical).
  - Smooth blinking CSS animation when battery hits critical level without charging.
  - Responsive subtle hover highlight on right-side modules.
- **🌤 Live Weather & Desktop Notification (`scripts/weather.py`):**
  - Weather fetched and cached from WeatherAPI.
  - Condition-aware styling (Day/Night, Rainy, and Error states).
  - Click to display a formatted rich notification via `notify-send`.
- **⚡ Instant NumLock LED Indicator (`scripts/numlock.py`):**
  - Fast sysfs brightness polling for real-time NumLock LED state without latency.
  - Green (`#8cd867`) active and Red (`#f7768e`) inactive indicators with subtle green background glow when ON.
- **✨ Neon Glow & Ambient Bloom (`style.css`):**
  - Outer bar glow via `window#waybar` — `border-top: 1px solid rgba(91,157,255,0.28)` + layered `box-shadow: 0 -2px 14px rgba(91,157,255,0.32), 0 -4px 32px rgba(91,157,255,0.14)` for upward bloom.
  - Per-module `text-shadow: 0 0 8px currentColor` in matching hue (aqua, terracotta, rose, green, sky, gold, violet, sapphire) + `box-shadow` bloom on `#custom-logo`, `#workspaces button.active`, `#clock`, and tooltip.
  - Center clock uses muted **Soft Pink** (`rgba(232,139,172,0.14)` / `#e8b4c8` / `0 0 10px rgba(232,139,172,0.20)`) for pleasant, non-harsh highlight.
- **🎛 Integrated Controls & Quick Menus:**
  - Left-click on network opens `nmtui` in Kitty.
  - Left-click on bluetooth opens `bluetoothctl` in Kitty.
  - Scroll on volume to adjust levels (±5%), click to toggle mute.
  - Scroll on clock to navigate calendar months.

---

## 🧩 Modules & Interaction Reference

| Zone | Module | Icon & Label | Click Action | Scroll Action | Hover Tooltip |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Left** | `custom/logo` | `󰣇` **App Drawer** | Launch GTK3 App Drawer | — | `"App drawer"` |
| | `hyprland/workspaces` | `1` `2` `3` **Workspaces** | Switch workspace | — | — |
| | `hyprland/window` | `firefox` **Window Title** | — | — | Full window title |
| **Center** | `clock` | `󰃭` `Sat 23 Aug 08:15 PM` | — | Shift month up/down | Calendar view with today highlighted |
| **Right** | `custom/weather` | `󰖃` **29°C Kolkata** | Rich weather notification | — | Detailed weather report |
| | `cpu` | `󰲋` `{usage}%` | — | — | CPU load average & Max frequency |
| | `memory` | `󰻟` `{percent}%` | — | — | Memory used / total in GiB |
| | `battery` | `󰁹` `{capacity}%` | — | — | Time remaining (alternate mode) |
| | `network` | `󰖩` `{signal}%` | Launch `kitty nmtui` | — | SSID, IP/CIDR, Up/Down bandwidth |
| | `backlight` | `󰃠` `{percent}%` | — | Brightness up/down | — |
| | `pulseaudio` | `󰕾` `{volume}%` | Toggle mute | Volume ±5% | — |
| | `bluetooth` | `󰂱` / `󰂲` **Bluetooth** | Launch `kitty bluetoothctl` | — | Connected device details & battery |
| | `custom/numlock` | `●` **NumLock** | — | — | NumLock status (ON / OFF) |

---

## 🎨 Color Palette & Theming

The bar uses a custom **Deep Night Blue** theme with refined Tokyo-Night inspired pastel accents:

| Swatch | Color Name | Hex Code | Purpose / Affected Elements |
| :---: | :--- | :---: | :--- |
| ⬛ | **Extreme Dark Blue** | `#050a1f` | Main Waybar background (`window#waybar`) |
| ⬜ | **Soft Lavender** | `#c0caf5` | Default foreground text and tooltip text |
| 🟦 | **Accent Blue** | `#5b9dff` | Arch logo (`#custom-logo`), Active workspace button, Outer bar glow (`window#waybar`) |
| 🩷 | **Soft Pink** | `#e88bac` / `#e8b4c8` | Clock pill (`#clock`) — `rgba(232,139,172,0.14)` bg, `rgba(232,139,172,0.28)` border, `0 0 10px rgba(232,139,172,0.20)` glow |
| 🩵 | **Soft Aqua / Seafoam** | `#5eead4` | Weather module normal/day state (`#custom-weather`) |
| 🌧️ | **Rain Blue** | `#70c0e8` | Weather rainy state (`#custom-weather.rainy`) |
| 🌙 | **Night Blue** | `#89b4fa` | Weather night state (`#custom-weather.night`) |
| 🟧 | **Warm Terracotta** | `#ea9978` | CPU normal state (`#cpu`) |
| 🌸 | **Dusty Rose** | `#e89bbd` | Memory (RAM) normal state (`#memory`) |
| 🟩 | **Leaf Green** | `#8cd867` | Battery normal state (`#battery`), NumLock active (`#custom-numlock.on`) |
| 🟢 | **Mint Green** | `#6ee7b7` | Battery charging & plugged state (`#battery.charging`, `#battery.plugged`) |
| 🟨 | **Warm Sunbeam / Gold** | `#ffd166` | Backlight (`#backlight`), Battery warning (`#battery.warning`) |
| 🟠 | **Apricot Coral** | `#ff8c5a` | CPU warning (`#cpu.warning`), Memory warning (`#memory.warning`) |
| 🟥 | **Tokyo Red / Crimson** | `#f7768e` | Critical alerts (`#cpu.critical`, `#memory.critical`, `#battery.critical`), Weather error, Urgent workspaces, NumLock inactive (`#custom-numlock.off`) |
| 🌐 | **Ice Sky Blue** | `#60cdff` | Network signal indicator (`#network`) |
| 🟣 | **Lavender-Indigo** | `#a78bfa` | PulseAudio volume level (`#pulseaudio`) |
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

### 3. Change Bar Height or Position
In `config.jsonc` (lines 2–4):
```jsonc
{
    "layer": "bottom",       // "top" or "bottom"
    "position": "bottom",    // "top", "bottom", "left", "right"
    "height": 25             // Height in pixels
}
```

### 4. Customize Colors & Appearance
Edit `style.css`:
- **Bar background & outer glow**: `window#waybar { background-color: #050a1f; border-top: 1px solid rgba(91,157,255,0.28); box-shadow: 0 -2px 14px rgba(91,157,255,0.32), 0 -4px 32px rgba(91,157,255,0.14); }` — lower alphas for subtler bloom, raise for stronger neon.
- **Clock highlight (Soft Pink)**: `#clock { background-color: rgba(232,139,172,0.14); color: #e8b4c8; border: 1px solid rgba(232,139,172,0.28); box-shadow: 0 0 10px rgba(232,139,172,0.20); text-shadow: 0 0 8px rgba(232,139,172,0.42); }` — was solid `#5b9dff`; increase `0.14 → 0.20` for brighter pill.
- **Module glow**: Each right-module has `text-shadow: 0 0 8px <matching-color>` (e.g. `#cpu: rgba(234,153,120,0.6)`) — adjust blur `8px → 12px` for stronger neon or remove for flat look. Active workspace (`#workspaces button.active`) and logo (`#custom-logo`) use layered `box-shadow` bloom.
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
    ├── 🐍 numlock.py          # Real-time /sys/class/leds NumLock state emitter
    └── 🐍 weather.py          # WeatherAPI parser with tooltip & notification payload
```

---

## 🛠 Developer Notes & Insights

> [!TIP]
> **Waybar Custom Exec Execution Model:**
> Waybar's `custom/exec` modules update when the executed script **exits** (it does not stream persistent stdout). Scripts like `numlock.py` poll quickly for a small interval, output JSON, and exit immediately so Waybar re-runs them cleanly at the specified interval.

> [!NOTE]
> **Sysfs & Inotify:**
> The Linux kernel does not emit standard `inotify` events for changes in `/sys/class/leds/*`. Fast micro-polling (e.g. `0.2s`) is the standard, reliable method to capture LED toggle events instantaneously.

---

## 📜 License

Distributed under the MIT License. Feel free to fork, customize, and adapt for your own desktop rice!
