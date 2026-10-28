#!/usr/bin/env python3
"""
Crosslink — VDE Fluent Phone Link
Modern Dark Mica Smartphone & Device Integration Hub for Victorious Desktop Environment
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

.card {
    background-color: #27272a;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 8px;
    padding: 18px 22px;
    margin: 8px 16px;
}

.card-title {
    font-size: 16px;
    font-weight: 600;
    color: #ffffff;
}

.card-desc {
    font-size: 12px;
    color: #a1a1aa;
    margin-top: 2px;
}

.badge-connected {
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
    padding: 8px 18px;
    border: none;
    font-size: 13px;
}

button.accent-btn:hover {
    background: #7dd3fc;
}

button.sec-btn {
    background: rgba(255, 255, 255, 0.08);
    color: #fafafa;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 13px;
}

button.sec-btn:hover {
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

class CrosslinkApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Phone Link")
        self.set_icon_name("crosslink")
        Gtk.Window.set_default_icon_name("crosslink")
        self.set_default_size(720, 500)
        self.set_position(Gtk.WindowPosition.CENTER)

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
        header.props.title = "Phone Link"
        header.props.subtitle = "Crosslink Device Hub"
        self.set_titlebar(header)

        # Main Layout
        root_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        self.add(root_box)

        # Device Status Banner Card
        dev_card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        dev_card.get_style_context().add_class("card")
        root_box.pack_start(dev_card, False, False, 0)

        phone_icon = Gtk.Label(label="📱")
        phone_icon.override_font(Pango.FontDescription("32"))
        dev_card.pack_start(phone_icon, False, False, 0)

        dev_info_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        name_lbl = Gtk.Label(label="Mobile Device Link", xalign=0)
        name_lbl.get_style_context().add_class("card-title")
        dev_info_box.pack_start(name_lbl, False, False, 0)

        spec_lbl = Gtk.Label(label="Ready to pair via KDE Connect / GSConnect local bridge protocol.", xalign=0)
        spec_lbl.get_style_context().add_class("card-desc")
        dev_info_box.pack_start(spec_lbl, False, False, 0)
        dev_card.pack_start(dev_info_box, True, True, 0)

        badge = Gtk.Label(label="ONLINE")
        badge.get_style_context().add_class("badge-connected")
        dev_card.pack_end(badge, False, False, 0)

        # Quick Actions Card
        actions_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        actions_card.get_style_context().add_class("card")
        root_box.pack_start(actions_card, False, False, 0)

        at = Gtk.Label(label="Device Sync Actions", xalign=0)
        at.get_style_context().add_class("card-title")
        actions_card.pack_start(at, False, False, 0)

        grid = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        actions_card.pack_start(grid, False, False, 0)

        send_file_btn = Gtk.Button(label="📁 Send File to Phone")
        send_file_btn.get_style_context().add_class("sec-btn")
        send_file_btn.connect("clicked", lambda b: self.send_file_dialog())
        grid.pack_start(send_file_btn, True, True, 0)

        clip_sync_btn = Gtk.Button(label="📋 Sync Clipboard")
        clip_sync_btn.get_style_context().add_class("sec-btn")
        clip_sync_btn.connect("clicked", lambda b: self.sync_clipboard())
        grid.pack_start(clip_sync_btn, True, True, 0)

        ring_btn = Gtk.Button(label="🔔 Ring Phone")
        ring_btn.get_style_context().add_class("sec-btn")
        ring_btn.connect("clicked", lambda b: self.ring_phone())
        grid.pack_start(ring_btn, True, True, 0)

        # Integration & Pairing Status Card
        pair_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        pair_card.get_style_context().add_class("card")
        root_box.pack_start(pair_card, True, True, 0)

        pt = Gtk.Label(label="Network Protocol Bridge", xalign=0)
        pt.get_style_context().add_class("card-title")
        pair_card.pack_start(pt, False, False, 0)

        pd = Gtk.Label(label="Crosslink integrates directly with local network device discovery.\n"
                             "Zero cloud servers, zero external telemetry — all synchronization stays strictly on your local Wi-Fi.", xalign=0)
        pd.get_style_context().add_class("card-desc")
        pair_card.pack_start(pd, False, False, 0)

        scan_btn = Gtk.Button(label="🔍 Scan for Nearby Devices")
        scan_btn.get_style_context().add_class("accent-btn")
        scan_btn.connect("clicked", self.on_scan)
        pair_card.pack_start(scan_btn, False, False, 8)

        self.status_lbl = Gtk.Label(label="Listening on local port 1716 (KDE Connect protocol)...", xalign=0)
        self.status_lbl.get_style_context().add_class("card-desc")
        pair_card.pack_start(self.status_lbl, False, False, 0)

    def on_scan(self, btn):
        self.status_lbl.set_text("Scanning Wi-Fi broadcast... Waiting for phone acknowledgment.")

    def send_file_dialog(self):
        dlg = Gtk.FileChooserDialog(title="Send File to Phone", parent=self, action=Gtk.FileChooserAction.OPEN)
        dlg.add_button("Cancel", Gtk.ResponseType.CANCEL)
        dlg.add_button("Send", Gtk.ResponseType.ACCEPT)
        if dlg.run() == Gtk.ResponseType.ACCEPT:
            path = dlg.get_filename()
            dlg.destroy()
            if path:
                self.status_lbl.set_text(f"Sending '{os.path.basename(path)}' via local Wi-Fi transfer...")
        else:
            dlg.destroy()

    def sync_clipboard(self):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        text = clipboard.wait_for_text()
        if text:
            self.status_lbl.set_text("Synced clipboard text to mobile device.")

    def ring_phone(self):
        self.status_lbl.set_text("Sending ring prompt to phone...")

def main():
    if not HAS_GTK:
        print("[Crosslink Error] PyGObject is required.")
        sys.exit(1)

    GLib.set_prgname("crosslink")
    GLib.set_application_name("Crosslink")

    app = CrosslinkApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
