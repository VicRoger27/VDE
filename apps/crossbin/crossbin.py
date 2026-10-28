#!/usr/bin/env python3
"""
Cross Bin — VDE Fluent Recycle Bin
Modern Dark Mica Trash & File Recovery Manager for Victorious Desktop Environment
"""

import os
import sys
import shutil
import urllib.parse
from datetime import datetime

try:
    import gi
    gi.require_version('Gtk', '3.0')
    from gi.repository import Gtk, Gdk, GLib
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

.command-bar {
    background-color: #1c1c1f;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    padding: 8px 14px;
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

button.cmd-btn {
    background: transparent;
    border: none;
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 13px;
    color: #e4e4e7;
}

button.cmd-btn:hover {
    background: rgba(255, 255, 255, 0.08);
    color: #ffffff;
}

button.danger-btn {
    background: rgba(239, 68, 68, 0.15);
    border: 1px solid rgba(239, 68, 68, 0.4);
    border-radius: 4px;
    padding: 6px 14px;
    font-size: 13px;
    color: #f87171;
    font-weight: 600;
}

button.danger-btn:hover {
    background: rgba(239, 68, 68, 0.25);
}

.statusbar {
    background-color: #121214;
    border-top: 1px solid rgba(255, 255, 255, 0.08);
    padding: 6px 16px;
    font-size: 11px;
    color: #a1a1aa;
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

def format_size(bytes_num):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_num < 1024.0:
            return f"{bytes_num:.1f} {unit}" if unit != 'B' else f"{bytes_num} B"
        bytes_num /= 1024.0
    return f"{bytes_num:.1f} TB"

class CrossBinApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Recycle Bin")
        self.set_icon_name("crossbin")
        Gtk.Window.set_default_icon_name("crossbin")
        self.set_default_size(880, 520)
        self.set_position(Gtk.WindowPosition.CENTER)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(CSS_STYLE)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.trash_files_dir = os.path.expanduser("~/.local/share/Trash/files")
        self.trash_info_dir = os.path.expanduser("~/.local/share/Trash/info")
        os.makedirs(self.trash_files_dir, exist_ok=True)
        os.makedirs(self.trash_info_dir, exist_ok=True)

        # HeaderBar
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.set_decoration_layout(":minimize,maximize,close")
        header.props.title = "Recycle Bin"
        header.props.subtitle = "Cross Bin"
        self.set_titlebar(header)

        # Main Layout
        root_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(root_box)

        # Command Bar
        cmd_bar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=8)
        cmd_bar.get_style_context().add_class("command-bar")
        root_box.pack_start(cmd_bar, False, False, 0)

        restore_btn = Gtk.Button(label="♻ Restore Selected")
        restore_btn.get_style_context().add_class("cmd-btn")
        restore_btn.connect("clicked", lambda b: self.restore_selected())
        cmd_bar.pack_start(restore_btn, False, False, 0)

        del_btn = Gtk.Button(label="❌ Delete Permanently")
        del_btn.get_style_context().add_class("cmd-btn")
        del_btn.connect("clicked", lambda b: self.delete_permanent())
        cmd_bar.pack_start(del_btn, False, False, 0)

        empty_btn = Gtk.Button(label="🗑 Empty Recycle Bin")
        empty_btn.get_style_context().add_class("danger-btn")
        empty_btn.connect("clicked", lambda b: self.empty_bin())
        cmd_bar.pack_end(empty_btn, False, False, 0)

        refresh_btn = Gtk.Button(label="↻")
        refresh_btn.get_style_context().add_class("cmd-btn")
        refresh_btn.connect("clicked", lambda b: self.load_trash())
        cmd_bar.pack_end(refresh_btn, False, False, 0)

        # Scrolled Table
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        root_box.pack_start(scrolled, True, True, 0)

        # Store: [icon_name, name, original_path, delete_date, size_str, actual_file_path]
        self.store = Gtk.ListStore(str, str, str, str, str, str)
        self.treeview = Gtk.TreeView(model=self.store)
        self.treeview.set_rules_hint(True)
        scrolled.add(self.treeview)

        # Name Col
        col_name = Gtk.TreeViewColumn("Name")
        cell_icon = Gtk.CellRendererPixbuf()
        cell_name = Gtk.CellRendererText()
        col_name.pack_start(cell_icon, False)
        col_name.pack_start(cell_name, True)
        col_name.add_attribute(cell_icon, "icon-name", 0)
        col_name.add_attribute(cell_name, "text", 1)
        col_name.set_sort_column_id(1)
        col_name.set_min_width(220)
        self.treeview.append_column(col_name)

        # Original Location
        col_loc = Gtk.TreeViewColumn("Original Location", Gtk.CellRendererText(), text=2)
        col_loc.set_sort_column_id(2)
        col_loc.set_min_width(260)
        self.treeview.append_column(col_loc)

        # Date Deleted
        col_date = Gtk.TreeViewColumn("Date Deleted", Gtk.CellRendererText(), text=3)
        col_date.set_sort_column_id(3)
        col_date.set_min_width(160)
        self.treeview.append_column(col_date)

        # Size
        col_size = Gtk.TreeViewColumn("Size", Gtk.CellRendererText(), text=4)
        col_size.set_sort_column_id(4)
        col_size.set_min_width(90)
        self.treeview.append_column(col_size)

        # Status Bar
        self.statusbar = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        self.statusbar.get_style_context().add_class("statusbar")
        root_box.pack_start(self.statusbar, False, False, 0)

        self.status_lbl = Gtk.Label(label="0 items", xalign=0)
        self.statusbar.pack_start(self.status_lbl, True, True, 0)

        self.load_trash()

    def parse_trashinfo(self, info_file):
        orig_path = "Unknown"
        del_date = "Unknown"
        try:
            with open(info_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.startswith("Path="):
                        orig_path = urllib.parse.unquote(line.split("Path=", 1)[1].strip())
                    elif line.startswith("DeletionDate="):
                        del_date = line.split("DeletionDate=", 1)[1].strip().replace("T", " ")
        except Exception:
            pass
        return orig_path, del_date

    def load_trash(self):
        self.store.clear()
        total_items = 0
        total_size = 0

        if os.path.exists(self.trash_files_dir):
            for filename in os.listdir(self.trash_files_dir):
                file_path = os.path.join(self.trash_files_dir, filename)
                info_path = os.path.join(self.trash_info_dir, filename + ".trashinfo")

                orig_loc, del_date = self.parse_trashinfo(info_path)
                try:
                    stat = os.stat(file_path)
                    sz = stat.st_size
                    total_size += sz
                    size_str = format_size(sz)
                except Exception:
                    size_str = "Unknown"

                icon_name = "folder" if os.path.isdir(file_path) else "text-x-generic"
                self.store.append([icon_name, filename, orig_loc, del_date, size_str, file_path])
                total_items += 1

        self.status_lbl.set_text(f"{total_items} items in Recycle Bin ({format_size(total_size)})")

    def get_selected(self):
        selection = self.treeview.get_selection()
        model, iter = selection.get_selected()
        if iter:
            return model[iter][1], model[iter][2], model[iter][5] # name, orig_loc, actual_file
        return None, None, None

    def restore_selected(self):
        name, orig_loc, actual_file = self.get_selected()
        if not actual_file or not os.path.exists(actual_file):
            return
        dest = orig_loc if orig_loc and orig_loc != "Unknown" else os.path.expanduser(f"~/Desktop/{name}")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        try:
            shutil.move(actual_file, dest)
            info_file = os.path.join(self.trash_info_dir, name + ".trashinfo")
            if os.path.exists(info_file):
                os.remove(info_file)
            self.load_trash()
        except Exception as e:
            err = Gtk.MessageDialog(parent=self, message_type=Gtk.MessageType.ERROR, buttons=Gtk.ButtonsType.OK, text=f"Error restoring: {e}")
            err.run()
            err.destroy()

    def delete_permanent(self):
        name, orig_loc, actual_file = self.get_selected()
        if not actual_file:
            return
        dlg = Gtk.MessageDialog(
            parent=self,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text=f"Permanently delete '{name}'? This cannot be undone."
        )
        if dlg.run() == Gtk.ResponseType.YES:
            if os.path.isdir(actual_file):
                shutil.rmtree(actual_file, ignore_errors=True)
            else:
                os.remove(actual_file)
            info_file = os.path.join(self.trash_info_dir, name + ".trashinfo")
            if os.path.exists(info_file):
                os.remove(info_file)
            self.load_trash()
        dlg.destroy()

    def empty_bin(self):
        dlg = Gtk.MessageDialog(
            parent=self,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.YES_NO,
            text="Are you sure you want to permanently delete all items in Recycle Bin?"
        )
        if dlg.run() == Gtk.ResponseType.YES:
            for f in os.listdir(self.trash_files_dir):
                fp = os.path.join(self.trash_files_dir, f)
                if os.path.isdir(fp):
                    shutil.rmtree(fp, ignore_errors=True)
                else:
                    os.remove(fp)
            for f in os.listdir(self.trash_info_dir):
                os.remove(os.path.join(self.trash_info_dir, f))
            self.load_trash()
        dlg.destroy()

def main():
    if not HAS_GTK:
        print("[Cross Bin Error] PyGObject is required.")
        sys.exit(1)

    GLib.set_prgname("crossbin")
    GLib.set_application_name("Recycle Bin")

    app = CrossBinApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
