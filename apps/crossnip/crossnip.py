#!/usr/bin/env python3
"""
Crossnip — VDE Fluent Snipping Tool
Modern Dark Mica Screen Capture & Annotation Tool for Victorious Desktop Environment
"""

import os
import sys
import subprocess
import time
from datetime import datetime

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GLib, GdkPixbuf
    HAS_GTK = True
except Exception:
    HAS_GTK = False

CSS_STYLE = b"""
* {
    font-family: 'Segoe UI Variable Text', 'Inter', sans-serif;
    color: #fafafa;
}

window {
    background-color: #18181b;
}

headerbar {
    background: #18181b;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    min-height: 42px;
}

.toolbar-panel {
    background-color: #121214;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding: 8px 16px;
}

button.snip-btn {
    background: #38bdf8;
    color: #09090b;
    font-weight: 700;
    border-radius: 6px;
    padding: 8px 18px;
    border: none;
    font-size: 13px;
}

button.snip-btn:hover {
    background: #7dd3fc;
}

button.tool-btn {
    background: transparent;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 13px;
    color: #e4e4e7;
}

button.tool-btn:hover {
    background: rgba(255, 255, 255, 0.08);
    color: #ffffff;
}

.preview-area {
    background-color: #09090b;
}

.statusbar {
    background-color: #121214;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding: 6px 16px;
    font-size: 11px;
    color: #a1a1aa;
}
"""

class CrossnipApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Snipping Tool")
        self.set_default_size(780, 520)
        self.set_position(Gtk.WindowPosition.CENTER)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(CSS_STYLE)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.last_screenshot_path = None
        self.pixbuf = None

        # HeaderBar
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.props.title = "Snipping Tool"
        header.props.subtitle = "Crossnip"
        self.set_titlebar(header)

        # Main Layout
        root_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(root_box)

        # Toolbar Panel
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        toolbar.get_style_context().add_class("toolbar-panel")
        root_box.pack_start(toolbar, False, False, 0)

        # New Snip Button
        new_snip_btn = Gtk.Button(label="✂ New Snip")
        new_snip_btn.get_style_context().add_class("snip-btn")
        new_snip_btn.connect("clicked", lambda b: self.start_snip())
        toolbar.pack_start(new_snip_btn, False, False, 0)

        # Snip Mode Combo
        self.mode_combo = Gtk.ComboBoxText()
        self.mode_combo.append("region", "Rectangle Snip")
        self.mode_combo.append("fullscreen", "Full Screen")
        self.mode_combo.set_active(0)
        toolbar.pack_start(self.mode_combo, False, False, 0)

        # Delay Combo
        self.delay_combo = Gtk.ComboBoxText()
        self.delay_combo.append("0", "No Delay")
        self.delay_combo.append("3", "3 seconds delay")
        self.delay_combo.append("5", "5 seconds delay")
        self.delay_combo.set_active(0)
        toolbar.pack_start(self.delay_combo, False, False, 0)

        toolbar.pack_start(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL), False, False, 6)

        # Copy & Save
        copy_btn = Gtk.Button(label="📋 Copy")
        copy_btn.get_style_context().add_class("tool-btn")
        copy_btn.connect("clicked", lambda b: self.copy_to_clipboard())
        toolbar.pack_start(copy_btn, False, False, 0)

        save_btn = Gtk.Button(label="💾 Save As")
        save_btn.get_style_context().add_class("tool-btn")
        save_btn.connect("clicked", lambda b: self.save_as_dialog())
        toolbar.pack_start(save_btn, False, False, 0)

        paint_btn = Gtk.Button(label="🎨 Edit in Paint")
        paint_btn.get_style_context().add_class("tool-btn")
        paint_btn.connect("clicked", lambda b: self.edit_in_paint())
        toolbar.pack_start(paint_btn, False, False, 0)

        # Preview Area
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.get_style_context().add_class("preview-area")
        root_box.pack_start(scrolled, True, True, 0)

        self.preview_img = Gtk.Image()
        scrolled.add(self.preview_img)

        # Status Bar
        self.statusbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        self.statusbar.get_style_context().add_class("statusbar")
        root_box.pack_start(self.statusbar, False, False, 0)

        self.status_lbl = Gtk.Label(label="Click 'New Snip' or press Super+Shift+S", xalign=0)
        self.statusbar.pack_start(self.status_lbl, True, True, 0)

    def start_snip(self):
        delay = int(self.delay_combo.get_active_id() or "0")
        mode = self.mode_combo.get_active_id() or "region"

        self.iconify() # Minimize window to capture what is beneath
        GLib.timeout_add(max(200, delay * 1000 + 200), lambda: self.execute_capture(mode))

    def execute_capture(self, mode):
        screenshots_dir = os.path.expanduser("~/Pictures/Screenshots")
        os.makedirs(screenshots_dir, exist_ok=True)
        filename = datetime.now().strftime("Screenshot_%Y%m%d_%H%M%S.png")
        target_path = os.path.join(screenshots_dir, filename)

        try:
            if mode == "region":
                cmd = f'grim -g "$(slurp)" "{target_path}"'
                subprocess.check_call(cmd, shell=True)
            else:
                subprocess.check_call(["grim", target_path])

            if os.path.exists(target_path):
                self.last_screenshot_path = target_path
                self.load_preview(target_path)
                # Copy to Wayland clipboard
                subprocess.Popen(f'wl-copy < "{target_path}"', shell=True)
                self.status_lbl.set_text(f"Captured: {filename} (Copied to Clipboard)")
        except Exception as e:
            self.status_lbl.set_text(f"Capture canceled or failed: {e}")

        self.deiconify()
        self.present()
        return False

    def load_preview(self, path):
        try:
            self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
            alloc = self.get_allocation()
            w = min(self.pixbuf.get_width(), max(400, alloc.width - 40))
            scale = w / self.pixbuf.get_width()
            h = int(self.pixbuf.get_height() * scale)
            scaled = self.pixbuf.scale_simple(w, h, GdkPixbuf.InterpType.BILINEAR)
            self.preview_img.set_from_pixbuf(scaled)
        except Exception as e:
            self.status_lbl.set_text(f"Error loading preview: {e}")

    def copy_to_clipboard(self):
        if self.last_screenshot_path and os.path.exists(self.last_screenshot_path):
            subprocess.Popen(f'wl-copy < "{self.last_screenshot_path}"', shell=True)
            self.status_lbl.set_text("Copied screenshot to clipboard.")

    def save_as_dialog(self):
        if not self.last_screenshot_path or not os.path.exists(self.last_screenshot_path):
            return
        dlg = Gtk.FileChooserDialog(title="Save Screenshot As", parent=self, action=Gtk.FileChooserAction.SAVE)
        dlg.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dlg.add_button("Save", Gtk.ResponseType.ACCEPT)
        dlg.set_current_name(os.path.basename(self.last_screenshot_path))
        if dlg.run() == Gtk.ResponseType.ACCEPT:
            dest = dlg.get_filename()
            dlg.destroy()
            if dest:
                shutil.copy2(self.last_screenshot_path, dest)
                self.status_lbl.set_text(f"Saved to: {dest}")
        else:
            dlg.destroy()

    def edit_in_paint(self):
        if self.last_screenshot_path and os.path.exists(self.last_screenshot_path):
            subprocess.Popen(["/usr/local/bin/crossaint", self.last_screenshot_path])

def main():
    if not HAS_GTK:
        print("[Crossnip Error] PyGObject is required.")
        sys.exit(1)

    app = CrossnipApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
