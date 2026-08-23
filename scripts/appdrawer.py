#!/usr/bin/env python3
"""GTK3 app drawer launched from the waybar Arch logo.

- Scrollable, filterable list of GUI apps grouped by source package manager
  ([pacman] = official repos, [yay] = AUR/foreign).
- A fixed horizontal bar of power icons (Reboot / Shutdown / Logout) pinned to
  the bottom-right, outside the scrolling queue.
"""
import os
import time
import subprocess
import traceback

os.environ.setdefault("GDK_BACKEND", "wayland")

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

LOG = "/tmp/drawer.log"


def log(msg):
    try:
        with open(LOG, "a") as f:
            f.write(msg + "\n")
    except OSError:
        pass

HOME = os.path.expanduser("~")
CACHE = os.path.join(HOME, ".cache/waybar")
LIST = os.path.join(CACHE, "appdrawer.list")
MAP = os.path.join(CACHE, "appdrawer.map")
GEN = os.path.join(HOME, ".config/waybar", "scripts", "gen_applist.sh")

CSS = """
* {
    background-color: transparent;
    background-image: none;
    border: none;
    box-shadow: none;
}
window {
    background-color: #1a1b26;
    border: 2px solid #7aa2f7;
    border-radius: 14px;
    color: #c0caf5;
    font-family: "JetBrainsMono Nerd Font", "Noto Sans", "Font Awesome 7 Free", sans-serif;
}
entry {
    border-bottom: 1px solid rgba(122, 162, 247, 0.4);
    color: #c0caf5;
    padding: 9px 4px;
    caret-color: #7aa2f7;
}
entry selection { color: #7aa2f7; }
row { padding: 9px 14px; border-radius: 9px; }
row label { color: #c0caf5; }
row:selected { background-color: rgba(122, 162, 247, 0.22); }
row:selected label { color: #ffffff; font-weight: 700; }
button {
    padding: 10px 16px;
    color: #c0caf5;
    font-weight: 700;
}
button:hover { color: #ffffff; }
.power-reboot { color: #7aa2f7; }
.power-shutdown { color: #f7768e; }
.power-logout { color: #e0af68; }
.power-reboot:hover { color: #9ec1ff; }
.power-shutdown:hover { color: #ff9aa9; }
.power-logout:hover { color: #f3c98a; }
"""


def ensure_gen():
    try:
        age = time.time() - os.path.getmtime(LIST)
    except OSError:
        age = 1e9
    if age > 600:
        subprocess.run(["bash", GEN], check=False)


def load_entries():
    apps, power = [], []
    try:
        with open(MAP, encoding="utf-8") as f:
            for line in f:
                line = line.rstrip("\n")
                if not line or "\t" not in line:
                    continue
                disp, action = line.split("\t", 1)
                (power if action.startswith("power:") else apps).append((disp, action))
    except OSError:
        pass
    return apps, power


class Drawer(Gtk.Window):
    def __init__(self, apps, power):
        super().__init__(title="Apps")
        self.apps = apps
        self.set_decorated(False)
        self.set_skip_taskbar_hint(True)
        self.set_keep_above(True)
        self.set_position(Gtk.WindowPosition.CENTER)
        self.set_default_size(460, 640)

        provider = Gtk.CssProvider()
        provider.load_from_data(CSS.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        groups = {disp.split("]", 1)[0].lstrip("[") for disp, _ in self.apps}
        gcss = "\n".join(
            ".g-%s { color: %s; }" % (g, self.color_for(g)) for g in groups
        )
        gprov = Gtk.CssProvider()
        gprov.load_from_data(gcss.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(), gprov, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        vbox.set_margin_top(10)
        vbox.set_margin_bottom(10)
        vbox.set_margin_start(10)
        vbox.set_margin_end(10)

        self.search = Gtk.SearchEntry()
        self.search.set_placeholder_text("Search applications…")
        self.search.connect("search-changed", self.on_search)
        vbox.pack_start(self.search, False, False, 0)

        self.store = Gtk.ListBox()
        self.store.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.store.set_activate_on_single_click(True)
        self.store.connect("row-activated", self.on_activate)
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.store)
        vbox.pack_start(scrolled, True, True, 0)

        pbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        pbox.set_halign(Gtk.Align.END)
        pbox.set_margin_top(6)
        for disp, action in power:
            pbox.pack_end(self.make_power_btn(disp, action), False, False, 0)
        vbox.pack_end(pbox, False, False, 0)

        self.add(vbox)

        for disp, action in apps:
            self.store.add(self.make_app_row(disp, action))

        self.connect("key-press-event", self.on_key)
        self.search.grab_focus()
        self.show_all()

    def make_app_row(self, disp, action):
        row = Gtk.ListBoxRow()
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        label = Gtk.Label(label=disp)
        label.set_xalign(0.0)
        group = disp.split("]", 1)[0].lstrip("[")
        label.get_style_context().add_class("g-" + group)
        box.pack_start(label, True, True, 0)
        row.add(box)
        row.disp = disp
        row.action = action
        return row

    @staticmethod
    def color_for(group):
        colors = {
            "pacman": "#7dcfff",
            "yay": "#ffc777",
            "paru": "#bb9af7",
            "aura": "#f7768e",
            "trizen": "#9ece6a",
            "pikaur": "#73daca",
            "aur": "#ff9e64",
            "flatpak": "#9ece6a",
            "snap": "#73daca",
        }
        if group in colors:
            return colors[group]
        fallback = ["#7dcfff", "#ffc777", "#bb9af7", "#9ece6a",
                    "#73daca", "#ff9e64", "#f7768e", "#e0af68"]
        return fallback[sum(ord(c) for c in group) % len(fallback)]

    def make_power_btn(self, disp, action):
        kind = action.split(":", 1)[1]
        glyph = {"reboot": "󰍣", "shutdown": "󰐥", "logout": "󰗽"}.get(kind, "")
        name = {"reboot": "Reboot", "shutdown": "Shutdown", "logout": "Logout"}.get(kind, disp.strip())
        btn = Gtk.Button(label=(glyph + " " + name).strip())
        btn.get_style_context().add_class("power-" + kind)
        btn.connect("clicked", lambda *_: self.do_power(action))
        return btn

    def on_search(self, entry):
        text = entry.get_text().lower()
        self.store.set_filter_func(
            lambda row, t: t in row.disp.lower(), text
        )

    def on_activate(self, _listbox, row):
        self.launch(row.action)

    def on_key(self, _w, event):
        if event.keyval == Gdk.KEY_Escape:
            self.destroy()

    def do_power(self, action):
        kind = action.split(":", 1)[1]
        cmds = {
            "reboot": ["systemctl", "reboot"],
            "shutdown": ["systemctl", "poweroff"],
            "logout": ["hyprctl", "dispatch", "exit"],
        }.get(kind)
        if cmds:
            subprocess.Popen(cmds)
        self.destroy()

    def launch(self, action):
        if action.startswith("app:"):
            subprocess.Popen(["/usr/sbin/gtk-launch", action[4:]])
        self.destroy()


def main():
    log("drawer: starting (WAYLAND_DISPLAY=%s, DISPLAY=%s)"
        % (os.environ.get("WAYLAND_DISPLAY"), os.environ.get("DISPLAY")))
    ensure_gen()
    apps, power = load_entries()
    log("drawer: %d apps, %d power entries loaded" % (len(apps), len(power)))
    Drawer(apps, power)
    Gtk.main()
    log("drawer: exited cleanly")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        log("drawer: FATAL\n" + traceback.format_exc())
        raise
