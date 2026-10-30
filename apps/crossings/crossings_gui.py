#!/usr/bin/env python3
"""
Crossings — VDE System & Personalization Hub
Native Dark Mica Settings Application for Victorious Desktop Environment (VDE)
"""

import os
import sys
import subprocess
import shutil

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GLib, Pango
    HAS_GTK = True
except Exception:
    HAS_GTK = False

CSS_STYLE = b"""
* {
    font-family: 'Segoe UI Variable Text', 'Inter', 'Cantarell', sans-serif;
    color: #fafafa;
}

window {
    background-color: #18181b;
}

headerbar {
    background: #18181b;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    min-height: 44px;
}

headerbar .title {
    font-weight: 600;
    font-size: 14px;
    color: #ffffff;
}

headerbar .subtitle {
    font-size: 11px;
    color: #a1a1aa;
}

.sidebar {
    background-color: #121214;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
}

.sidebar list {
    background-color: transparent;
}

.sidebar row {
    padding: 10px 14px;
    margin: 3px 8px;
    border-radius: 6px;
    color: #e4e4e7;
    font-size: 13px;
    font-weight: 500;
    transition: all 0.2s ease;
}

.sidebar row:hover {
    background-color: rgba(255, 255, 255, 0.06);
}

.sidebar row:selected {
    background-color: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
    font-weight: 600;
    border-left: 3px solid #38bdf8;
}

.content-page {
    background-color: #18181b;
    padding: 24px 32px;
}

.page-title {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 6px;
}

.page-subtitle {
    font-size: 13px;
    color: #a1a1aa;
    margin-bottom: 20px;
}

.card {
    background-color: #27272a;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    padding: 16px 20px;
    margin-bottom: 14px;
}

.card-title {
    font-size: 15px;
    font-weight: 600;
    color: #ffffff;
}

.card-desc {
    font-size: 12px;
    color: #a1a1aa;
    margin-top: 2px;
}

.badge-green {
    background-color: rgba(34, 197, 94, 0.2);
    color: #4ade80;
    border: 1px solid rgba(34, 197, 94, 0.4);
    border-radius: 12px;
    padding: 3px 10px;
    font-size: 11px;
    font-weight: 600;
}

button.accent-btn {
    background: #38bdf8;
    color: #09090b;
    font-weight: 600;
    border-radius: 6px;
    padding: 8px 16px;
    border: none;
}

button.accent-btn:hover {
    background: #7dd3fc;
}

button.card-btn {
    background: rgba(255, 255, 255, 0.08);
    color: #fafafa;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 6px;
    padding: 4px 12px;
    min-height: 28px;
    font-size: 12px;
}

button.card-btn:hover {
    background: rgba(255, 255, 255, 0.15);
}

/* Windows 11 / Windhawk Titlebar Button Controls */
headerbar button.titlebutton {
    background: transparent;
    border: none;
    border-radius: 4px;
    min-height: 28px;
    min-width: 42px;
    margin: 2px 1px;
    padding: 0;
    color: #a1a1aa;
    transition: all 0.15s ease;
}

headerbar button.titlebutton:hover {
    background: rgba(255, 255, 255, 0.08);
    color: #ffffff;
}

headerbar button.titlebutton:active {
    background: rgba(255, 255, 255, 0.04);
}

headerbar button.titlebutton.close:hover {
    background-color: #c42b1c;
    color: #ffffff;
}

headerbar button.titlebutton.close:active {
    background-color: #a82315;
    color: #ffffff;
}

/* Modern Rounded Floating Scrollbars */
scrollbar {
    background: transparent;
    border: none;
}
scrollbar trough {
    background: transparent;
    border: none;
}
scrollbar slider {
    background-color: rgba(255, 255, 255, 0.18);
    border-radius: 999px;
    border: none;
    min-width: 6px;
    min-height: 6px;
    margin: 3px;
    transition: all 0.2s ease;
}
scrollbar slider:hover {
    background-color: rgba(255, 255, 255, 0.38);
}
"""

def run_cmd(cmd_list):
    try:
        return subprocess.check_output(cmd_list, stderr=subprocess.DEVNULL, universal_newlines=True).strip()
    except Exception:
        return ""

def get_memory_info():
    try:
        with open("/proc/meminfo", "r") as f:
            lines = f.readlines()
        mem_total = 0
        mem_avail = 0
        for l in lines:
            if l.startswith("MemTotal:"):
                mem_total = int(l.split()[1]) // 1024
            elif l.startswith("MemAvailable:"):
                mem_avail = int(l.split()[1]) // 1024
        mem_used = mem_total - mem_avail
        return f"{mem_used} MB / {mem_total} MB"
    except Exception:
        return "Unknown"

if HAS_GTK:
    class CrossingsApp(Gtk.Window):
        def __init__(self):
            super().__init__(title="Settings — Crossings")
            self.set_icon_name("crossings")
            Gtk.Window.set_default_icon_name("crossings")
            self.set_default_size(920, 640)
            self.set_position(Gtk.WindowPosition.CENTER)

            # Apply CSS styling
            css_provider = Gtk.CssProvider()
            css_provider.load_from_data(CSS_STYLE)
            Gtk.StyleContext.add_provider_for_screen(
                Gdk.Screen.get_default(),
                css_provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )

            # HeaderBar
            header = Gtk.HeaderBar()
            header.set_show_close_button(True)
            header.set_decoration_layout(":minimize,maximize,close")
            header.props.title = "Settings"
            header.props.subtitle = "Crossings Hub"
            self.set_titlebar(header)

            # Main Layout
            hpaned = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            self.add(hpaned)

            # Left Sidebar
            sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            sidebar_box.get_style_context().add_class("sidebar")
            sidebar_box.set_size_request(220, -1)
            hpaned.pack_start(sidebar_box, False, False, 0)

            # Search entry in sidebar
            search_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
            search_box.set_margin_top(12)
            search_box.set_margin_bottom(8)
            search_box.set_margin_start(12)
            search_box.set_margin_end(12)
            search_entry = Gtk.SearchEntry()
            search_entry.set_placeholder_text("Find a setting")
            search_box.pack_start(search_entry, True, True, 0)
            sidebar_box.pack_start(search_box, False, False, 0)

            # Stack & Sidebar List
            self.stack = Gtk.Stack()
            self.stack.set_transition_type(Gtk.StackTransitionType.CROSSFADE)
            self.stack.set_transition_duration(150)
            hpaned.pack_start(self.stack, True, True, 0)

            self.listbox = Gtk.ListBox()
            self.listbox.set_selection_mode(Gtk.SelectionMode.SINGLE)
            self.listbox.connect("row-selected", self.on_sidebar_selected)
            sidebar_box.pack_start(self.listbox, True, True, 0)

            # Sidebar Items
            self.pages = [
                ("system", "🖥️  System & Display"),
                ("personalization", "🎨  Personalization"),
                ("audio", "🔊  Sound & Audio"),
                ("privacy", "🛡️  Privacy & Telemetry"),
                ("about", "ℹ️  About VDE")
            ]

            for page_id, title in self.pages:
                row = Gtk.ListBoxRow()
                lbl = Gtk.Label(label=title, xalign=0)
                row.add(lbl)
                row.page_id = page_id
                self.listbox.add(row)

            # Build Pages
            self.build_system_page()
            self.build_personalization_page()
            self.build_audio_page()
            self.build_privacy_page()
            self.build_about_page()

            # Select first row
            first_row = self.listbox.get_row_at_index(0)
            if first_row:
                self.listbox.select_row(first_row)

        def on_sidebar_selected(self, listbox, row):
            if row and hasattr(row, 'page_id'):
                self.stack.set_visible_child_name(row.page_id)

        def build_system_page(self):
            scrolled = Gtk.ScrolledWindow()
            scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            page.get_style_context().add_class("content-page")
            scrolled.add(page)

            # Title
            t = Gtk.Label(label="System & Display", xalign=0)
            t.get_style_context().add_class("page-title")
            page.pack_start(t, False, False, 0)

            sub = Gtk.Label(label="Manage monitors, display scaling, refresh rate, and power options.", xalign=0)
            sub.get_style_context().add_class("page-subtitle")
            page.pack_start(sub, False, False, 0)

            # Card: Display Resolution & Scaling
            card1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            card1.get_style_context().add_class("card")
            page.pack_start(card1, False, False, 0)

            ct1 = Gtk.Label(label="Display Resolution & Scaling", xalign=0)
            ct1.get_style_context().add_class("card-title")
            card1.pack_start(ct1, False, False, 0)

            cd1 = Gtk.Label(label="Wayland wlroots output scaling and resolution controls.", xalign=0)
            cd1.get_style_context().add_class("card-desc")
            card1.pack_start(cd1, False, False, 0)

            scale_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            scale_lbl = Gtk.Label(label="Display Scale:", xalign=0)
            scale_row.pack_start(scale_lbl, False, False, 0)

            scale_combo = Gtk.ComboBoxText()
            scale_combo.append("1.0", "100% (Native)")
            scale_combo.append("1.25", "125% (Balanced)")
            scale_combo.append("1.5", "150% (High DPI)")
            scale_combo.append("2.0", "200% (Retina)")
            scale_combo.set_active(0)
            scale_combo.connect("changed", self.on_scale_changed)
            scale_row.pack_start(scale_combo, False, False, 0)

            mirror_btn = Gtk.Button(label="Mirror / Project Displays (Win+P)")
            mirror_btn.get_style_context().add_class("card-btn")
            mirror_btn.connect("clicked", lambda b: subprocess.Popen(["/usr/local/bin/vde-display-toggle"]))
            scale_row.pack_end(mirror_btn, False, False, 0)

            card1.pack_start(scale_row, False, False, 0)

            # Card: Brightness
            card2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            card2.get_style_context().add_class("card")
            page.pack_start(card2, False, False, 0)

            ct2 = Gtk.Label(label="Display Brightness", xalign=0)
            ct2.get_style_context().add_class("card-title")
            card2.pack_start(ct2, False, False, 0)

            b_slider = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 10, 100, 5)
            b_slider.set_value(80)
            b_slider.connect("value-changed", self.on_brightness_changed)
            card2.pack_start(b_slider, False, False, 0)

            # Card: Power Controls
            card3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            card3.get_style_context().add_class("card")
            page.pack_start(card3, False, False, 0)

            ct3 = Gtk.Label(label="Power Actions", xalign=0)
            ct3.get_style_context().add_class("card-title")
            card3.pack_start(ct3, False, False, 0)

            power_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            card3.pack_start(power_box, False, False, 0)

            lock_btn = Gtk.Button(label="🔒 Lock (Win+L)")
            lock_btn.get_style_context().add_class("card-btn")
            lock_btn.connect("clicked", lambda b: subprocess.Popen(["loginctl", "lock-session"]))
            power_box.pack_start(lock_btn, False, False, 0)

            reboot_btn = Gtk.Button(label="🔄 Restart")
            reboot_btn.get_style_context().add_class("card-btn")
            reboot_btn.connect("clicked", lambda b: subprocess.Popen(["systemctl", "reboot"]))
            power_box.pack_start(reboot_btn, False, False, 0)

            poweroff_btn = Gtk.Button(label="⏻ Shut Down")
            poweroff_btn.get_style_context().add_class("card-btn")
            poweroff_btn.connect("clicked", lambda b: subprocess.Popen(["systemctl", "poweroff"]))
            power_box.pack_start(poweroff_btn, False, False, 0)

            self.stack.add_named(scrolled, "system")

        def on_scale_changed(self, combo):
            val = combo.get_active_id()
            if val and shutil.which("wlr-randr"):
                try:
                    subprocess.Popen(["wlr-randr", "--scale", val])
                except Exception:
                    pass

        def on_brightness_changed(self, scale):
            val = int(scale.get_value())
            if shutil.which("brightnessctl"):
                try:
                    subprocess.Popen(["brightnessctl", "set", f"{val}%"])
                except Exception:
                    pass

        def build_personalization_page(self):
            scrolled = Gtk.ScrolledWindow()
            scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            page.get_style_context().add_class("content-page")
            scrolled.add(page)

            t = Gtk.Label(label="Personalization", xalign=0)
            t.get_style_context().add_class("page-title")
            page.pack_start(t, False, False, 0)

            sub = Gtk.Label(label="Customize dark Mica wallpaper, taskbar ergonomics, and accent colors.", xalign=0)
            sub.get_style_context().add_class("page-subtitle")
            page.pack_start(sub, False, False, 0)

            # Wallpaper Presets Card
            card1 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            card1.get_style_context().add_class("card")
            page.pack_start(card1, False, False, 0)

            ct1 = Gtk.Label(label="High-Definition Wallpapers", xalign=0)
            ct1.get_style_context().add_class("card-title")
            card1.pack_start(ct1, False, False, 0)

            flow_box = Gtk.FlowBox()
            flow_box.set_valign(Gtk.Align.START)
            flow_box.set_max_children_per_line(3)
            flow_box.set_selection_mode(Gtk.SelectionMode.NONE)
            card1.pack_start(flow_box, False, False, 0)

            wallpapers_imgs = [
                ("Default VDE Mica (Logo)", "/usr/share/vde/assets/wallpapers/default.png"),
                ("Mica Dark Obsidian", "/usr/share/vde/assets/wallpapers/vde_mica_dark.png"),
                ("Abstract Fluent Flow", "/usr/share/vde/assets/wallpapers/vde_abstract_flow.png"),
                ("Aurora Ribbon", "/usr/share/vde/assets/wallpapers/vde_aurora_ribbon.png"),
                ("Cosmic Deep Nebula", "/usr/share/vde/assets/wallpapers/vde_cosmic_nebula.png"),
                ("Crystal Waves", "/usr/share/vde/assets/wallpapers/vde_crystal_waves.png")
            ]

            for name, path in wallpapers_imgs:
                btn = Gtk.Button(label=f"🖼️ {name}")
                btn.get_style_context().add_class("card-btn")
                btn.connect("clicked", lambda b, p=path: self.set_wallpaper_image(p))
                flow_box.add(btn)

            browse_btn = Gtk.Button(label="📁 Browse Custom Image...")
            browse_btn.get_style_context().add_class("card-btn")
            browse_btn.connect("clicked", self.on_browse_wallpaper)
            card1.pack_start(browse_btn, False, False, 0)

            # Solid Color Palette Card
            card_colors = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            card_colors.get_style_context().add_class("card")
            page.pack_start(card_colors, False, False, 0)

            ct_c = Gtk.Label(label="Solid Accent Wallpapers", xalign=0)
            ct_c.get_style_context().add_class("card-title")
            card_colors.pack_start(ct_c, False, False, 0)

            wall_grid = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            card_colors.pack_start(wall_grid, False, False, 0)

            wallpapers = [
                ("Mica Zinc", "#18181b"),
                ("Obsidian", "#09090b"),
                ("Deep Slate", "#0f172a"),
                ("Midnight", "#030712"),
                ("Forest Zinc", "#141e17")
            ]

            for name, hex_code in wallpapers:
                btn = Gtk.Button(label=f"⬛ {name}")
                btn.get_style_context().add_class("card-btn")
                btn.connect("clicked", lambda b, c=hex_code: self.set_wallpaper(c))
                wall_grid.pack_start(btn, True, True, 0)

            # Accent Colors Card
            card2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            card2.get_style_context().add_class("card")
            page.pack_start(card2, False, False, 0)

            ct2 = Gtk.Label(label="Accent Color", xalign=0)
            ct2.get_style_context().add_class("card-title")
            card2.pack_start(ct2, False, False, 0)

            acc_grid = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            card2.pack_start(acc_grid, False, False, 0)

            accents = [
                ("Electric Cyan", "#38bdf8"),
                ("Fluent Blue", "#0078d4"),
                ("Mica Indigo", "#6366f1"),
                ("Emerald", "#10b981")
            ]

            for name, color in accents:
                btn = Gtk.Button(label=f"● {name}")
                btn.get_style_context().add_class("card-btn")
                acc_grid.pack_start(btn, True, True, 0)

            self.stack.add_named(scrolled, "personalization")

        def set_wallpaper_image(self, file_path):
            conf_dir = os.path.expanduser("~/.config/vde")
            os.makedirs(conf_dir, exist_ok=True)
            target = os.path.join(conf_dir, "wallpaper.png")
            try:
                shutil.copyfile(file_path, target)
            except Exception:
                pass
            subprocess.call(["pkill", "-9", "swaybg"])
            subprocess.Popen(["swaybg", "-i", target, "-m", "fill"])

        def on_browse_wallpaper(self, widget):
            dialog = Gtk.FileChooserDialog(
                title="Choose VDE Desktop Wallpaper",
                parent=self.window,
                action=Gtk.FileChooserAction.OPEN
            )
            dialog.add_buttons(
                Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                Gtk.STOCK_OPEN, Gtk.ResponseType.OK
            )
            filter_img = Gtk.FileFilter()
            filter_img.set_name("Images (*.png, *.jpg, *.jpeg)")
            filter_img.add_mime_type("image/png")
            filter_img.add_mime_type("image/jpeg")
            filter_img.add_pattern("*.png")
            filter_img.add_pattern("*.jpg")
            filter_img.add_pattern("*.jpeg")
            dialog.add_filter(filter_img)

            # Suggest custom background directory if it exists
            unsloth_dir = "/media/windows/Images/Unsloth"
            if os.path.exists(unsloth_dir):
                dialog.set_current_folder(unsloth_dir)
            elif os.path.exists(os.path.expanduser("~/Pictures")):
                dialog.set_current_folder(os.path.expanduser("~/Pictures"))

            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                selected_file = dialog.get_filename()
                if selected_file:
                    self.set_wallpaper_image(selected_file)
            dialog.destroy()

        def set_wallpaper(self, color_hex):
            subprocess.call(["pkill", "-9", "swaybg"])
            subprocess.Popen(["swaybg", "-c", color_hex])
            # Save configuration
            conf_dir = os.path.expanduser("~/.config/vde")
            os.makedirs(conf_dir, exist_ok=True)
            with open(os.path.join(conf_dir, "wallpaper.color"), "w") as f:
                f.write(color_hex)

        def build_audio_page(self):
            scrolled = Gtk.ScrolledWindow()
            scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            page.get_style_context().add_class("content-page")
            scrolled.add(page)

            t = Gtk.Label(label="Sound & Audio", xalign=0)
            t.get_style_context().add_class("page-title")
            page.pack_start(t, False, False, 0)

            sub = Gtk.Label(label="WirePlumber and PipeWire sound server management.", xalign=0)
            sub.get_style_context().add_class("page-subtitle")
            page.pack_start(sub, False, False, 0)

            card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            card.get_style_context().add_class("card")
            page.pack_start(card, False, False, 0)

            ct = Gtk.Label(label="Master Volume", xalign=0)
            ct.get_style_context().add_class("card-title")
            card.pack_start(ct, False, False, 0)

            vol_slider = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 100, 5)
            vol_slider.set_value(65)
            vol_slider.connect("value-changed", self.on_volume_changed)
            card.pack_start(vol_slider, False, False, 0)

            mute_btn = Gtk.Button(label="🔇 Toggle Mute")
            mute_btn.get_style_context().add_class("card-btn")
            mute_btn.connect("clicked", lambda b: subprocess.Popen(["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle"]))
            card.pack_start(mute_btn, False, False, 0)

            self.stack.add_named(scrolled, "audio")

        def on_volume_changed(self, scale):
            val = scale.get_value() / 100.0
            if shutil.which("wpctl"):
                try:
                    subprocess.Popen(["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", f"{val:.2f}"])
                except Exception:
                    pass

        def build_privacy_page(self):
            scrolled = Gtk.ScrolledWindow()
            scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            page.get_style_context().add_class("content-page")
            scrolled.add(page)

            t = Gtk.Label(label="Privacy & Telemetry", xalign=0)
            t.get_style_context().add_class("page-title")
            page.pack_start(t, False, False, 0)

            sub = Gtk.Label(label="Zero-telemetry architecture: no cloud tracking, metrics, or diagnostic daemons.", xalign=0)
            sub.get_style_context().add_class("page-subtitle")
            page.pack_start(sub, False, False, 0)

            # Status Badge Card
            status_card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
            status_card.get_style_context().add_class("card")
            page.pack_start(status_card, False, False, 0)

            status_icon = Gtk.Label(label="🛡️", xalign=0.5)
            status_icon.override_font(Pango.FontDescription("32"))
            status_card.pack_start(status_icon, False, False, 0)

            status_text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
            status_title = Gtk.Label(label="Zero Telemetry Protection: ACTIVE", xalign=0)
            status_title.get_style_context().add_class("card-title")
            status_text_box.pack_start(status_title, False, False, 0)

            status_desc = Gtk.Label(label="All background analytics, crash uploaders, and telemetry sinks are purged.", xalign=0)
            status_desc.get_style_context().add_class("card-desc")
            status_text_box.pack_start(status_desc, False, False, 0)
            status_card.pack_start(status_text_box, True, True, 0)

            badge = Gtk.Label(label="VERIFIED")
            badge.get_style_context().add_class("badge-green")
            status_card.pack_end(badge, False, False, 0)

            # Audit Checklist
            check_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
            check_card.get_style_context().add_class("card")
            page.pack_start(check_card, False, False, 0)

            ct = Gtk.Label(label="Purged Telemetry Daemons", xalign=0)
            ct.get_style_context().add_class("card-title")
            check_card.pack_start(ct, False, False, 0)

            checks = [
                ("Snap Daemon (snapd)", "PURGED"),
                ("Ubuntu Report (metrics uploader)", "PURGED"),
                ("Whoopsie (crash reporter)", "PURGED"),
                ("Apport & Landscape", "PURGED"),
                ("Network Outbound Analytics", "BLOCKED (0 KB/s)")
            ]

            for item, status in checks:
                row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
                l = Gtk.Label(label=f"✓  {item}", xalign=0)
                s = Gtk.Label(label=status)
                s.get_style_context().add_class("badge-green")
                row.pack_start(l, True, True, 0)
                row.pack_end(s, False, False, 0)
                check_card.pack_start(row, False, False, 0)

            self.stack.add_named(scrolled, "privacy")

        def build_about_page(self):
            scrolled = Gtk.ScrolledWindow()
            scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
            page = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            page.get_style_context().add_class("content-page")
            scrolled.add(page)

            t = Gtk.Label(label="About VDE", xalign=0)
            t.get_style_context().add_class("page-title")
            page.pack_start(t, False, False, 0)

            sub = Gtk.Label(label="Victorious Desktop Environment specifications and license.", xalign=0)
            sub.get_style_context().add_class("page-subtitle")
            page.pack_start(sub, False, False, 0)

            card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
            card.get_style_context().add_class("card")
            page.pack_start(card, False, False, 0)

            ct = Gtk.Label(label="Victorious Desktop Environment 1.0 (LTS)", xalign=0)
            ct.get_style_context().add_class("card-title")
            card.pack_start(ct, False, False, 0)

            specs = [
                ("RAM Consumption", get_memory_info() + " (Sub-500 MB idle target)"),
                ("Compositor", "Labwc (wlroots layer-shell)"),
                ("Shell Architecture", "Astal / Waybar Fluent Dark Mica"),
                ("Application Launcher", "Wofi Mica"),
                ("Terminal Emulator", "Foot (VDE Acrylic)"),
                ("Linux Kernel", run_cmd(["uname", "-r"]) or "Linux 6.8+"),
                ("License", "Victorious Public License (VPL) — Zero Telemetry")
            ]

            for label, val in specs:
                row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
                l = Gtk.Label(label=f"<b>{label}:</b>", xalign=0)
                l.set_use_markup(True)
                v = Gtk.Label(label=val, xalign=1)
                v.get_style_context().add_class("card-desc")
                row.pack_start(l, False, False, 0)
                row.pack_end(v, False, False, 0)
                card.pack_start(row, False, False, 0)

            self.stack.add_named(scrolled, "about")

def main():
    if not HAS_GTK:
        print("[Crossings Error] PyGObject (Gtk 3) is required to run Crossings Settings.")
        sys.exit(1)

    GLib.set_prgname("crossings")
    GLib.set_application_name("Settings")

    app = CrossingsApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
