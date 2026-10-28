#!/usr/bin/env python3
"""
Crossaint — VDE Fluent Paint
Modern Dark Mica creative canvas and image editor for Victorious Desktop Environment
"""

import os
import sys

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GLib, GdkPixbuf, cairo
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

button.tool-btn {
    background: transparent;
    border: 1px solid transparent;
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 13px;
    color: #e4e4e7;
}

button.tool-btn:hover {
    background: rgba(255, 255, 255, 0.08);
    color: #ffffff;
}

button.tool-btn:checked {
    background: rgba(56, 189, 248, 0.2);
    border: 1px solid #38bdf8;
    color: #38bdf8;
    font-weight: 600;
}

.canvas-area {
    background-color: #27272a;
}
"""

class CrossaintWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Crossaint")
        self.set_icon_name("crossaint")
        Gtk.Window.set_default_icon_name("crossaint")
        self.set_default_size(960, 640)
        self.set_position(Gtk.WindowPosition.CENTER)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(CSS_STYLE)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # Drawing state
        self.surface = None
        self.current_tool = "brush"   # brush, line, rect, ellipse, eraser
        self.brush_size = 4
        self.current_color = (0.22, 0.74, 0.97, 1.0) # #38bdf8
        self.start_pos = None
        self.last_pos = None

        # HeaderBar
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.set_decoration_layout(":minimize,maximize,close")
        self.header.props.title = "Crossaint"
        self.header.props.subtitle = "Creative Canvas"
        self.set_titlebar(self.header)

        open_btn = Gtk.Button(label="📂 Open")
        open_btn.get_style_context().add_class("tool-btn")
        open_btn.connect("clicked", lambda b: self.open_image())
        self.header.pack_start(open_btn)

        save_btn = Gtk.Button(label="💾 Save")
        save_btn.get_style_context().add_class("tool-btn")
        save_btn.connect("clicked", lambda b: self.save_image())
        self.header.pack_start(save_btn)

        clear_btn = Gtk.Button(label="🗑 Clear")
        clear_btn.get_style_context().add_class("tool-btn")
        clear_btn.connect("clicked", lambda b: self.clear_canvas())
        self.header.pack_end(clear_btn)

        # Main Layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)

        # Toolbar Panel
        toolbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        toolbar.get_style_context().add_class("toolbar-panel")
        main_box.pack_start(toolbar, False, False, 0)

        # Tools group
        tools = [
            ("brush", "🖌 Brush"),
            ("line", "╱ Line"),
            ("rect", "▭ Rectangle"),
            ("ellipse", "◯ Circle"),
            ("eraser", "⌫ Eraser")
        ]
        self.tool_buttons = {}
        first_btn = None
        for tid, label in tools:
            btn = Gtk.RadioButton.new_with_label_from_widget(first_btn, label)
            btn.set_mode(False) # Pushbutton appearance
            btn.get_style_context().add_class("tool-btn")
            btn.connect("toggled", self.on_tool_toggled, tid)
            toolbar.pack_start(btn, False, False, 0)
            self.tool_buttons[tid] = btn
            if not first_btn:
                first_btn = btn

        toolbar.pack_start(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL), False, False, 6)

        # Size Slider
        size_lbl = Gtk.Label(label="Size:")
        toolbar.pack_start(size_lbl, False, False, 0)

        size_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 40, 1)
        size_scale.set_size_request(100, -1)
        size_scale.set_value(4)
        size_scale.connect("value-changed", self.on_size_changed)
        toolbar.pack_start(size_scale, False, False, 0)

        toolbar.pack_start(Gtk.Separator(orientation=Gtk.Orientation.VERTICAL), False, False, 6)

        # Colors Palette
        color_lbl = Gtk.Label(label="Color:")
        toolbar.pack_start(color_lbl, False, False, 0)

        colors = [
            ("#ffffff", (1.0, 1.0, 1.0, 1.0)),
            ("#18181b", (0.09, 0.09, 0.11, 1.0)),
            ("#ef4444", (0.94, 0.27, 0.27, 1.0)),
            ("#22c55e", (0.13, 0.77, 0.37, 1.0)),
            ("#38bdf8", (0.22, 0.74, 0.97, 1.0)),
            ("#eab308", (0.92, 0.70, 0.03, 1.0)),
            ("#a855f7", (0.66, 0.33, 0.97, 1.0))
        ]
        for name, rgb in colors:
            btn = Gtk.Button(label="●")
            btn.get_style_context().add_class("tool-btn")
            btn.connect("clicked", lambda b, c=rgb: self.set_color(c))
            toolbar.pack_start(btn, False, False, 0)

        # Custom Color Button
        color_btn = Gtk.ColorButton()
        color_btn.set_rgba(Gdk.RGBA(0.22, 0.74, 0.97, 1.0))
        color_btn.connect("color-set", self.on_custom_color)
        toolbar.pack_start(color_btn, False, False, 0)

        # Scrolled Canvas
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        main_box.pack_start(scrolled, True, True, 0)

        self.darea = Gtk.DrawingArea()
        self.darea.set_size_request(1280, 800)
        self.darea.connect("draw", self.on_draw)
        self.darea.connect("configure-event", self.on_configure)
        self.darea.connect("motion-notify-event", self.on_motion_notify)
        self.darea.connect("button-press-event", self.on_button_press)
        self.darea.connect("button-release-event", self.on_button_release)
        self.darea.set_events(
            Gdk.EventMask.BUTTON_PRESS_MASK |
            Gdk.EventMask.BUTTON_RELEASE_MASK |
            Gdk.EventMask.POINTER_MOTION_MASK
        )
        scrolled.add(self.darea)

    def on_tool_toggled(self, btn, tool_id):
        if btn.get_active():
            self.current_tool = tool_id

    def on_size_changed(self, scale):
        self.brush_size = int(scale.get_value())

    def set_color(self, rgb):
        self.current_color = rgb

    def on_custom_color(self, btn):
        rgba = btn.get_rgba()
        self.current_color = (rgba.red, rgba.green, rgba.blue, rgba.alpha)

    def on_configure(self, widget, event):
        alloc = widget.get_allocation()
        if self.surface:
            # Preserve old content
            old_surf = self.surface
            self.surface = widget.get_window().create_similar_surface(
                cairo.CONTENT_COLOR,
                max(alloc.width, 1280),
                max(alloc.height, 800)
            )
            cr = cairo.Context(self.surface)
            cr.set_source_rgb(1.0, 1.0, 1.0)
            cr.paint()
            cr.set_source_surface(old_surf, 0, 0)
            cr.paint()
        else:
            self.surface = widget.get_window().create_similar_surface(
                cairo.CONTENT_COLOR,
                max(alloc.width, 1280),
                max(alloc.height, 800)
            )
            cr = cairo.Context(self.surface)
            cr.set_source_rgb(1.0, 1.0, 1.0) # White canvas
            cr.paint()
        return True

    def on_draw(self, widget, cr):
        if self.surface:
            cr.set_source_surface(self.surface, 0, 0)
            cr.paint()
        return False

    def on_button_press(self, widget, event):
        if event.button == 1:
            self.start_pos = (event.x, event.y)
            self.last_pos = (event.x, event.y)
            if self.current_tool in ("brush", "eraser"):
                self.draw_brush(event.x, event.y)
        return True

    def on_motion_notify(self, widget, event):
        if event.state & Gdk.ModifierType.BUTTON1_MASK:
            if self.current_tool in ("brush", "eraser"):
                self.draw_brush(event.x, event.y)
                self.last_pos = (event.x, event.y)
        return True

    def on_button_release(self, widget, event):
        if event.button == 1 and self.start_pos:
            end_pos = (event.x, event.y)
            if self.current_tool == "line":
                cr = cairo.Context(self.surface)
                cr.set_source_rgba(*self.current_color)
                cr.set_line_width(self.brush_size)
                cr.set_line_cap(cairo.LINE_CAP_ROUND)
                cr.move_to(self.start_pos[0], self.start_pos[1])
                cr.line_to(end_pos[0], end_pos[1])
                cr.stroke()
            elif self.current_tool == "rect":
                cr = cairo.Context(self.surface)
                cr.set_source_rgba(*self.current_color)
                cr.set_line_width(self.brush_size)
                x = min(self.start_pos[0], end_pos[0])
                y = min(self.start_pos[1], end_pos[1])
                w = abs(end_pos[0] - self.start_pos[0])
                h = abs(end_pos[1] - self.start_pos[1])
                cr.rectangle(x, y, w, h)
                cr.stroke()
            elif self.current_tool == "ellipse":
                cr = cairo.Context(self.surface)
                cr.set_source_rgba(*self.current_color)
                cr.set_line_width(self.brush_size)
                x = min(self.start_pos[0], end_pos[0])
                y = min(self.start_pos[1], end_pos[1])
                w = abs(end_pos[0] - self.start_pos[0])
                h = abs(end_pos[1] - self.start_pos[1])
                cr.save()
                cr.translate(x + w / 2, y + h / 2)
                cr.scale(w / 2, h / 2)
                cr.arc(0, 0, 1.0, 0, 2 * 3.14159)
                cr.restore()
                cr.stroke()
            self.darea.queue_draw()
            self.start_pos = None
            self.last_pos = None
        return True

    def draw_brush(self, x, y):
        cr = cairo.Context(self.surface)
        if self.current_tool == "eraser":
            cr.set_source_rgb(1.0, 1.0, 1.0)
            cr.set_line_width(self.brush_size * 3)
        else:
            cr.set_source_rgba(*self.current_color)
            cr.set_line_width(self.brush_size)
        cr.set_line_cap(cairo.LINE_CAP_ROUND)
        cr.set_line_join(cairo.LINE_JOIN_ROUND)

        if self.last_pos:
            cr.move_to(self.last_pos[0], self.last_pos[1])
            cr.line_to(x, y)
            cr.stroke()
        self.darea.queue_draw()

    def clear_canvas(self):
        if self.surface:
            cr = cairo.Context(self.surface)
            cr.set_source_rgb(1.0, 1.0, 1.0)
            cr.paint()
            self.darea.queue_draw()

    def open_image(self):
        dlg = Gtk.FileChooserDialog(title="Open Image", parent=self, action=Gtk.FileChooserAction.OPEN)
        dlg.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dlg.add_button("Open", Gtk.ResponseType.ACCEPT)
        if dlg.run() == Gtk.ResponseType.ACCEPT:
            path = dlg.get_filename()
            dlg.destroy()
            if path and os.path.exists(path):
                pixbuf = GdkPixbuf.Pixbuf.new_from_file(path)
                cr = cairo.Context(self.surface)
                Gdk.cairo_set_source_pixbuf(cr, pixbuf, 0, 0)
                cr.paint()
                self.darea.queue_draw()
        else:
            dlg.destroy()

    def save_image(self):
        dlg = Gtk.FileChooserDialog(title="Save Canvas As", parent=self, action=Gtk.FileChooserAction.SAVE)
        dlg.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dlg.add_button("Save", Gtk.ResponseType.ACCEPT)
        dlg.set_current_name("Drawing.png")
        if dlg.run() == Gtk.ResponseType.ACCEPT:
            path = dlg.get_filename()
            dlg.destroy()
            if path:
                if not path.lower().endswith(".png"):
                    path += ".png"
                self.surface.write_to_png(path)
        else:
            dlg.destroy()

def main():
    if not HAS_GTK:
        print("[Crossaint Error] PyGObject is required.")
        sys.exit(1)

    GLib.set_prgname("crossaint")
    GLib.set_application_name("Crossaint")

    app = CrossaintWindow()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
