#!/usr/bin/env python3
"""
VDE Windows 11 Fluent Taskbar (Windhawk Acrylic Styler Edition)
Native Sub-15MB RAM • 1-to-1 Windows 11 Centered Dock & Control Center
Zero External Dependencies • Universal Wayland Layer-Shell & X11 Dock Support
"""

import os
import sys
import time
import subprocess
import shutil
import glob
from datetime import datetime

try:
    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    from gi.repository import Gtk, Gdk, GLib, Gio
    HAS_GTK = True
    try:
        gi.require_version('GtkLayerShell', '0.1')
        from gi.repository import GtkLayerShell
        HAS_LAYER_SHELL = True
    except Exception:
        HAS_LAYER_SHELL = False
except Exception:
    HAS_GTK = False
    HAS_LAYER_SHELL = False

PID_FILE = os.path.expanduser("~/.cache/vde-taskbar.pid")
TASKBAR_HEIGHT = 48

CSS = b"""
* {
    font-family: 'Segoe UI Variable Text', 'Inter', 'Cantarell', -apple-system, sans-serif;
    color: #f4f4f5;
    -gtk-icon-style: regular;
}

window.vde-taskbar {
    background-color: rgba(18, 18, 22, 0.88);
    border-top: 1px solid rgba(255, 255, 255, 0.12);
}

.taskbar-container {
    min-height: 48px;
    padding: 0 4px;
}

/* ------------------------------------------------------------- */
/* Brand Pill & Action Buttons                                   */
/* ------------------------------------------------------------- */
.vde-pill-btn {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 3px 12px;
    margin: 8px 4px;
    transition: all 0.2s ease;
}

.vde-pill-btn:hover {
    background: rgba(56, 189, 248, 0.12);
    border-color: rgba(56, 189, 248, 0.35);
}

.vde-pill-label {
    font-size: 11px;
    font-weight: 700;
    color: #38bdf8;
    letter-spacing: 1.2px;
}

.icon-btn {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 4px 6px;
    margin: 4px 1px;
    transition: all 0.15s ease;
}

.icon-btn:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.12);
}

.icon-btn:active {
    background: rgba(255, 255, 255, 0.05);
}

/* ------------------------------------------------------------- */
/* Centered App Launchers & Windhawk Indicators                  */
/* ------------------------------------------------------------- */
.start-btn {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 4px 10px;
    margin: 3px 2px;
    transition: all 0.2s ease;
}

.start-btn:hover {
    background: rgba(56, 189, 248, 0.15);
    border-color: rgba(56, 189, 248, 0.30);
    box-shadow: 0 0 12px rgba(56, 189, 248, 0.25);
}

.start-btn:active {
    background: rgba(56, 189, 248, 0.25);
}

.task-item-btn {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 3px 8px 1px 8px;
    margin: 2px 1px;
    transition: all 0.15s ease;
}

.task-item-btn:hover {
    background: rgba(255, 255, 255, 0.09);
    border-color: rgba(255, 255, 255, 0.12);
}

.task-item-btn:active {
    background: rgba(255, 255, 255, 0.05);
}

/* Windhawk Active Indicator Pill */
.indicator-pill {
    min-height: 3px;
    max-height: 3px;
    border-radius: 2px;
    margin-top: 1px;
}

.indicator-pill.running {
    min-width: 16px;
    background-color: #38bdf8;
    box-shadow: 0 0 6px rgba(56, 189, 248, 0.5);
}

.indicator-pill.idle {
    min-width: 0px;
    background-color: transparent;
}

/* ------------------------------------------------------------- */
/* Right Zone: System Tray, Quick Settings Pill & Clock          */
/* ------------------------------------------------------------- */
.qs-pill {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 4px 8px;
    margin: 4px 2px;
    transition: all 0.15s ease;
}

.qs-pill:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.12);
}

.clock-btn {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 2px 8px;
    margin: 3px 2px;
    transition: all 0.15s ease;
}

.clock-btn:hover {
    background: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.12);
}

.clock-time {
    font-size: 11px;
    font-weight: 600;
    color: #fafafa;
}

.clock-date {
    font-size: 10px;
    color: #a1a1aa;
}

.show-desktop-strip {
    min-width: 4px;
    max-width: 4px;
    margin: 6px 1px 6px 4px;
    background: rgba(255, 255, 255, 0.15);
    border-radius: 2px;
    border: none;
    transition: all 0.2s ease;
}

.show-desktop-strip:hover {
    background: #38bdf8;
    box-shadow: 0 0 8px rgba(56, 189, 248, 0.6);
}
"""

PINNED_APPS = [
    {
        "id": "terminal",
        "name": "Crossminal (Terminal)",
        "icon": "utilities-terminal",
        "fallback_icon": "terminal",
        "cmd": "/usr/local/bin/crossminal",
        "proc_pattern": "crossminal"
    },
    {
        "id": "files",
        "name": "Crossmanager (Files)",
        "icon": "system-file-manager",
        "fallback_icon": "folder",
        "cmd": "/usr/local/bin/crossmanager",
        "proc_pattern": "crossmanager"
    },
    {
        "id": "pad",
        "name": "Crosspad (Notepad)",
        "icon": "accessories-text-editor",
        "fallback_icon": "text-editor",
        "cmd": "/usr/local/bin/crosspad",
        "proc_pattern": "crosspad"
    },
    {
        "id": "settings",
        "name": "Crossings (Settings)",
        "icon": "preferences-system",
        "fallback_icon": "settings",
        "cmd": "/usr/local/bin/crossings",
        "proc_pattern": "crossings"
    },
    {
        "id": "paint",
        "name": "Crossaint (Paint)",
        "icon": "applications-graphics",
        "fallback_icon": "paint",
        "cmd": "/usr/local/bin/crossaint",
        "proc_pattern": "crossaint"
    },
    {
        "id": "calc",
        "name": "Crossculator (Calculator)",
        "icon": "accessories-calculator",
        "fallback_icon": "calc",
        "cmd": "/usr/local/bin/crossculator",
        "proc_pattern": "crossculator"
    },
    {
        "id": "snip",
        "name": "Crossnip (Snipping Tool)",
        "icon": "applets-screenshooter",
        "fallback_icon": "screenshot",
        "cmd": "/usr/local/bin/crossnip",
        "proc_pattern": "crossnip"
    }
]

class VDETaskbarWindow(Gtk.Window):
    def __init__(self):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.set_title("vde-bar")
        self.set_role("taskbar")
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)
        self.get_style_context().add_class("vde-taskbar")

        self.assets_dir = "/usr/share/vde/assets"
        if not os.path.isdir(self.assets_dir):
            local_assets = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
            if os.path.isdir(local_assets):
                self.assets_dir = local_assets

        # Setup Layer-Shell (Wayland) or Dock Strut (X11)
        self.init_window_dock()

        # Build Main UI Box
        main_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        main_box.get_style_context().add_class("taskbar-container")
        self.add(main_box)

        # 1. Left Zone: Brand Pill & Workspace
        left_box = self.build_left_zone()
        main_box.pack_start(left_box, False, False, 0)

        # 2. Center Dock: Start + Pinned Apps
        center_box = self.build_center_dock()
        main_box.set_center_widget(center_box)

        # 3. Right Zone: System Tray, Quick Settings Pill, Clock, Show Desktop
        right_box = self.build_right_zone()
        main_box.pack_end(right_box, False, False, 0)

        # Periodic Timers
        GLib.timeout_add_seconds(1, self.update_clock)
        GLib.timeout_add_seconds(3, self.update_system_status)
        GLib.timeout_add_seconds(2, self.update_running_indicators)

        # Initial updates
        self.update_clock()
        self.update_system_status()
        self.update_running_indicators()

    def init_window_dock(self):
        if HAS_LAYER_SHELL:
            try:
                GtkLayerShell.init_for_window(self)
                GtkLayerShell.set_layer(self, GtkLayerShell.Layer.TOP)
                GtkLayerShell.auto_exclusive_zone_enable(self)
                GtkLayerShell.set_keyboard_mode(self, GtkLayerShell.KeyboardMode.NONE)
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.BOTTOM, True)
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.LEFT, True)
                GtkLayerShell.set_anchor(self, GtkLayerShell.Edge.RIGHT, True)
                return
            except Exception as e:
                print(f"[VDETaskbar] LayerShell init fallback: {e}")

        # Fallback to standard X11 / Wayland Dock hint
        self.set_type_hint(Gdk.WindowTypeHint.DOCK)
        self.reposition_dock()

        screen = Gdk.Screen.get_default()
        if screen:
            screen.connect("monitors-changed", lambda s: self.reposition_dock())
            screen.connect("size-changed", lambda s: self.reposition_dock())

    def reposition_dock(self):
        screen = Gdk.Screen.get_default()
        if screen:
            geom = screen.get_monitor_geometry(screen.get_primary_monitor())
            self.set_size_request(geom.width, TASKBAR_HEIGHT)
            self.resize(geom.width, TASKBAR_HEIGHT)
            self.move(geom.x, geom.y + geom.height - TASKBAR_HEIGHT)

    def get_asset_icon(self, icon_name, fallback_name=None, pixel_size=20):
        # 1. Check local assets/icons
        candidates = [
            os.path.join(self.assets_dir, "icons", f"{icon_name}.svg"),
            os.path.join(self.assets_dir, "icons", f"{icon_name}-dark.svg"),
            os.path.join(self.assets_dir, "icons", "glm", f"{icon_name}.svg"),
        ]
        if fallback_name:
            candidates.append(os.path.join(self.assets_dir, "icons", f"{fallback_name}.svg"))
            candidates.append(os.path.join(self.assets_dir, "icons", f"{fallback_name}-dark.svg"))

        for path in candidates:
            if os.path.exists(path):
                img = Gtk.Image.new_from_file(path)
                img.set_pixel_size(pixel_size)
                return img

        # 2. GTK System Icon Theme
        theme = Gtk.IconTheme.get_default()
        if theme.has_icon(icon_name):
            img = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.LARGE_TOOLBAR)
            img.set_pixel_size(pixel_size)
            return img

        if fallback_name and theme.has_icon(fallback_name):
            img = Gtk.Image.new_from_icon_name(fallback_name, Gtk.IconSize.LARGE_TOOLBAR)
            img.set_pixel_size(pixel_size)
            return img

        # 3. Generic fallback
        img = Gtk.Image.new_from_icon_name("application-x-executable", Gtk.IconSize.LARGE_TOOLBAR)
        img.set_pixel_size(pixel_size)
        return img

    def build_left_zone(self):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=4)
        box.set_valign(Gtk.Align.CENTER)

        # Brand Pill
        pill_btn = Gtk.Button()
        pill_btn.get_style_context().add_class("vde-pill-btn")
        pill_lbl = Gtk.Label(label="❖ VDE")
        pill_lbl.get_style_context().add_class("vde-pill-label")
        pill_btn.add(pill_lbl)
        pill_btn.set_tooltip_text("Victorious Desktop Environment")
        pill_btn.connect("clicked", lambda b: self.spawn_cmd("/usr/local/bin/vde-launcher"))
        box.pack_start(pill_btn, False, False, 0)

        # Task View / Switcher Icon
        task_view_btn = Gtk.Button()
        task_view_btn.get_style_context().add_class("icon-btn")
        tv_img = self.get_asset_icon("all-apps", "view-grid", 18)
        task_view_btn.add(tv_img)
        task_view_btn.set_tooltip_text("Task View (Alt+Tab)")
        task_view_btn.connect("clicked", lambda b: self.trigger_task_view())
        box.pack_start(task_view_btn, False, False, 0)

        return box

    def build_center_dock(self):
        dock = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=3)
        dock.set_valign(Gtk.Align.CENTER)

        # 1. Start Button (Windows 11 Logo)
        start_btn = Gtk.Button()
        start_btn.get_style_context().add_class("start-btn")
        start_img = self.get_asset_icon("vde", "start-here", 22)
        start_btn.add(start_img)
        start_btn.set_tooltip_text("Start Menu (Win Key)")
        start_btn.connect("clicked", lambda b: self.spawn_cmd("/usr/local/bin/vde-launcher"))
        dock.pack_start(start_btn, False, False, 0)

        # 2. Search Button
        search_btn = Gtk.Button()
        search_btn.get_style_context().add_class("start-btn")
        search_img = self.get_asset_icon("search", "system-search", 18)
        search_btn.add(search_img)
        search_btn.set_tooltip_text("Search (Win+S)")
        search_btn.connect("clicked", lambda b: self.spawn_cmd("/usr/local/bin/vde-launcher"))
        dock.pack_start(search_btn, False, False, 0)

        # 3. Pinned App Launchers with Indicator Pills
        self.app_indicators = {}
        for app in PINNED_APPS:
            app_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            app_box.set_valign(Gtk.Align.CENTER)

            btn = Gtk.Button()
            btn.get_style_context().add_class("task-item-btn")
            btn.set_tooltip_text(app["name"])

            icon = self.get_asset_icon(app["icon"], app.get("fallback_icon"), 22)
            btn_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
            btn_box.pack_start(icon, False, False, 0)

            # Indicator line underneath
            indicator = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            indicator.get_style_context().add_class("indicator-pill")
            indicator.get_style_context().add_class("idle")
            indicator.set_halign(Gtk.Align.CENTER)
            btn_box.pack_start(indicator, False, False, 0)

            btn.add(btn_box)
            cmd = app["cmd"]
            btn.connect("clicked", lambda b, c=cmd: self.spawn_cmd(c))

            dock.pack_start(btn, False, False, 0)
            self.app_indicators[app["id"]] = (indicator, app["proc_pattern"])

        return dock

    def build_right_zone(self):
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=2)
        box.set_valign(Gtk.Align.CENTER)

        # Tray Chevron ^
        tray_btn = Gtk.Button()
        tray_btn.get_style_context().add_class("icon-btn")
        chevron = Gtk.Label(label="^")
        chevron.get_style_context().add_class("vde-pill-label")
        tray_btn.add(chevron)
        tray_btn.set_tooltip_text("System Tray Overflow")
        tray_btn.connect("clicked", lambda b: self.spawn_cmd("/usr/local/bin/vde-quicksettings"))
        box.pack_start(tray_btn, False, False, 0)

        # Quick Settings Combined Pill (Network + Volume + Battery)
        qs_btn = Gtk.Button()
        qs_btn.get_style_context().add_class("qs-pill")
        qs_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)

        self.net_icon = Gtk.Label(label="🌐")
        self.vol_icon = Gtk.Label(label="🔊")
        self.bat_icon = Gtk.Label(label="🔋")

        qs_box.pack_start(self.net_icon, False, False, 0)
        qs_box.pack_start(self.vol_icon, False, False, 0)
        qs_box.pack_start(self.bat_icon, False, False, 0)
        qs_btn.add(qs_box)
        qs_btn.set_tooltip_text("Quick Settings & Network (Win+A)")
        qs_btn.connect("clicked", lambda b: self.spawn_cmd("/usr/local/bin/vde-quicksettings"))
        box.pack_start(qs_btn, False, False, 0)

        # Clock Widget (Two-Line: Time / Date)
        clock_btn = Gtk.Button()
        clock_btn.get_style_context().add_class("clock-btn")
        clock_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        clock_box.set_valign(Gtk.Align.CENTER)

        self.time_lbl = Gtk.Label(label="12:00 PM")
        self.time_lbl.get_style_context().add_class("clock-time")
        self.time_lbl.set_xalign(1.0)

        self.date_lbl = Gtk.Label(label="1/1/2026")
        self.date_lbl.get_style_context().add_class("clock-date")
        self.date_lbl.set_xalign(1.0)

        clock_box.pack_start(self.time_lbl, False, False, 0)
        clock_box.pack_start(self.date_lbl, False, False, 0)
        clock_btn.add(clock_box)
        clock_btn.set_tooltip_text("Notification & Calendar Center (Win+N)")
        clock_btn.connect("clicked", lambda b: self.spawn_cmd("/usr/local/bin/vde-quicksettings"))
        box.pack_start(clock_btn, False, False, 0)

        # Show Desktop Strip (Extreme Right Edge)
        peek_btn = Gtk.Button()
        peek_btn.get_style_context().add_class("show-desktop-strip")
        peek_btn.set_tooltip_text("Show Desktop")
        peek_btn.connect("clicked", lambda b: self.toggle_show_desktop())
        box.pack_start(peek_btn, False, False, 0)

        return box

    def update_clock(self):
        now = datetime.now()
        self.time_lbl.set_text(now.strftime("%I:%M %p").lstrip("0"))
        self.date_lbl.set_text(now.strftime("%m/%d/%Y"))
        return True

    def update_system_status(self):
        # 1. Network Status Check (Carrier on eth/wlan)
        online = False
        try:
            for iface in os.listdir("/sys/class/net"):
                if iface.startswith("lo"):
                    continue
                carrier_file = f"/sys/class/net/{iface}/carrier"
                if os.path.exists(carrier_file):
                    with open(carrier_file, "r") as f:
                        if f.read().strip() == "1":
                            online = True
                            break
        except Exception:
            online = True

        self.net_icon.set_text("🌐" if online else "⚠")

        # 2. Volume Check
        try:
            vol_out = subprocess.check_output(["pactl", "get-sink-volume", "@DEFAULT_SINK@"], stderr=subprocess.DEVNULL).decode()
            if "/" in vol_out:
                pct = int(vol_out.split("/")[1].strip().replace("%", ""))
                self.vol_icon.set_text("🔇" if pct == 0 else "🔊")
        except Exception:
            self.vol_icon.set_text("🔊")

        # 3. Battery Check
        bat_dirs = glob.glob("/sys/class/power_supply/BAT*")
        if bat_dirs:
            self.bat_icon.set_visible(True)
            try:
                cap_file = os.path.join(bat_dirs[0], "capacity")
                if os.path.exists(cap_file):
                    with open(cap_file, "r") as f:
                        cap = int(f.read().strip())
                        self.bat_icon.set_text("🪫" if cap < 20 else "🔋")
            except Exception:
                self.bat_icon.set_text("🔋")
        else:
            self.bat_icon.set_visible(False)

        return True

    def update_running_indicators(self):
        # Scan active process names to toggle the Windhawk indicator pill
        try:
            active_pids = subprocess.check_output(["pgrep", "-a", "python3"], stderr=subprocess.DEVNULL).decode()
        except Exception:
            active_pids = ""

        for app_id, (indicator, pattern) in self.app_indicators.items():
            is_running = pattern in active_pids
            ctx = indicator.get_style_context()
            if is_running:
                ctx.remove_class("idle")
                ctx.add_class("running")
            else:
                ctx.remove_class("running")
                ctx.add_class("idle")

        return True

    def spawn_cmd(self, cmd):
        try:
            parts = cmd.split()
            subprocess.Popen(parts, start_new_session=True)
        except Exception as e:
            print(f"[VDETaskbar Error] Failed to launch {cmd}: {e}")

    def trigger_task_view(self):
        if shutil.which("wlrctl"):
            subprocess.Popen(["wlrctl", "keyboard", "type", "Tab"], start_new_session=True)
        elif shutil.which("xdotool"):
            subprocess.Popen(["xdotool", "key", "alt+Tab"], start_new_session=True)

    def toggle_show_desktop(self):
        if shutil.which("wlrctl"):
            subprocess.Popen(["wlrctl", "toplevel", "minimize"], start_new_session=True)
        elif shutil.which("xdotool"):
            subprocess.Popen(["xdotool", "key", "super+d"], start_new_session=True)

def main():
    if not HAS_GTK:
        print("[VDETaskbar Error] PyGObject (Gtk 3) required.")
        sys.exit(1)

    # Single-instance check
    os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                old_pid = int(f.read().strip())
            # Check if still running
            os.kill(old_pid, 0)
            print("[VDETaskbar] Already running.")
            sys.exit(0)
        except ProcessLookupError:
            pass
        except Exception:
            pass

    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    # Apply Fluent CSS
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(CSS)
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    GLib.set_prgname("vde-bar")
    GLib.set_application_name("VDE Taskbar")

    win = VDETaskbarWindow()
    win.show_all()

    try:
        Gtk.main()
    finally:
        try:
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)
        except Exception:
            pass

if __name__ == "__main__":
    main()
