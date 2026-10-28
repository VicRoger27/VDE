#!/usr/bin/env python3
"""
VDE Windows 11 Start Menu (Windhawk Acrylic Styler Edition)
Native Fluent Dark Mica Application Launcher & Action Center
Zero Telemetry • Sub-15MB RAM • 1-to-1 Windows 11 Layout
"""

import os
import sys
import subprocess
import pwd
import getpass

try:
    import gi
    gi.require_version('Gtk', '3.0')
    gi.require_version('Gdk', '3.0')
    from gi.repository import Gtk, Gdk, GLib, Gio
    HAS_GTK = True
except Exception:
    HAS_GTK = False

# Lock file for single-instance toggle
PID_FILE = os.path.expanduser("~/.cache/vde-startmenu.pid")

CSS = b"""
* {
    font-family: 'Segoe UI Variable Text', 'Inter', 'Cantarell', sans-serif;
    color: #f4f4f5;
}

window.start-menu {
    background-color: rgba(28, 28, 34, 0.92);
    border: 1px solid rgba(255, 255, 255, 0.14);
    border-radius: 14px;
    box-shadow: 0 16px 40px rgba(0, 0, 0, 0.65);
}

.search-box {
    background-color: rgba(0, 0, 0, 0.35);
    border: 1px solid rgba(255, 255, 255, 0.10);
    border-bottom: 2px solid #38bdf8;
    border-radius: 8px;
    padding: 8px 14px;
    font-size: 13px;
    color: #ffffff;
    transition: all 0.2s ease;
}

.search-box:focus {
    background-color: rgba(0, 0, 0, 0.5);
    border-color: #38bdf8;
    box-shadow: 0 0 10px rgba(56, 189, 248, 0.35);
}

.section-title {
    font-size: 13px;
    font-weight: 700;
    color: #f4f4f5;
}

.section-link {
    font-size: 11px;
    color: #38bdf8;
    background: transparent;
    border: none;
    padding: 2px 6px;
    border-radius: 4px;
}

.section-link:hover {
    background: rgba(56, 189, 248, 0.12);
}

.app-tile {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 8px 4px;
    transition: all 0.15s cubic-bezier(0.16, 1, 0.3, 1);
}

.app-tile:hover {
    background-color: rgba(255, 255, 255, 0.09);
    border: 1px solid rgba(255, 255, 255, 0.14);
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.25);
}

.app-tile:active {
    background-color: rgba(255, 255, 255, 0.05);
}

.app-title {
    font-size: 11px;
    font-weight: 500;
    color: #e4e4e7;
    margin-top: 4px;
}

.rec-item {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 6px 10px;
    transition: all 0.15s ease;
}

.rec-item:hover {
    background-color: rgba(255, 255, 255, 0.08);
    border-color: rgba(255, 255, 255, 0.1);
}

.rec-title {
    font-size: 12px;
    font-weight: 600;
    color: #fafafa;
}

.rec-sub {
    font-size: 10px;
    color: #71717a;
}

.footer-bar {
    background-color: rgba(18, 18, 22, 0.7);
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    border-bottom-left-radius: 14px;
    border-bottom-right-radius: 14px;
    padding: 10px 18px;
}

.user-btn {
    background: transparent;
    border: none;
    border-radius: 6px;
    padding: 4px 8px;
}

.user-btn:hover {
    background-color: rgba(255, 255, 255, 0.08);
}

.user-name {
    font-size: 12px;
    font-weight: 600;
    color: #f4f4f5;
}

.power-btn {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 6px 10px;
    font-size: 15px;
    color: #f4f4f5;
    transition: all 0.15s ease;
}

.power-btn:hover {
    background-color: rgba(239, 68, 68, 0.18);
    border-color: rgba(239, 68, 68, 0.35);
    color: #ef4444;
}

.power-menu-item {
    padding: 8px 14px;
    font-size: 12px;
    color: #f4f4f5;
}
"""

PINNED_APPS = [
    {
        "name": "Crossmanager",
        "label": "File Explorer",
        "icon": "system-file-manager",
        "cmd": "/usr/local/bin/crossmanager",
        "cat": "system"
    },
    {
        "name": "Crossminal",
        "label": "Terminal",
        "icon": "utilities-terminal",
        "cmd": "/usr/local/bin/crossminal",
        "cat": "system"
    },
    {
        "name": "Crosspad",
        "label": "Notepad",
        "icon": "accessories-text-editor",
        "cmd": "/usr/local/bin/crosspad",
        "cat": "utility"
    },
    {
        "name": "Crossings",
        "label": "Settings",
        "icon": "settings",
        "cmd": "/usr/local/bin/crossings",
        "cat": "settings"
    },
    {
        "name": "Crossaint",
        "label": "Paint",
        "icon": "applications-graphics",
        "cmd": "/usr/local/bin/crossaint",
        "cat": "graphics"
    },
    {
        "name": "Crosstos",
        "label": "Photos",
        "icon": "app-gallery-dark",
        "cmd": "/usr/local/bin/crosstos",
        "cat": "graphics"
    },
    {
        "name": "Crossculator",
        "label": "Calculator",
        "icon": "accessories-calculator",
        "cmd": "/usr/local/bin/crossculator",
        "cat": "utility"
    },
    {
        "name": "Crosslock",
        "label": "Clock",
        "icon": "tray-calendar-dark",
        "cmd": "/usr/local/bin/crosslock",
        "cat": "utility"
    },
    {
        "name": "Crossbin",
        "label": "Recycle Bin",
        "icon": "user-trash",
        "cmd": "/usr/local/bin/crossbin",
        "cat": "system"
    },
    {
        "name": "Crossnip",
        "label": "Snipping Tool",
        "icon": "applets-screenshooter",
        "cmd": "/usr/local/bin/crossnip",
        "cat": "utility"
    },
    {
        "name": "Crosslink",
        "label": "Phone Link",
        "icon": "cast-display-dark",
        "cmd": "/usr/local/bin/crosslink",
        "cat": "utility"
    },
    {
        "name": "Crossnarrator",
        "label": "Narrator",
        "icon": "volume-dark",
        "cmd": "/usr/local/bin/crossnarrator",
        "cat": "utility"
    }
]

RECOMMENDED_ITEMS = [
    {
        "name": "Crossminal (Terminal)",
        "sub": "Recently opened • Fluent CLI",
        "icon": "utilities-terminal",
        "cmd": "/usr/local/bin/crossminal"
    },
    {
        "name": "Crossings (Settings)",
        "sub": "System & Personalization Hub",
        "icon": "settings",
        "cmd": "/usr/local/bin/crossings"
    },
    {
        "name": "Crossmanager (Files)",
        "sub": "Home folder & Storage",
        "icon": "system-file-manager",
        "cmd": "/usr/local/bin/crossmanager"
    },
    {
        "name": "Crosspad (Text Editor)",
        "sub": "Zero-telemetry document writer",
        "icon": "accessories-text-editor",
        "cmd": "/usr/local/bin/crosspad"
    }
]

class StartMenuWindow(Gtk.Window):
    def __init__(self):
        super().__init__(type=Gtk.WindowType.TOPLEVEL)
        self.set_title("Start")
        self.set_decorated(False)
        self.set_resizable(False)
        self.set_default_size(580, 590)
        self.set_skip_taskbar_hint(True)
        self.set_skip_pager_hint(True)
        self.set_keep_above(True)
        self.get_style_context().add_class("start-menu")

        # Position window centered at bottom, above taskbar
        screen = Gdk.Screen.get_default()
        if screen:
            geom = screen.get_monitor_geometry(screen.get_primary_monitor())
            win_w = 580
            win_h = 590
            pos_x = geom.x + (geom.width - win_w) // 2
            pos_y = geom.y + geom.height - win_h - 56  # 56px taskbar height + margin
            self.move(pos_x, pos_y)

        # Main Box
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)

        # Upper Content Area (Padding: 20px)
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        content_box.set_margin_top(18)
        content_box.set_margin_bottom(12)
        content_box.set_margin_left(20)
        content_box.set_margin_right(20)
        main_box.pack_start(content_box, True, True, 0)

        # 1. Search Box
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Search for apps, settings, and documents...")
        self.search_entry.get_style_context().add_class("search-box")
        self.search_entry.connect("search-changed", self.on_search_changed)
        self.search_entry.connect("activate", self.on_search_activate)
        content_box.pack_start(self.search_entry, False, False, 0)

        # 2. Pinned Header
        pinned_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        pinned_lbl = Gtk.Label(label="Pinned", xalign=0)
        pinned_lbl.get_style_context().add_class("section-title")
        pinned_header.pack_start(pinned_lbl, True, True, 0)

        all_apps_btn = Gtk.Button(label="All apps >")
        all_apps_btn.get_style_context().add_class("section-link")
        all_apps_btn.connect("clicked", lambda _: self.launch_app("/usr/local/bin/crossings"))
        pinned_header.pack_end(all_apps_btn, False, False, 0)
        content_box.pack_start(pinned_header, False, False, 0)

        # 3. Pinned Apps Grid (6 columns)
        self.apps_flow = Gtk.FlowBox()
        self.apps_flow.set_valign(Gtk.Align.START)
        self.apps_flow.set_max_children_per_line(6)
        self.apps_flow.set_min_children_per_line(6)
        self.apps_flow.set_selection_mode(Gtk.SelectionMode.NONE)
        self.apps_flow.set_homogeneous(True)
        self.apps_flow.set_column_spacing(8)
        self.apps_flow.set_row_spacing(6)
        content_box.pack_start(self.apps_flow, False, False, 0)

        self.tiles = []
        for app in PINNED_APPS:
            tile = self.create_app_tile(app)
            self.apps_flow.add(tile)
            self.tiles.append((app, tile))

        # 4. Recommended Header
        rec_header = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        rec_lbl = Gtk.Label(label="Recommended", xalign=0)
        rec_lbl.get_style_context().add_class("section-title")
        rec_header.pack_start(rec_lbl, True, True, 0)
        content_box.pack_start(rec_header, False, False, 4)

        # 5. Recommended 2x2 Grid
        rec_grid = Gtk.Grid()
        rec_grid.set_column_spacing(12)
        rec_grid.set_row_spacing(6)
        rec_grid.set_column_homogeneous(True)
        content_box.pack_start(rec_grid, False, False, 0)

        for idx, item in enumerate(RECOMMENDED_ITEMS):
            r_item = self.create_rec_item(item)
            col = idx % 2
            row = idx // 2
            rec_grid.attach(r_item, col, row, 1, 1)

        # 6. Bottom Footer Bar (User + Power)
        footer = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        footer.get_style_context().add_class("footer-bar")
        main_box.pack_end(footer, False, False, 0)

        # User profile
        username = getpass.getuser()
        user_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        user_avatar = Gtk.Label(label="👤")
        user_avatar.set_margin_left(4)
        user_name = Gtk.Label(label=username.capitalize(), xalign=0)
        user_name.get_style_context().add_class("user-name")
        user_box.pack_start(user_avatar, False, False, 0)
        user_box.pack_start(user_name, False, False, 0)

        user_btn = Gtk.Button()
        user_btn.add(user_box)
        user_btn.get_style_context().add_class("user-btn")
        user_btn.connect("clicked", lambda _: self.launch_app("/usr/local/bin/crossings"))
        footer.pack_start(user_btn, False, False, 0)

        # Power Button with Popover Menu
        self.power_btn = Gtk.MenuButton()
        self.power_btn.get_style_context().add_class("power-btn")
        self.power_btn.set_label("⏻")

        self.power_popover = Gtk.Popover.new(self.power_btn)
        power_menu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        power_menu_box.set_margin_top(6)
        power_menu_box.set_margin_bottom(6)
        power_menu_box.set_margin_left(6)
        power_menu_box.set_margin_right(6)

        actions = [
            ("🔒  Lock Screen", "loginctl lock-session || crosslock"),
            ("🚪  Sign Out", "pkill -u $USER labwc || pkill -u $USER vde"),
            ("🔄  Restart", "systemctl reboot || reboot"),
            ("⏻  Shut Down", "systemctl poweroff || poweroff")
        ]
        for label, cmd in actions:
            btn = Gtk.Button(label=label, xalign=0)
            btn.get_style_context().add_class("power-menu-item")
            btn.connect("clicked", lambda _, c=cmd: self.execute_power(c))
            power_menu_box.pack_start(btn, False, False, 0)

        self.power_popover.add(power_menu_box)
        self.power_popover.show_all()
        self.power_btn.set_popover(self.power_popover)
        footer.pack_end(self.power_btn, False, False, 0)

        # Signals
        self.connect("key-press-event", self.on_key_press)
        self.connect("focus-out-event", self.on_focus_out)

    def create_app_tile(self, app):
        btn = Gtk.Button()
        btn.get_style_context().add_class("app-tile")
        btn.set_tooltip_text(f"{app['label']} ({app['name']})")

        box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=3)
        box.set_halign(Gtk.Align.CENTER)

        icon_theme = Gtk.IconTheme.get_default()
        icon_path = f"/usr/share/vde/assets/icons/glm/{app['name'].lower()}.svg"
        
        if os.path.exists(icon_path):
            img = Gtk.Image.new_from_file(icon_path)
            img.set_pixel_size(36)
        elif icon_theme.has_icon(app["icon"]):
            img = Gtk.Image.new_from_icon_name(app["icon"], Gtk.IconSize.DND)
            img.set_pixel_size(36)
        else:
            img = Gtk.Image.new_from_icon_name("application-x-executable", Gtk.IconSize.DND)
            img.set_pixel_size(36)

        lbl = Gtk.Label(label=app["label"])
        lbl.get_style_context().add_class("app-title")
        lbl.set_ellipsize(3)  # PANGO_ELLIPSIZE_END
        lbl.set_max_width_chars(10)

        box.pack_start(img, False, False, 0)
        box.pack_start(lbl, False, False, 0)
        btn.add(box)

        btn.connect("clicked", lambda _: self.launch_app(app["cmd"]))
        return btn

    def create_rec_item(self, item):
        btn = Gtk.Button()
        btn.get_style_context().add_class("rec-item")
        
        box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        icon_path = f"/usr/share/vde/assets/icons/glm/{item['name'].split()[0].lower()}.svg"
        if os.path.exists(icon_path):
            img = Gtk.Image.new_from_file(icon_path)
            img.set_pixel_size(28)
        else:
            img = Gtk.Image.new_from_icon_name(item["icon"], Gtk.IconSize.LARGE_TOOLBAR)
            img.set_pixel_size(28)

        text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=1)
        t = Gtk.Label(label=item["name"], xalign=0)
        t.get_style_context().add_class("rec-title")
        s = Gtk.Label(label=item["sub"], xalign=0)
        s.get_style_context().add_class("rec-sub")
        text_box.pack_start(t, False, False, 0)
        text_box.pack_start(s, False, False, 0)

        box.pack_start(img, False, False, 0)
        box.pack_start(text_box, True, True, 0)
        btn.add(box)
        btn.connect("clicked", lambda _: self.launch_app(item["cmd"]))
        return btn

    def on_search_changed(self, entry):
        query = entry.get_text().strip().lower()
        for app, tile in self.tiles:
            matches = (query in app["name"].lower() or 
                       query in app["label"].lower() or 
                       query in app["cat"].lower())
            tile.set_visible(matches or len(query) == 0)

    def on_search_activate(self, entry):
        query = entry.get_text().strip().lower()
        if not query:
            return
        # Launch first matching app
        for app, tile in self.tiles:
            if tile.get_visible():
                self.launch_app(app["cmd"])
                return
        # Fallback to terminal command
        subprocess.Popen(["/usr/local/bin/crossminal", "-e", query], shell=False)
        self.close_and_exit()

    def launch_app(self, cmd):
        # Spawns detached process
        try:
            parts = cmd.split()
            subprocess.Popen(parts, start_new_session=True)
        except Exception as e:
            print(f"[StartMenu Error] Failed to launch {cmd}: {e}")
        self.close_and_exit()

    def execute_power(self, cmd):
        try:
            subprocess.Popen(cmd, shell=True)
        except Exception as e:
            print(f"[Power Error] {e}")
        self.close_and_exit()

    def on_key_press(self, widget, event):
        if event.keyval in (Gdk.KEY_Escape, Gdk.KEY_Super_L, Gdk.KEY_Super_R):
            self.close_and_exit()
            return True
        return False

    def on_focus_out(self, widget, event):
        self.close_and_exit()
        return False

    def close_and_exit(self):
        try:
            if os.path.exists(PID_FILE):
                os.remove(PID_FILE)
        except Exception:
            pass
        Gtk.main_quit()
        sys.exit(0)

def main():
    if not HAS_GTK:
        print("[StartMenu Error] PyGObject (Gtk 3) required.")
        sys.exit(1)

    # Single-instance toggle check
    os.makedirs(os.path.dirname(PID_FILE), exist_ok=True)
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                old_pid = int(f.read().strip())
            os.kill(old_pid, 15)  # SIGTERM to toggle closed
            os.remove(PID_FILE)
            sys.exit(0)
        except Exception:
            pass

    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    # Apply CSS
    style_provider = Gtk.CssProvider()
    style_provider.load_from_data(CSS)
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        style_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    )

    GLib.set_prgname("vde-startmenu")
    GLib.set_application_name("Start Menu")

    win = StartMenuWindow()
    win.show_all()
    win.present()
    win.search_entry.grab_focus()
    Gtk.main()

if __name__ == "__main__":
    main()
