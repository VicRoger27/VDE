#!/usr/bin/env python3
"""
Crosspad — VDE Fluent Notepad
Ultra-lightweight, tabbed, modern Dark Mica text editor for Victorious Desktop Environment
"""

import os
import sys

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
    min-height: 42px;
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
    padding: 6px 14px;
    margin-right: 4px;
    font-size: 12px;
    color: #a1a1aa;
}

notebook tab:checked {
    background-color: #18181b;
    border-top: 2px solid #38bdf8;
    color: #ffffff;
    font-weight: 600;
}

textview {
    background-color: #18181b;
    color: #f4f4f5;
    font-family: 'DejaVu Sans Mono', 'Cascadia Code', 'Consolas', monospace;
    font-size: 13px;
}

textview text {
    background-color: #18181b;
    color: #f4f4f5;
}

.statusbar {
    background-color: #121214;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding: 4px 16px;
    font-size: 11px;
    color: #a1a1aa;
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

button.accent-btn {
    background: #38bdf8;
    color: #09090b;
    font-weight: 600;
    border-radius: 4px;
    padding: 4px 12px;
    border: none;
}
"""

class CrosspadTab(Gtk.Box):
    def __init__(self, filepath=None):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_icon_name("crosspad")
        Gtk.Window.set_default_icon_name("crosspad")
        self.filepath = filepath
        self.filename = os.path.basename(filepath) if filepath else "Untitled"
        self.is_modified = False

        self.scrolled = Gtk.ScrolledWindow()
        self.scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        self.pack_start(self.scrolled, True, True, 0)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.textview.set_left_margin(16)
        self.textview.set_right_margin(16)
        self.textview.set_top_margin(12)
        self.textview.set_bottom_margin(12)
        self.buffer = self.textview.get_buffer()
        self.buffer.connect("changed", self.on_text_changed)
        self.scrolled.add(self.textview)

        if filepath and os.path.exists(filepath):
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    self.buffer.set_text(f.read())
                self.is_modified = False
            except Exception as e:
                self.buffer.set_text(f"Error opening file: {e}")

    def on_text_changed(self, buf):
        self.is_modified = True

class CrosspadApp(Gtk.Window):
    def __init__(self, initial_files=None):
        super().__init__(title="Crosspad")
        self.set_default_size(880, 560)
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
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.set_decoration_layout(":minimize,maximize,close")
        self.header.props.title = "Crosspad"
        self.header.props.subtitle = "Victorious Text Editor"
        self.set_titlebar(self.header)

        # HeaderBar actions
        new_btn = Gtk.Button(label="📄 New")
        new_btn.get_style_context().add_class("flat-btn")
        new_btn.connect("clicked", lambda b: self.new_tab())
        self.header.pack_start(new_btn)

        open_btn = Gtk.Button(label="📂 Open")
        open_btn.get_style_context().add_class("flat-btn")
        open_btn.connect("clicked", lambda b: self.open_file_dialog())
        self.header.pack_start(open_btn)

        save_btn = Gtk.Button(label="💾 Save")
        save_btn.get_style_context().add_class("flat-btn")
        save_btn.connect("clicked", lambda b: self.save_current_tab())
        self.header.pack_start(save_btn)

        find_btn = Gtk.Button(label="🔍 Find")
        find_btn.get_style_context().add_class("flat-btn")
        find_btn.connect("clicked", lambda b: self.show_find_dialog())
        self.header.pack_end(find_btn)

        # Main Layout
        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)

        # Notebook (tabs)
        self.notebook = Gtk.Notebook()
        self.notebook.set_scrollable(True)
        self.notebook.connect("switch-page", self.on_switch_page)
        main_box.pack_start(self.notebook, True, True, 0)

        # Status Bar
        self.statusbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        self.statusbar.get_style_context().add_class("statusbar")
        main_box.pack_start(self.statusbar, False, False, 0)

        self.pos_lbl = Gtk.Label(label="Ln 1, Col 1", xalign=0)
        self.statusbar.pack_start(self.pos_lbl, False, False, 0)

        self.char_lbl = Gtk.Label(label="0 characters", xalign=0)
        self.statusbar.pack_start(self.char_lbl, False, False, 0)

        encoding_lbl = Gtk.Label(label="UTF-8", xalign=1)
        self.statusbar.pack_end(encoding_lbl, False, False, 0)

        # Open files or blank tab
        if initial_files:
            for f in initial_files:
                if os.path.exists(f):
                    self.new_tab(f)
        if self.notebook.get_n_pages() == 0:
            self.new_tab()

    def new_tab(self, filepath=None):
        tab_content = CrosspadTab(filepath)
        tab_content.buffer.connect("notify::cursor-position", self.update_status)

        # Custom Tab Label with Close button
        tab_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        label = Gtk.Label(label=tab_content.filename)
        tab_box.pack_start(label, True, True, 0)

        close_btn = Gtk.Button(label="×")
        close_btn.get_style_context().add_class("flat-btn")
        close_btn.connect("clicked", lambda b: self.close_tab(tab_content))
        tab_box.pack_start(close_btn, False, False, 0)
        tab_box.show_all()

        page_num = self.notebook.append_page(tab_content, tab_box)
        self.notebook.show_all()
        self.notebook.set_current_page(page_num)

    def close_tab(self, tab_content):
        page_num = self.notebook.page_num(tab_content)
        if page_num != -1:
            self.notebook.remove_page(page_num)
        if self.notebook.get_n_pages() == 0:
            self.new_tab()

    def get_current_tab(self):
        page_num = self.notebook.get_current_page()
        if page_num != -1:
            return self.notebook.get_nth_page(page_num)
        return None

    def on_switch_page(self, notebook, page, page_num):
        self.update_status()

    def update_status(self, *args):
        tab = self.get_current_tab()
        if not tab:
            return
        buf = tab.buffer
        insert_iter = buf.get_iter_at_mark(buf.get_insert())
        line = insert_iter.get_line() + 1
        col = insert_iter.get_line_offset() + 1
        chars = buf.get_char_count()
        self.pos_lbl.set_text(f"Ln {line}, Col {col}")
        self.char_lbl.set_text(f"{chars} characters")
        self.header.props.subtitle = tab.filepath if tab.filepath else "Untitled"

    def open_file_dialog(self):
        dlg = Gtk.FileChooserDialog(
            title="Open File",
            parent=self,
            action=Gtk.FileChooserAction.OPEN
        )
        dlg.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dlg.add_button("Open", Gtk.ResponseType.ACCEPT)
        if dlg.run() == Gtk.ResponseType.ACCEPT:
            path = dlg.get_filename()
            dlg.destroy()
            if path:
                self.new_tab(path)
        else:
            dlg.destroy()

    def save_current_tab(self):
        tab = self.get_current_tab()
        if not tab:
            return
        if not tab.filepath:
            dlg = Gtk.FileChooserDialog(
                title="Save As",
                parent=self,
                action=Gtk.FileChooserAction.SAVE
            )
            dlg.add_button("Cancel", Gtk.ResponseType.CANCEL)
            dlg.add_button("Save", Gtk.ResponseType.ACCEPT)
            dlg.set_do_overwrite_confirmation(True)
            if dlg.run() == Gtk.ResponseType.ACCEPT:
                tab.filepath = dlg.get_filename()
                tab.filename = os.path.basename(tab.filepath)
                dlg.destroy()
            else:
                dlg.destroy()
                return

        if tab.filepath:
            try:
                buf = tab.buffer
                start_iter = buf.get_start_iter()
                end_iter = buf.get_end_iter()
                text = buf.get_text(start_iter, end_iter, True)
                with open(tab.filepath, "w", encoding="utf-8") as f:
                    f.write(text)
                tab.is_modified = False
                self.update_status()
            except Exception as e:
                err_dlg = Gtk.MessageDialog(
                    parent=self,
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text=f"Error saving file: {e}"
                )
                err_dlg.run()
                err_dlg.destroy()

    def show_find_dialog(self):
        dlg = Gtk.Dialog(title="Find Text", parent=self, flags=0)
        dlg.add_button("Cancel", Gtk.ResponseType.CANCEL)
        find_btn = dlg.add_button("Find Next", Gtk.ResponseType.OK)
        find_btn.get_style_context().add_class("accent-btn")

        content = dlg.get_content_area()
        content.set_spacing(12)
        content.set_margin_start(16)
        content.set_margin_end(16)
        content.set_margin_top(16)
        content.set_margin_bottom(16)

        entry = Gtk.SearchEntry()
        entry.set_placeholder_text("Search query...")
        content.add(entry)
        dlg.show_all()

        if dlg.run() == Gtk.ResponseType.OK:
            query = entry.get_text()
            tab = self.get_current_tab()
            if tab and query:
                buf = tab.buffer
                insert = buf.get_iter_at_mark(buf.get_insert())
                match = insert.forward_search(query, Gtk.TextSearchFlags.CASE_INSENSITIVE, None)
                if match:
                    match_start, match_end = match
                    buf.select_range(match_start, match_end)
                    tab.textview.scroll_to_iter(match_start, 0.1, False, 0, 0)
        dlg.destroy()

def main():
    if not HAS_GTK:
        print("[Crosspad Error] PyGObject (Gtk 3) is required.")
        sys.exit(1)

    GLib.set_prgname("crosspad")
    GLib.set_application_name("Crosspad")

    app = CrosspadApp(sys.argv[1:])
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
