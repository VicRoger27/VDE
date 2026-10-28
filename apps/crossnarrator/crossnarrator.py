#!/usr/bin/env python3
"""
Cross Narrator — VDE Fluent Accessibility Narrator
Speech Synthesis & Screen Reader Tool for Victorious Desktop Environment
"""

import os
import sys
import subprocess
import shutil

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

.card {
    background-color: #27272a;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 8px;
    padding: 16px;
    margin: 8px 16px;
}

textview {
    background-color: #121214;
    color: #ffffff;
    font-size: 14px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 6px;
    padding: 10px;
}

textview text {
    background-color: #121214;
    color: #ffffff;
}

button.accent-btn {
    background: #38bdf8;
    color: #09090b;
    font-weight: 600;
    border-radius: 6px;
    padding: 8px 20px;
    border: none;
}

button.accent-btn:hover {
    background: #7dd3fc;
}

button.sec-btn {
    background: rgba(255, 255, 255, 0.08);
    color: #fafafa;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 6px;
    padding: 8px 16px;
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

class CrossNarratorApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Narrator")
        self.set_icon_name("crossnarrator")
        Gtk.Window.set_default_icon_name("crossnarrator")
        self.set_default_size(560, 480)
        self.set_position(Gtk.WindowPosition.CENTER)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(CSS_STYLE)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.proc = None

        # HeaderBar
        header = Gtk.HeaderBar()
        header.set_show_close_button(True)
        header.set_decoration_layout(":minimize,maximize,close")
        header.props.title = "Narrator"
        header.props.subtitle = "Cross Narrator"
        self.set_titlebar(header)

        # Main Layout
        root_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(root_box)

        # Status Card
        status_card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        status_card.get_style_context().add_class("card")
        root_box.pack_start(status_card, False, False, 0)

        icon_lbl = Gtk.Label(label="🗣️")
        icon_lbl.override_font(gi.repository.Pango.FontDescription("28"))
        status_card.pack_start(icon_lbl, False, False, 0)

        status_text_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=2)
        t = Gtk.Label(label="VDE Accessibility Narrator", xalign=0)
        t.override_font(gi.repository.Pango.FontDescription("14 bold"))
        d = Gtk.Label(label="Speak on-screen text, clipboard contents, or custom inputs.", xalign=0)
        d.override_font(gi.repository.Pango.FontDescription("11"))
        status_text_box.pack_start(t, False, False, 0)
        status_text_box.pack_start(d, False, False, 0)
        status_card.pack_start(status_text_box, True, True, 0)

        # Text input card
        text_card = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=8)
        text_card.get_style_context().add_class("card")
        root_box.pack_start(text_card, True, True, 0)

        tl = Gtk.Label(label="Text to Speak:", xalign=0)
        text_card.pack_start(tl, False, False, 0)

        scrolled = Gtk.ScrolledWindow()
        scrolled.set_size_request(-1, 140)
        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.buffer = self.textview.get_buffer()
        self.buffer.set_text("Welcome to Victorious Desktop Environment. Narrator is active and ready to assist you.")
        scrolled.add(self.textview)
        text_card.pack_start(scrolled, True, True, 0)

        # Sliders Card
        ctrl_card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=16)
        ctrl_card.get_style_context().add_class("card")
        root_box.pack_start(ctrl_card, False, False, 0)

        # Speed
        speed_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        speed_box.pack_start(Gtk.Label(label="Speed (wpm):", xalign=0), False, False, 0)
        self.speed_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 100, 250, 10)
        self.speed_scale.set_value(160)
        speed_box.pack_start(self.speed_scale, True, True, 0)
        ctrl_card.pack_start(speed_box, True, True, 0)

        # Pitch
        pitch_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        pitch_box.pack_start(Gtk.Label(label="Pitch:", xalign=0), False, False, 0)
        self.pitch_scale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 10, 90, 5)
        self.pitch_scale.set_value(50)
        pitch_box.pack_start(self.pitch_scale, True, True, 0)
        ctrl_card.pack_start(pitch_box, True, True, 0)

        # Action Buttons
        btn_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        btn_box.set_margin_start(16)
        btn_box.set_margin_end(16)
        btn_box.set_margin_bottom(16)
        root_box.pack_start(btn_box, False, False, 0)

        speak_btn = Gtk.Button(label="▶ Speak Text")
        speak_btn.get_style_context().add_class("accent-btn")
        speak_btn.connect("clicked", lambda b: self.speak_current())
        btn_box.pack_start(speak_btn, True, True, 0)

        clip_btn = Gtk.Button(label="📋 Read Clipboard")
        clip_btn.get_style_context().add_class("sec-btn")
        clip_btn.connect("clicked", lambda b: self.read_clipboard())
        btn_box.pack_start(clip_btn, True, True, 0)

        stop_btn = Gtk.Button(label="⏹ Stop")
        stop_btn.get_style_context().add_class("sec-btn")
        stop_btn.connect("clicked", lambda b: self.stop_speech())
        btn_box.pack_start(stop_btn, False, False, 0)

    def speak_text(self, text):
        self.stop_speech()
        if not text.strip():
            return

        speed = int(self.speed_scale.get_value())
        pitch = int(self.pitch_scale.get_value())

        if shutil.which("espeak-ng"):
            self.proc = subprocess.Popen(["espeak-ng", "-s", str(speed), "-p", str(pitch), text])
        elif shutil.which("espeak"):
            self.proc = subprocess.Popen(["espeak", "-s", str(speed), "-p", str(pitch), text])
        elif shutil.which("spd-say"):
            self.proc = subprocess.Popen(["spd-say", "-r", str(speed - 160), text])

    def speak_current(self):
        buf = self.buffer
        text = buf.get_text(buf.get_start_iter(), buf.get_end_iter(), True)
        self.speak_text(text)

    def read_clipboard(self):
        clipboard = Gtk.Clipboard.get(Gdk.SELECTION_CLIPBOARD)
        text = clipboard.wait_for_text()
        if text:
            self.buffer.set_text(text)
            self.speak_text(text)

    def stop_speech(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            self.proc = None
        subprocess.call(["pkill", "-9", "espeak-ng"], stderr=subprocess.DEVNULL)
        subprocess.call(["pkill", "-9", "espeak"], stderr=subprocess.DEVNULL)

def main():
    if not HAS_GTK:
        print("[Cross Narrator Error] PyGObject is required.")
        sys.exit(1)

    GLib.set_prgname("crossnarrator")
    GLib.set_application_name("Narrator")

    app = CrossNarratorApp()
    app.connect("destroy", lambda w: (app.stop_speech(), Gtk.main_quit()))
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
