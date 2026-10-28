#!/usr/bin/env python3
"""
Crosslock — VDE Fluent Clock & Timer
Modern Dark Mica World Clock, Stopwatch, and Timer for Victorious Desktop Environment
"""

import os
import sys
import time
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

notebook {
    background-color: #18181b;
    border: none;
}

notebook tab {
    background-color: #121214;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-bottom: none;
    border-radius: 6px 6px 0 0;
    padding: 8px 18px;
    margin-right: 4px;
    font-size: 13px;
    color: #a1a1aa;
}

notebook tab:checked {
    background-color: #18181b;
    border-top: 2px solid #38bdf8;
    color: #ffffff;
    font-weight: 600;
}

.time-hero {
    font-size: 56px;
    font-weight: 700;
    color: #ffffff;
    margin: 20px 0 6px 0;
}

.date-hero {
    font-size: 18px;
    color: #a1a1aa;
    margin-bottom: 24px;
}

.stopwatch-hero {
    font-size: 52px;
    font-weight: 700;
    font-family: 'DejaVu Sans Mono', monospace;
    color: #38bdf8;
    margin: 24px 0;
}

button.accent-btn {
    background: #38bdf8;
    color: #09090b;
    font-weight: 600;
    border-radius: 6px;
    padding: 8px 24px;
    border: none;
    font-size: 14px;
}

button.accent-btn:hover {
    background: #7dd3fc;
}

button.sec-btn {
    background: rgba(255, 255, 255, 0.08);
    color: #fafafa;
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 6px;
    padding: 8px 20px;
    font-size: 14px;
}

button.sec-btn:hover {
    background: rgba(255, 255, 255, 0.15);
}

.card {
    background-color: #27272a;
    border: 1px solid rgba(255, 255, 255, 0.06);
    border-radius: 8px;
    padding: 14px 18px;
    margin: 6px 16px;
}
"""

class CrosslockApp(Gtk.Window):
    def __init__(self):
        super().__init__(title="Clock")
        self.set_default_size(520, 520)
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
        header.props.title = "Clock & Timer"
        header.props.subtitle = "Crosslock"
        self.set_titlebar(header)

        # Notebook
        notebook = Gtk.Notebook()
        self.add(notebook)

        # 1. World Clock Tab
        clock_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        clock_box.set_valign(Gtk.Align.CENTER)
        self.clock_lbl = Gtk.Label(label="00:00:00", xalign=0.5)
        self.clock_lbl.get_style_context().add_class("time-hero")
        clock_box.pack_start(self.clock_lbl, False, False, 0)

        self.date_lbl = Gtk.Label(label="Date", xalign=0.5)
        self.date_lbl.get_style_context().add_class("date-hero")
        clock_box.pack_start(self.date_lbl, False, False, 0)

        world_cities = [("London", "UTC"), ("New York", "UTC-5"), ("Tokyo", "UTC+9")]
        for city, tz in world_cities:
            card = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
            card.get_style_context().add_class("card")
            c_name = Gtk.Label(label=f"🌍 {city} ({tz})", xalign=0)
            c_time = Gtk.Label(label="--:--", xalign=1)
            card.pack_start(c_name, True, True, 0)
            card.pack_end(c_time, False, False, 0)
            clock_box.pack_start(card, False, False, 0)

        notebook.append_page(clock_box, Gtk.Label(label="🕒 Clock"))

        # 2. Stopwatch Tab
        self.sw_running = False
        self.sw_start_time = 0
        self.sw_elapsed = 0
        self.laps = []

        sw_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        sw_box.set_valign(Gtk.Align.CENTER)
        self.sw_lbl = Gtk.Label(label="00:00.00", xalign=0.5)
        self.sw_lbl.get_style_context().add_class("stopwatch-hero")
        sw_box.pack_start(self.sw_lbl, False, False, 0)

        sw_ctrl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        sw_ctrl.set_halign(Gtk.Align.CENTER)
        self.sw_toggle_btn = Gtk.Button(label="Start")
        self.sw_toggle_btn.get_style_context().add_class("accent-btn")
        self.sw_toggle_btn.connect("clicked", self.on_sw_toggle)
        sw_ctrl.pack_start(self.sw_toggle_btn, False, False, 0)

        self.sw_reset_btn = Gtk.Button(label="Reset")
        self.sw_reset_btn.get_style_context().add_class("sec-btn")
        self.sw_reset_btn.connect("clicked", self.on_sw_reset)
        sw_ctrl.pack_start(self.sw_reset_btn, False, False, 0)
        sw_box.pack_start(sw_ctrl, False, False, 0)

        notebook.append_page(sw_box, Gtk.Label(label="⏱ Stopwatch"))

        # 3. Timer Tab
        self.timer_seconds_left = 300 # 5 minutes default
        self.timer_running = False

        timer_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        timer_box.set_valign(Gtk.Align.CENTER)
        self.timer_lbl = Gtk.Label(label="05:00", xalign=0.5)
        self.timer_lbl.get_style_context().add_class("stopwatch-hero")
        timer_box.pack_start(self.timer_lbl, False, False, 0)

        spin_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        spin_box.set_halign(Gtk.Align.CENTER)
        spin_lbl = Gtk.Label(label="Minutes:")
        self.timer_spin = Gtk.SpinButton.new_with_range(1, 180, 1)
        self.timer_spin.set_value(5)
        self.timer_spin.connect("value-changed", self.on_timer_spin_changed)
        spin_box.pack_start(spin_lbl, False, False, 0)
        spin_box.pack_start(self.timer_spin, False, False, 0)
        timer_box.pack_start(spin_box, False, False, 0)

        timer_ctrl = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        timer_ctrl.set_halign(Gtk.Align.CENTER)
        self.timer_toggle_btn = Gtk.Button(label="Start")
        self.timer_toggle_btn.get_style_context().add_class("accent-btn")
        self.timer_toggle_btn.connect("clicked", self.on_timer_toggle)
        timer_ctrl.pack_start(self.timer_toggle_btn, False, False, 0)

        self.timer_reset_btn = Gtk.Button(label="Reset")
        self.timer_reset_btn.get_style_context().add_class("sec-btn")
        self.timer_reset_btn.connect("clicked", self.on_timer_reset)
        timer_ctrl.pack_start(self.timer_reset_btn, False, False, 0)
        timer_box.pack_start(timer_ctrl, False, False, 0)

        notebook.append_page(timer_box, Gtk.Label(label="⏳ Timer"))

        # Tick Timer
        GLib.timeout_add(100, self.on_tick)

    def on_tick(self):
        now = datetime.now()
        self.clock_lbl.set_text(now.strftime("%I:%M:%S %p"))
        self.date_lbl.set_text(now.strftime("%A, %B %d, %Y"))

        if self.sw_running:
            elapsed = time.time() - self.sw_start_time
            mins = int(elapsed // 60)
            secs = int(elapsed % 60)
            cents = int((elapsed * 100) % 100)
            self.sw_lbl.set_text(f"{mins:02d}:{secs:02d}.{cents:02d}")

        if self.timer_running and self.timer_seconds_left > 0:
            self.timer_seconds_left -= 0.1
            if self.timer_seconds_left <= 0:
                self.timer_seconds_left = 0
                self.timer_running = False
                self.timer_toggle_btn.set_label("Start")
                self.timer_lbl.set_text("00:00 - Done!")
            else:
                secs_total = int(self.timer_seconds_left)
                m = secs_total // 60
                s = secs_total % 60
                self.timer_lbl.set_text(f"{m:02d}:{s:02d}")

        return True

    def on_sw_toggle(self, btn):
        if self.sw_running:
            self.sw_running = False
            self.sw_elapsed = time.time() - self.sw_start_time
            self.sw_toggle_btn.set_label("Start")
        else:
            self.sw_running = True
            self.sw_start_time = time.time() - self.sw_elapsed
            self.sw_toggle_btn.set_label("Pause")

    def on_sw_reset(self, btn):
        self.sw_running = False
        self.sw_elapsed = 0
        self.sw_lbl.set_text("00:00.00")
        self.sw_toggle_btn.set_label("Start")

    def on_timer_spin_changed(self, spin):
        if not self.timer_running:
            mins = int(spin.get_value())
            self.timer_seconds_left = mins * 60
            self.timer_lbl.set_text(f"{mins:02d}:00")

    def on_timer_toggle(self, btn):
        if self.timer_running:
            self.timer_running = False
            self.timer_toggle_btn.set_label("Start")
        else:
            if self.timer_seconds_left <= 0:
                self.timer_seconds_left = int(self.timer_spin.get_value()) * 60
            self.timer_running = True
            self.timer_toggle_btn.set_label("Pause")

    def on_timer_reset(self, btn):
        self.timer_running = False
        mins = int(self.timer_spin.get_value())
        self.timer_seconds_left = mins * 60
        self.timer_lbl.set_text(f"{mins:02d}:00")
        self.timer_toggle_btn.set_label("Start")

def main():
    if not HAS_GTK:
        print("[Crosslock Error] PyGObject is required.")
        sys.exit(1)

    app = CrosslockApp()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
