#!/usr/bin/env python3
"""
Crossminal — VDE Fluent Acrylic Terminal
Modern Dark Mica Terminal Emulator for Victorious Desktop Environment
"""

import os
import sys

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GLib
    HAS_GTK = True
except Exception:
    HAS_GTK = False

try:
    gi.require_version('Vte', '2.91')
    from gi.repository import Vte
    HAS_VTE = True
except Exception:
    HAS_VTE = False

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
    min-height: 40px;
}

headerbar .title {
    font-weight: 600;
    font-size: 13px;
    color: #ffffff;
}

notebook {
    background-color: #18181b;
    border: none;
}

notebook tab {
    background-color: #121214;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-bottom: none;
    border-radius: 6px 6px 0 0;
    padding: 4px 12px;
    margin-right: 4px;
    font-size: 11px;
    color: #a1a1aa;
}

notebook tab:checked {
    background-color: #18181b;
    border-top: 2px solid #38bdf8;
    color: #ffffff;
    font-weight: 600;
}

button.flat-btn {
    background: transparent;
    border: none;
    border-radius: 4px;
    padding: 4px 8px;
    color: #e4e4e7;
}

button.flat-btn:hover {
    background: rgba(255, 255, 255, 0.08);
    color: #ffffff;
}
"""

# VDE Dark Mica Terminal Color Palette
COLOR_BG = Gdk.RGBA(0.094, 0.094, 0.106, 0.95)   # #18181b
COLOR_FG = Gdk.RGBA(0.98, 0.98, 0.98, 1.0)       # #fafafa

PALETTE = [
    Gdk.RGBA(0.094, 0.094, 0.106, 1.0),  # Black (#18181b)
    Gdk.RGBA(0.937, 0.267, 0.267, 1.0),  # Red (#ef4444)
    Gdk.RGBA(0.133, 0.773, 0.369, 1.0),  # Green (#22c55e)
    Gdk.RGBA(0.918, 0.702, 0.031, 1.0),  # Yellow (#eab308)
    Gdk.RGBA(0.220, 0.741, 0.973, 1.0),  # Blue/Cyan (#38bdf8)
    Gdk.RGBA(0.659, 0.333, 0.969, 1.0),  # Magenta (#a855f7)
    Gdk.RGBA(0.024, 0.714, 0.831, 1.0),  # Cyan (#06b6d4)
    Gdk.RGBA(0.957, 0.957, 0.961, 1.0),  # White (#f4f4f5)
    # Brights
    Gdk.RGBA(0.153, 0.153, 0.165, 1.0),  # Bright Black (#27272a)
    Gdk.RGBA(0.973, 0.443, 0.443, 1.0),  # Bright Red (#f87171)
    Gdk.RGBA(0.290, 0.871, 0.502, 1.0),  # Bright Green (#4ade80)
    Gdk.RGBA(0.992, 0.878, 0.278, 1.0),  # Bright Yellow (#fde047)
    Gdk.RGBA(0.376, 0.647, 0.980, 1.0),  # Bright Blue (#60a5fa)
    Gdk.RGBA(0.753, 0.518, 0.988, 1.0),  # Bright Magenta (#c084fc)
    Gdk.RGBA(0.133, 0.827, 0.933, 1.0),  # Bright Cyan (#22d3ee)
    Gdk.RGBA(1.000, 1.000, 1.000, 1.0),  # Bright White (#ffffff)
]

class CrossminalWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Crossminal")
        self.set_icon_name("crossminal")
        Gtk.Window.set_default_icon_name("crossminal")
        self.set_default_size(840, 520)
        self.set_position(Gtk.WindowPosition.CENTER)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(CSS_STYLE)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        # HeaderBar
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.set_decoration_layout(":minimize,maximize,close")
        self.header.props.title = "Crossminal"
        self.header.props.subtitle = "Victorious Terminal"
        self.set_titlebar(self.header)

        new_tab_btn = Gtk.Button(label="＋ New Tab")
        new_tab_btn.get_style_context().add_class("flat-btn")
        new_tab_btn.connect("clicked", lambda b: self.add_terminal_tab())
        self.header.pack_start(new_tab_btn)

        zoom_in_btn = Gtk.Button(label="A+")
        zoom_in_btn.get_style_context().add_class("flat-btn")
        zoom_in_btn.connect("clicked", lambda b: self.change_font_scale(1.1))
        self.header.pack_end(zoom_in_btn)

        zoom_out_btn = Gtk.Button(label="A-")
        zoom_out_btn.get_style_context().add_class("flat-btn")
        zoom_out_btn.connect("clicked", lambda b: self.change_font_scale(0.9))
        self.header.pack_end(zoom_out_btn)

        self.notebook = Gtk.Notebook()
        self.notebook.set_scrollable(True)
        self.add(self.notebook)

        self.add_terminal_tab()

    def add_terminal_tab(self):
        vte = Vte.Terminal()
        vte.set_colors(COLOR_FG, COLOR_BG, PALETTE)
        vte.set_scroll_on_output(True)
        vte.set_scroll_on_keystroke(True)
        vte.set_mouse_autohide(True)
        vte.set_audible_bell(False)
        vte.set_font_scale(1.0)

        # Spawn default shell
        shell = os.environ.get("SHELL", "/bin/bash")
        vte.spawn_async(
            Vte.PtyFlags.DEFAULT,
            os.path.expanduser("~"),
            [shell],
            None,
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
            -1,
            None,
            None
        )

        vte.connect("child-exited", lambda term, status: self.on_terminal_exit(vte))
        vte.connect("window-title-changed", lambda term: self.on_title_changed(term))

        scrolled = Gtk.ScrolledWindow()
        scrolled.add(vte)

        tab_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        lbl = Gtk.Label(label="Terminal")
        tab_box.pack_start(lbl, True, True, 0)

        close_btn = Gtk.Button(label="×")
        close_btn.get_style_context().add_class("flat-btn")
        close_btn.connect("clicked", lambda b: self.close_terminal_tab(scrolled))
        tab_box.pack_start(close_btn, False, False, 0)
        tab_box.show_all()

        scrolled.tab_label = lbl
        scrolled.vte = vte

        page_num = self.notebook.append_page(scrolled, tab_box)
        self.notebook.show_all()
        self.notebook.set_current_page(page_num)
        vte.grab_focus()

    def on_title_changed(self, vte):
        title = vte.get_window_title() or "Terminal"
        for i in range(self.notebook.get_n_pages()):
            page = self.notebook.get_nth_page(i)
            if hasattr(page, 'vte') and page.vte == vte:
                page.tab_label.set_text(title[:20])
                break

    def on_terminal_exit(self, vte):
        for i in range(self.notebook.get_n_pages()):
            page = self.notebook.get_nth_page(i)
            if hasattr(page, 'vte') and page.vte == vte:
                self.notebook.remove_page(i)
                break
        if self.notebook.get_n_pages() == 0:
            self.destroy()

    def close_terminal_tab(self, page):
        num = self.notebook.page_num(page)
        if num != -1:
            self.notebook.remove_page(num)
        if self.notebook.get_n_pages() == 0:
            self.destroy()

    def change_font_scale(self, factor):
        page_num = self.notebook.get_current_page()
        if page_num != -1:
            page = self.notebook.get_nth_page(page_num)
            if hasattr(page, 'vte'):
                scale = page.vte.get_font_scale() * factor
                page.vte.set_font_scale(max(0.6, min(2.5, scale)))

def main():

    GLib.set_prgname("crossminal")
    GLib.set_application_name("Crossminal")
    if not HAS_GTK or not HAS_VTE:
        # Fallback cleanly to foot or xterm
        if os.path.exists("/usr/local/bin/vde-terminal"):
            os.execv("/usr/local/bin/vde-terminal", ["vde-terminal"] + sys.argv[1:])
        elif shutil.which("foot"):
            os.execv(shutil.which("foot"), ["foot"] + sys.argv[1:])
        elif shutil.which("xterm"):
            os.execv(shutil.which("xterm"), ["xterm", "-bg", "#18181b", "-fg", "#fafafa"] + sys.argv[1:])
        sys.exit(1)

    app = CrossminalWindow()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
