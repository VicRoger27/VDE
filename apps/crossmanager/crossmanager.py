#!/usr/bin/env python3
"""
Crossmanager — VDE Fluent File Explorer
1-to-1 Windows 11 Fluent Dark Mica File Manager for Victorious Desktop Environment
"""

import os
import sys
import shutil
import subprocess
import time
from datetime import datetime

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

.command-bar {
    background-color: #1c1c1f;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    padding: 6px 12px;
}

.address-bar-box {
    background-color: #121214;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    padding: 8px 12px;
}

entry.path-entry {
    background-color: #27272a;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 6px;
    padding: 6px 12px;
    font-size: 13px;
    color: #ffffff;
}

entry.path-entry:focus {
    border-color: #38bdf8;
}

.sidebar {
    background-color: #121214;
    border-right: 1px solid rgba(255, 255, 255, 0.06);
    padding: 8px 4px;
}

.sidebar row {
    padding: 8px 12px;
    border-radius: 6px;
    color: #e4e4e7;
    font-size: 13px;
    margin: 2px 6px;
}

.sidebar row:hover {
    background-color: rgba(255, 255, 255, 0.06);
}

.sidebar row:selected {
    background-color: rgba(56, 189, 248, 0.15);
    color: #38bdf8;
    font-weight: 600;
}

treeview {
    background-color: #18181b;
    color: #f4f4f5;
    font-size: 13px;
}

treeview:selected {
    background-color: rgba(56, 189, 248, 0.2);
    color: #ffffff;
}

treeview header button {
    background-color: #1c1c1f;
    border-bottom: 1px solid rgba(255, 255, 255, 0.08);
    color: #a1a1aa;
    font-weight: 600;
    font-size: 12px;
    padding: 4px 8px;
}

.statusbar {
    background-color: #121214;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding: 6px 16px;
    font-size: 11px;
    color: #a1a1aa;
}

button.cmd-btn {
    background: transparent;
    border: none;
    border-radius: 4px;
    padding: 5px 10px;
    font-size: 12px;
    color: #e4e4e7;
}

button.cmd-btn:hover {
    background: rgba(255, 255, 255, 0.08);
    color: #ffffff;
}
"""

def format_size(bytes_num):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:.1f} {unit}" if unit != 'B' else f"{bytes_num} B"
        bytes_num /= 1024.0
    return f"{bytes_num:.1f} PB"

class CrossmanagerApp(Gtk.Window):
    def __init__(self, start_dir=None):
        super().__init__(title="File Explorer")
        self.set_icon_name("crossmanager")
        Gtk.Window.set_default_icon_name("crossmanager")
        self.set_default_size(1040, 660)
        self.set_position(Gtk.WindowPosition.CENTER)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(CSS_STYLE)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.current_path = os.path.abspath(start_dir) if start_dir and os.path.exists(start_dir) else os.path.expanduser("~")
        self.history = [self.current_path]
        self.history_idx = 0
        self.show_hidden = False
        self.clipboard_file = None
        self.clipboard_action = None # 'copy' or 'cut'

        # HeaderBar
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.set_decoration_layout(":minimize,maximize,close")
        self.header.props.title = "File Explorer"
        self.header.props.subtitle = self.current_path
        self.set_titlebar(self.header)

        # Main Layout
        root_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(root_box)

        # 1. Command Bar (Ribbon)
        cmd_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        cmd_bar.get_style_context().add_class("command-bar")
        root_box.pack_start(cmd_bar, False, False, 0)

        new_folder_btn = Gtk.Button(label="📁 New Folder")
        new_folder_btn.get_style_context().add_class("cmd-btn")
        new_folder_btn.connect("clicked", lambda b: self.create_new_folder())
        cmd_bar.pack_start(new_folder_btn, False, False, 0)

        cut_btn = Gtk.Button(label="✂ Cut")
        cut_btn.get_style_context().add_class("cmd-btn")
        cut_btn.connect("clicked", lambda b: self.cut_selected())
        cmd_bar.pack_start(cut_btn, False, False, 0)

        copy_btn = Gtk.Button(label="📋 Copy")
        copy_btn.get_style_context().add_class("cmd-btn")
        copy_btn.connect("clicked", lambda b: self.copy_selected())
        cmd_bar.pack_start(copy_btn, False, False, 0)

        self.paste_btn = Gtk.Button(label="📥 Paste")
        self.paste_btn.get_style_context().add_class("cmd-btn")
        self.paste_btn.connect("clicked", lambda b: self.paste_file())
        cmd_bar.pack_start(self.paste_btn, False, False, 0)

        rename_btn = Gtk.Button(label="✏ Rename")
        rename_btn.get_style_context().add_class("cmd-btn")
        rename_btn.connect("clicked", lambda b: self.rename_selected())
        cmd_bar.pack_start(rename_btn, False, False, 0)

        del_btn = Gtk.Button(label="🗑 Delete")
        del_btn.get_style_context().add_class("cmd-btn")
        del_btn.connect("clicked", lambda b: self.delete_selected())
        cmd_bar.pack_start(del_btn, False, False, 0)

        hidden_btn = Gtk.Button(label="👁 Hidden Files")
        hidden_btn.get_style_context().add_class("cmd-btn")
        hidden_btn.connect("clicked", lambda b: self.toggle_hidden())
        cmd_bar.pack_end(hidden_btn, False, False, 0)

        # 2. Address & Navigation Bar
        addr_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        addr_bar.get_style_context().add_class("address-bar-box")
        root_box.pack_start(addr_bar, False, False, 0)

        self.back_btn = Gtk.Button(label="◀")
        self.back_btn.get_style_context().add_class("cmd-btn")
        self.back_btn.connect("clicked", lambda b: self.go_back())
        addr_bar.pack_start(self.back_btn, False, False, 0)

        self.fwd_btn = Gtk.Button(label="▶")
        self.fwd_btn.get_style_context().add_class("cmd-btn")
        self.fwd_btn.connect("clicked", lambda b: self.go_forward())
        addr_bar.pack_start(self.fwd_btn, False, False, 0)

        up_btn = Gtk.Button(label="▲")
        up_btn.get_style_context().add_class("cmd-btn")
        up_btn.connect("clicked", lambda b: self.go_up())
        addr_bar.pack_start(up_btn, False, False, 0)

        refresh_btn = Gtk.Button(label="↻")
        refresh_btn.get_style_context().add_class("cmd-btn")
        refresh_btn.connect("clicked", lambda b: self.load_directory(self.current_path))
        addr_bar.pack_start(refresh_btn, False, False, 0)

        # Path Entry
        self.path_entry = Gtk.Entry()
        self.path_entry.get_style_context().add_class("path-entry")
        self.path_entry.connect("activate", self.on_path_entered)
        addr_bar.pack_start(self.path_entry, True, True, 4)

        # Search Entry
        self.search_entry = Gtk.SearchEntry()
        self.search_entry.set_placeholder_text("Search...")
        self.search_entry.connect("search-changed", self.on_search_changed)
        addr_bar.pack_end(self.search_entry, False, False, 0)

        # 3. Main Paned Layout: Left Sidebar + File List
        hpaned = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        root_box.pack_start(hpaned, True, True, 0)

        # Left Sidebar (Quick Access)
        sidebar_scrolled = Gtk.ScrolledWindow()
        sidebar_scrolled.set_size_request(200, -1)
        sidebar_scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        sidebar_scrolled.get_style_context().add_class("sidebar")
        hpaned.pack_start(sidebar_scrolled, False, False, 0)

        self.sidebar_list = Gtk.ListBox()
        self.sidebar_list.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.sidebar_list.connect("row-selected", self.on_sidebar_select)
        sidebar_scrolled.add(self.sidebar_list)

        quick_places = [
            ("🏠 Home", os.path.expanduser("~")),
            ("🖥️ Desktop", os.path.expanduser("~/Desktop")),
            ("📥 Downloads", os.path.expanduser("~/Downloads")),
            ("📄 Documents", os.path.expanduser("~/Documents")),
            ("🖼️ Pictures", os.path.expanduser("~/Pictures")),
            ("🎵 Music", os.path.expanduser("~/Music")),
            ("🎬 Videos", os.path.expanduser("~/Videos")),
            ("💻 Root Filesystem", "/"),
            ("🗑️ Trash", os.path.expanduser("~/.local/share/Trash/files"))
        ]

        for name, path in quick_places:
            row = Gtk.ListBoxRow()
            lbl = Gtk.Label(label=name, xalign=0)
            row.add(lbl)
            row.target_path = path
            self.sidebar_list.add(row)

        # Right File List TreeView
        file_scrolled = Gtk.ScrolledWindow()
        file_scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        hpaned.pack_start(file_scrolled, True, True, 0)

        # Model: [icon_name, name, date_str, type_str, size_str, is_dir, full_path]
        self.store = Gtk.ListStore(str, str, str, str, str, bool, str)
        self.filter_model = self.store.filter_new()
        self.filter_model.set_visible_func(self.filter_func)

        self.treeview = Gtk.TreeView(model=self.filter_model)
        self.treeview.set_rules_hint(True)
        self.treeview.connect("row-activated", self.on_row_activated)
        self.treeview.connect("button-press-event", self.on_tree_button_press)
        file_scrolled.add(self.treeview)

        # Columns
        # 1. Name Column (Icon + Text)
        name_col = Gtk.TreeViewColumn("Name")
        icon_cell = Gtk.CellRendererPixbuf()
        name_cell = Gtk.CellRendererText()
        name_col.pack_start(icon_cell, False)
        name_col.pack_start(name_cell, True)
        name_col.add_attribute(icon_cell, "icon-name", 0)
        name_col.add_attribute(name_cell, "text", 1)
        name_col.set_sort_column_id(1)
        name_col.set_resizable(True)
        name_col.set_min_width(280)
        self.treeview.append_column(name_col)

        # 2. Date Modified Column
        date_col = Gtk.TreeViewColumn("Date modified", Gtk.CellRendererText(), text=2)
        date_col.set_sort_column_id(2)
        date_col.set_resizable(True)
        date_col.set_min_width(160)
        self.treeview.append_column(date_col)

        # 3. Type Column
        type_col = Gtk.TreeViewColumn("Type", Gtk.CellRendererText(), text=3)
        type_col.set_sort_column_id(3)
        type_col.set_resizable(True)
        type_col.set_min_width(120)
        self.treeview.append_column(type_col)

        # 4. Size Column
        size_col = Gtk.TreeViewColumn("Size", Gtk.CellRendererText(), text=4)
        size_col.set_sort_column_id(4)
        size_col.set_resizable(True)
        size_col.set_min_width(100)
        self.treeview.append_column(size_col)

        # 4. Status Bar
        self.statusbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        self.statusbar.get_style_context().add_class("statusbar")
        root_box.pack_start(self.statusbar, False, False, 0)

        self.status_items_lbl = Gtk.Label(label="0 items", xalign=0)
        self.statusbar.pack_start(self.status_items_lbl, False, False, 0)

        self.status_selected_lbl = Gtk.Label(label="", xalign=0)
        self.statusbar.pack_start(self.status_selected_lbl, True, True, 0)

        # Keybindings
        self.connect("key-press-event", self.on_key_press)

        # Initial load
        self.load_directory(self.current_path)

    def load_directory(self, target_path):
        if not os.path.exists(target_path) or not os.path.isdir(target_path):
            return
        self.current_path = os.path.abspath(target_path)
        self.path_entry.set_text(self.current_path)
        self.header.props.subtitle = self.current_path

        self.store.clear()
        total_items = 0

        try:
            entries = os.listdir(self.current_path)
            for entry in sorted(entries, key=lambda s: s.lower()):
                if not self.show_hidden and entry.startswith('.'):
                    continue
                full_path = os.path.join(self.current_path, entry)
                is_dir = os.path.isdir(full_path)

                try:
                    stat = os.stat(full_path)
                    mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%m/%d/%Y %I:%M %p")
                    size_str = format_size(stat.st_size) if not is_dir else ""
                except Exception:
                    mod_time = "Unknown"
                    size_str = ""

                if is_dir:
                    icon_name = "folder"
                    type_str = "File folder"
                else:
                    ext = os.path.splitext(entry)[1].lower()
                    icon_name = "text-x-generic"
                    if ext in ('.png', '.jpg', '.jpeg', '.webp', '.svg'):
                        icon_name = "image-x-generic"
                        type_str = "Image"
                    elif ext in ('.mp4', '.mkv', '.avi', '.mov'):
                        icon_name = "video-x-generic"
                        type_str = "Video"
                    elif ext in ('.mp3', '.flac', '.wav', '.ogg'):
                        icon_name = "audio-x-generic"
                        type_str = "Audio"
                    elif ext in ('.zip', '.tar', '.gz', '.xz', '.7z'):
                        icon_name = "package-x-generic"
                        type_str = "Archive"
                    elif ext in ('.py', '.sh', '.c', '.cpp', '.rs', '.js', '.ts'):
                        icon_name = "text-x-script"
                        type_str = "Script"
                    else:
                        type_str = f"{ext[1:].upper()} File" if ext else "File"

                self.store.append([icon_name, entry, mod_time, type_str, size_str, is_dir, full_path])
                total_items += 1
        except PermissionError:
            self.status_items_lbl.set_text("Access Denied")
            return

        self.status_items_lbl.set_text(f"{total_items} items")
        self.back_btn.set_sensitive(self.history_idx > 0)
        self.fwd_btn.set_sensitive(self.history_idx < len(self.history) - 1)

    def navigate_to(self, path):
        if os.path.exists(path) and os.path.isdir(path):
            if self.history_idx < len(self.history) - 1:
                self.history = self.history[:self.history_idx + 1]
            self.history.append(path)
            self.history_idx += 1
            self.load_directory(path)

    def go_back(self):
        if self.history_idx > 0:
            self.history_idx -= 1
            self.load_directory(self.history[self.history_idx])

    def go_forward(self):
        if self.history_idx < len(self.history) - 1:
            self.history_idx += 1
            self.load_directory(self.history[self.history_idx])

    def go_up(self):
        parent = os.path.dirname(self.current_path)
        if parent and parent != self.current_path:
            self.navigate_to(parent)

    def on_path_entered(self, entry):
        target = entry.get_text().strip()
        if os.path.exists(target) and os.path.isdir(target):
            self.navigate_to(target)
        else:
            entry.set_text(self.current_path)

    def on_search_changed(self, entry):
        self.filter_model.refilter()

    def filter_func(self, model, iter, data):
        query = self.search_entry.get_text().strip().lower()
        if not query:
            return True
        name = model[iter][1].lower()
        return query in name

    def on_sidebar_select(self, listbox, row):
        if row and hasattr(row, 'target_path'):
            self.navigate_to(row.target_path)

    def on_row_activated(self, treeview, path, column):
        iter = self.filter_model.get_iter(path)
        is_dir = self.filter_model[iter][5]
        full_path = self.filter_model[iter][6]
        if is_dir:
            self.navigate_to(full_path)
        else:
            # Open file with default application
            subprocess.Popen(["xdg-open", full_path])

    def get_selected_path(self):
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            return model[iter][6]
        return None

    def create_new_folder(self):
        dlg = Gtk.Dialog(title="New Folder", parent=self, flags=0)
        dlg.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dlg.add_button("Create", Gtk.ResponseType.OK)
        box = dlg.get_content_area()
        box.set_spacing(10)
        box.set_margin_start(16)
        box.set_margin_end(16)
        box.set_margin_top(16)
        box.set_margin_bottom(16)
        entry = Gtk.Entry()
        entry.set_text("New folder")
        box.add(entry)
        dlg.show_all()
        if dlg.run() == Gtk.ResponseType.OK:
            name = entry.get_text().strip()
            if name:
                new_dir = os.path.join(self.current_path, name)
                os.makedirs(new_dir, exist_ok=True)
                self.load_directory(self.current_path)
        dlg.destroy()

    def cut_selected(self):
        p = self.get_selected_path()
        if p:
            self.clipboard_file = p
            self.clipboard_action = 'cut'

    def copy_selected(self):
        p = self.get_selected_path()
        if p:
            self.clipboard_file = p
            self.clipboard_action = 'copy'

    def paste_file(self):
        if not self.clipboard_file or not os.path.exists(self.clipboard_file):
            return
        dest = os.path.join(self.current_path, os.path.basename(self.clipboard_file))
        try:
            if self.clipboard_action == 'cut':
                shutil.move(self.clipboard_file, dest)
                self.clipboard_file = None
            elif self.clipboard_action == 'copy':
                if os.path.isdir(self.clipboard_file):
                    shutil.copytree(self.clipboard_file, dest)
                else:
                    shutil.copy2(self.clipboard_file, dest)
            self.load_directory(self.current_path)
        except Exception as e:
            err = Gtk.MessageDialog(parent=self, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, text=f"Error pasting: {e}")
            err.run()
            err.destroy()

    def rename_selected(self):
        p = self.get_selected_path()
        if not p:
            return
        old_name = os.path.basename(p)
        dlg = Gtk.Dialog(title="Rename", parent=self, flags=0)
        dlg.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dlg.add_button("Rename", Gtk.ResponseType.OK)
        box = dlg.get_content_area()
        box.set_spacing(10)
        box.set_margin_start(16)
        box.set_margin_end(16)
        box.set_margin_top(16)
        box.set_margin_bottom(16)
        entry = Gtk.Entry()
        entry.set_text(old_name)
        box.add(entry)
        dlg.show_all()
        if dlg.run() == Gtk.ResponseType.OK:
            new_name = entry.get_text().strip()
            if new_name and new_name != old_name:
                new_path = os.path.join(os.path.dirname(p), new_name)
                os.rename(p, new_path)
                self.load_directory(self.current_path)
        dlg.destroy()

    def delete_selected(self):
        p = self.get_selected_path()
        if not p:
            return
        dlg = Gtk.MessageDialog(
            parent=self,
            message_type=Gtk.MessageType.QUESTION,
            buttons=Gtk.ButtonsType.YES_NO,
            text=f"Are you sure you want to move '{os.path.basename(p)}' to Trash?"
        )
        if dlg.run() == Gtk.ResponseType.YES:
            # Move to Trash
            trash_dir = os.path.expanduser("~/.local/share/Trash/files")
            os.makedirs(trash_dir, exist_ok=True)
            shutil.move(p, os.path.join(trash_dir, os.path.basename(p)))
            self.load_directory(self.current_path)
        dlg.destroy()

    def toggle_hidden(self):
        self.show_hidden = not self.show_hidden
        self.load_directory(self.current_path)

    def on_tree_button_press(self, treeview, event):
        if event.button == 3: # Right click context menu
            menu = Gtk.Menu()
            open_item = Gtk.MenuItem(label="Open")
            open_item.connect("activate", lambda i: self.on_row_activated(treeview, treeview.get_cursor()[0], None))
            menu.append(open_item)

            menu.append(Gtk.SeparatorMenuItem())

            cut_item = Gtk.MenuItem(label="Cut")
            cut_item.connect("activate", lambda i: self.cut_selected())
            menu.append(cut_item)

            copy_item = Gtk.MenuItem(label="Copy")
            copy_item.connect("activate", lambda i: self.copy_selected())
            menu.append(copy_item)

            paste_item = Gtk.MenuItem(label="Paste")
            paste_item.connect("activate", lambda i: self.paste_file())
            menu.append(paste_item)

            rename_item = Gtk.MenuItem(label="Rename")
            rename_item.connect("activate", lambda i: self.rename_selected())
            menu.append(rename_item)

            del_item = Gtk.MenuItem(label="Delete")
            del_item.connect("activate", lambda i: self.delete_selected())
            menu.append(del_item)

            menu.show_all()
            menu.popup_at_pointer(event)
            return True
        return False

    def on_key_press(self, widget, event):
        if event.keyval == Gdk.KEY_BackSpace:
            self.go_up()
            return True
        elif event.keyval == Gdk.KEY_F5:
            self.load_directory(self.current_path)
            return True
        elif event.keyval == Gdk.KEY_F2:
            self.rename_selected()
            return True
        elif event.keyval == Gdk.KEY_Delete:
            self.delete_selected()
            return True
        elif (event.state & Gdk.ModifierType.CONTROL_MASK) and event.keyval in (Gdk.KEY_h, Gdk.KEY_H):
            self.toggle_hidden()
            return True
        return False

def main():
    if not HAS_GTK:
        print("[Crossmanager Error] PyGObject is required.")
        sys.exit(1)

    GLib.set_prgname("crossmanager")
    GLib.set_application_name("File Explorer")

    initial_dir = sys.argv[1] if len(sys.argv) > 1 else None
    app = CrossmanagerApp(initial_dir)
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
