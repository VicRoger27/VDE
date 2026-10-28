#!/usr/bin/env python3
"""
Crosstos — VDE Fluent Photos
Modern Dark Mica Image & Photo Viewer for Victorious Desktop Environment
"""

import os
import sys
import glob

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
    background-color: #121214;
}

headerbar {
    background: #18181b;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    min-height: 42px;
}

.statusbar {
    background-color: #18181b;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding: 6px 16px;
    font-size: 11px;
    color: #a1a1aa;
}

button.flat-btn {
    background: transparent;
    border: none;
    border-radius: 4px;
    padding: 6px 10px;
    color: #e4e4e7;
    font-size: 13px;
}

button.flat-btn:hover {
    background: rgba(255, 255, 255, 0.08);
    color: #ffffff;
}
"""

IMAGE_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.webp', '.svg', '.bmp', '.gif')

class CrosstosWindow(Gtk.Window):
    def __init__(self, initial_path=None):
        super().__init__(title="Crosstos")
        self.set_default_size(960, 640)
        self.set_position(Gtk.WindowPosition.CENTER)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(CSS_STYLE)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.image_list = []
        self.current_index = -1
        self.original_pixbuf = None
        self.zoom_level = 1.0
        self.rotation_angle = 0
        self.is_fullscreen = False

        # HeaderBar
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.props.title = "Crosstos"
        self.header.props.subtitle = "Photos"
        self.set_titlebar(self.header)

        open_btn = Gtk.Button(label="📂 Open")
        open_btn.get_style_context().add_class("flat-btn")
        open_btn.connect("clicked", lambda b: self.open_dialog())
        self.header.pack_start(open_btn)

        prev_btn = Gtk.Button(label="◀ Prev")
        prev_btn.get_style_context().add_class("flat-btn")
        prev_btn.connect("clicked", lambda b: self.prev_image())
        self.header.pack_start(prev_btn)

        next_btn = Gtk.Button(label="Next ▶")
        next_btn.get_style_context().add_class("flat-btn")
        next_btn.connect("clicked", lambda b: self.next_image())
        self.header.pack_start(next_btn)

        # Zoom controls
        zoom_in = Gtk.Button(label="🔍＋")
        zoom_in.get_style_context().add_class("flat-btn")
        zoom_in.connect("clicked", lambda b: self.zoom(1.2))
        self.header.pack_end(zoom_in)

        zoom_out = Gtk.Button(label="🔍－")
        zoom_out.get_style_context().add_class("flat-btn")
        zoom_out.connect("clicked", lambda b: self.zoom(0.8))
        self.header.pack_end(zoom_out)

        rotate_btn = Gtk.Button(label="↻ Rotate")
        rotate_btn.get_style_context().add_class("flat-btn")
        rotate_btn.connect("clicked", lambda b: self.rotate_clockwise())
        self.header.pack_end(rotate_btn)

        fit_btn = Gtk.Button(label="⛶ Fit")
        fit_btn.get_style_context().add_class("flat-btn")
        fit_btn.connect("clicked", lambda b: self.fit_to_window())
        self.header.pack_end(fit_btn)

        # Layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)

        # Scrolled image viewport
        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        main_box.pack_start(self.scrolled, True, True, 0)

        self.image_widget = Gtk.Image()
        self.scrolled.add(self.image_widget)

        # Status Bar
        self.statusbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        self.statusbar.get_style_context().add_class("statusbar")
        main_box.pack_start(self.statusbar, False, False, 0)

        self.info_lbl = Gtk.Label(label="No image loaded", xalign=0)
        self.statusbar.pack_start(self.info_lbl, True, True, 0)

        self.zoom_lbl = Gtk.Label(label="100%", xalign=1)
        self.statusbar.pack_end(self.zoom_lbl, False, False, 0)

        # Keybindings
        self.connect("key-press-event", self.on_key_press)

        # Load initial file if specified
        if initial_path and os.path.exists(initial_path):
            self.load_directory(initial_path)
            self.load_image_at(self.image_list.index(initial_path) if initial_path in self.image_list else 0)

    def load_directory(self, target_file):
        folder = os.path.dirname(os.path.abspath(target_file))
        self.image_list = []
        try:
            for entry in sorted(os.listdir(folder)):
                ext = os.path.splitext(entry)[1].lower()
                if ext in IMAGE_EXTENSIONS:
                    self.image_list.append(os.path.join(folder, entry))
        except Exception:
            self.image_list = [target_file]

        if target_file in self.image_list:
            self.current_index = self.image_list.index(target_file)
        else:
            self.current_index = 0

    def load_image_at(self, idx):
        if not self.image_list or idx < 0 or idx >= len(self.image_list):
            return
        self.current_index = idx
        path = self.image_list[idx]
        try:
            self.original_pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
            self.rotation_angle = 0
            self.fit_to_window()
            self.header.props.title = os.path.basename(path)
            self.header.props.subtitle = f"{idx + 1} of {len(self.image_list)}"
            w = self.original_pixbuf.get_width()
            h = self.original_pixbuf.get_height()
            size_kb = os.path.getsize(path) / 1024
            self.info_lbl.set_text(f"{w} × {h} px  |  {size_kb:.1f} KB  |  {path}")
        except Exception as e:
            self.info_lbl.set_text(f"Error loading image: {e}")

    def render_image(self):
        if not self.original_pixbuf:
            return
        # Rotate
        pixbuf = self.original_pixbuf
        if self.rotation_angle == 90:
            pixbuf = pixbuf.rotate_simple(GdkPixbuf.PixbufRotation.CLOCKWISE)
        elif self.rotation_angle == 180:
            pixbuf = pixbuf.rotate_simple(GdkPixbuf.PixbufRotation.UPSIDEDOWN)
        elif self.rotation_angle == 270:
            pixbuf = pixbuf.rotate_simple(GdkPixbuf.PixbufRotation.COUNTERCLOCKWISE)

        # Scale
        w = int(pixbuf.get_width() * self.zoom_level)
        h = int(pixbuf.get_height() * self.zoom_level)
        w = max(16, min(10000, w))
        h = max(16, min(10000, h))
        scaled = pixbuf.scale_simple(w, h, GdkPixbuf.InterpType.BILINEAR)
        self.image_widget.set_from_pixbuf(scaled)
        self.zoom_lbl.set_text(f"{int(self.zoom_level * 100)}%")

    def zoom(self, factor):
        self.zoom_level = max(0.1, min(10.0, self.zoom_level * factor))
        self.render_image()

    def fit_to_window(self):
        if not self.original_pixbuf:
            return
        alloc = self.scrolled.get_allocation()
        target_w = max(100, alloc.width - 32)
        target_h = max(100, alloc.height - 32)
        img_w = self.original_pixbuf.get_width()
        img_h = self.original_pixbuf.get_height()
        scale = min(target_w / img_w, target_h / img_h, 1.0)
        self.zoom_level = scale
        self.render_image()

    def rotate_clockwise(self):
        self.rotation_angle = (self.rotation_angle + 90) % 360
        self.render_image()

    def next_image(self):
        if self.image_list:
            next_idx = (self.current_index + 1) % len(self.image_list)
            self.load_image_at(next_idx)

    def prev_image(self):
        if self.image_list:
            prev_idx = (self.current_index - 1) % len(self.image_list)
            self.load_image_at(prev_idx)

    def open_dialog(self):
        dlg = Gtk.FileChooserDialog(title="Open Photo", parent=self, action=Gtk.FileChooserAction.OPEN)
        dlg.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dlg.add_button("Open", Gtk.ResponseType.ACCEPT)
        filter_img = Gtk.FileFilter()
        filter_img.set_name("Images")
        filter_img.add_pixbuf_formats()
        dlg.add_filter(filter_img)

        if dlg.run() == Gtk.ResponseType.ACCEPT:
            path = dlg.get_filename()
            dlg.destroy()
            if path:
                self.load_directory(path)
                self.load_image_at(self.image_list.index(path) if path in self.image_list else 0)
        else:
            dlg.destroy()

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_Right or event.keyval == Gdk.KEY_Page_Down:
            self.next_image()
            return True
        elif event.keyval == Gdk.KEY_Left or event.keyval == Gdk.KEY_Page_Up:
            self.prev_image()
            return True
        elif event.keyval == Gdk.KEY_plus or event.keyval == Gdk.KEY_equal:
            self.zoom(1.2)
            return True
        elif event.keyval == Gdk.KEY_minus:
            self.zoom(0.8)
            return True
        elif event.keyval == Gdk.KEY_F11:
            if self.is_fullscreen:
                self.unfullscreen()
                self.is_fullscreen = False
            else:
                self.fullscreen()
                self.is_fullscreen = True
            return True
        elif event.keyval == Gdk.KEY_Escape and self.is_fullscreen:
            self.unfullscreen()
            self.is_fullscreen = False
            return True
        return False

def main():
    if not HAS_GTK:
        print("[Crosstos Error] PyGObject is required.")
        sys.exit(1)

    initial = sys.argv[1] if len(sys.argv) > 1 else None
    app = CrosstosWindow(initial)
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
