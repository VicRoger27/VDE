#!/usr/bin/env python3
"""
Crossculator — VDE Fluent Calculator
Modern Dark Mica Standard & Scientific Calculator for Victorious Desktop Environment
"""

import os
import sys
import math

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

.calc-display {
    background-color: #121214;
    border-bottom: 1px solid rgba(255, 255, 255, 0.06);
    padding: 16px 20px;
}

.calc-history-lbl {
    font-size: 13px;
    color: #a1a1aa;
}

.calc-result-lbl {
    font-size: 38px;
    font-weight: 700;
    color: #ffffff;
}

button.num-btn {
    background-color: #27272a;
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 6px;
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
    min-width: 58px;
    min-height: 48px;
    margin: 2px;
}

button.num-btn:hover {
    background-color: #3f3f46;
}

button.op-btn {
    background-color: #1c1c1f;
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: 6px;
    font-size: 16px;
    color: #e4e4e7;
    min-width: 58px;
    min-height: 48px;
    margin: 2px;
}

button.op-btn:hover {
    background-color: #27272a;
    color: #ffffff;
}

button.eq-btn {
    background-color: #38bdf8;
    border: none;
    border-radius: 6px;
    font-size: 20px;
    font-weight: 700;
    color: #09090b;
    min-width: 58px;
    min-height: 48px;
    margin: 2px;
}

button.eq-btn:hover {
    background-color: #7dd3fc;
}

.history-sidebar {
    background-color: #121214;
    border-left: 1px solid rgba(255, 255, 255, 0.08);
    padding: 12px;
    min-width: 180px;
}
"""

class CrossculatorWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Calculator")
        self.set_icon_name("crossculator")
        Gtk.Window.set_default_icon_name("crossculator")
        self.set_default_size(360, 520)
        self.set_position(Gtk.WindowPosition.CENTER)

        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(CSS_STYLE)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

        self.expression = ""
        self.current_entry = "0"
        self.memory = 0.0
        self.reset_on_next_input = False
        self.history = []

        # HeaderBar
        self.header = Gtk.HeaderBar()
        self.header.set_show_close_button(True)
        self.header.set_decoration_layout(":minimize,maximize,close")
        self.header.props.title = "Calculator"
        self.header.props.subtitle = "Standard"
        self.set_titlebar(self.header)

        # Main Layout
        root_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.add(root_box)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        root_box.pack_start(main_box, True, True, 0)

        # Display Section
        display_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        display_box.get_style_context().add_class("calc-display")
        main_box.pack_start(display_box, False, False, 0)

        self.expr_lbl = Gtk.Label(label="", xalign=1)
        self.expr_lbl.get_style_context().add_class("calc-history-lbl")
        display_box.pack_start(self.expr_lbl, False, False, 0)

        self.result_lbl = Gtk.Label(label="0", xalign=1)
        self.result_lbl.get_style_context().add_class("calc-result-lbl")
        display_box.pack_start(self.result_lbl, False, False, 0)

        # Keypad Grid
        grid = Gtk.Grid()
        grid.set_column_homogeneous(True)
        grid.set_row_homogeneous(True)
        grid.set_margin_start(8)
        grid.set_margin_end(8)
        grid.set_margin_top(8)
        grid.set_margin_bottom(8)
        main_box.pack_start(grid, True, True, 0)

        # Layout Buttons:
        # Row 0: %, CE, C, ⌫
        # Row 1: 1/x, x², √x, ÷
        # Row 2: 7, 8, 9, ×
        # Row 3: 4, 5, 6, -
        # Row 4: 1, 2, 3, +
        # Row 5: ±, 0, ., =
        buttons = [
            ("%", 0, 0, "op"), ("CE", 1, 0, "op"), ("C", 2, 0, "op"), ("⌫", 3, 0, "op"),
            ("1/x", 0, 1, "op"), ("x²", 1, 1, "op"), ("√x", 2, 1, "op"), ("÷", 3, 1, "op"),
            ("7", 0, 2, "num"), ("8", 1, 2, "num"), ("9", 2, 2, "num"), ("×", 3, 2, "op"),
            ("4", 0, 3, "num"), ("5", 1, 3, "num"), ("6", 2, 3, "num"), ("-", 3, 3, "op"),
            ("1", 0, 4, "num"), ("2", 1, 4, "num"), ("3", 2, 4, "num"), ("+", 3, 4, "op"),
            ("±", 0, 5, "op"), ("0", 1, 5, "num"), (".", 2, 5, "num"), ("=", 3, 5, "eq")
        ]

        for text, col, row, btype in buttons:
            btn = Gtk.Button(label=text)
            if btype == "num":
                btn.get_style_context().add_class("num-btn")
            elif btype == "eq":
                btn.get_style_context().add_class("eq-btn")
            else:
                btn.get_style_context().add_class("op-btn")
            btn.connect("clicked", self.on_btn_click, text)
            grid.attach(btn, col, row, 1, 1)

        # Key Press Event
        self.connect("key-press-event", self.on_key_press)

    def on_btn_click(self, widget, char):
        if char.isdigit():
            if self.current_entry == "0" or self.reset_on_next_input:
                self.current_entry = char
                self.reset_on_next_input = False
            else:
                self.current_entry += char
        elif char == ".":
            if self.reset_on_next_input:
                self.current_entry = "0."
                self.reset_on_next_input = False
            elif "." not in self.current_entry:
                self.current_entry += "."
        elif char == "±":
            if self.current_entry.startswith("-"):
                self.current_entry = self.current_entry[1:]
            elif self.current_entry != "0":
                self.current_entry = "-" + self.current_entry
        elif char == "C":
            self.expression = ""
            self.current_entry = "0"
            self.expr_lbl.set_text("")
        elif char == "CE":
            self.current_entry = "0"
        elif char == "⌫":
            if len(self.current_entry) > 1:
                self.current_entry = self.current_entry[:-1]
            else:
                self.current_entry = "0"
        elif char in ("+", "-", "×", "÷"):
            op = char.replace("×", "*").replace("÷", "/")
            self.expression += f" {self.current_entry} {op} "
            self.expr_lbl.set_text(self.expression)
            self.reset_on_next_input = True
        elif char == "=":
            full_expr = self.expression + f" {self.current_entry} "
            self.calculate(full_expr)
        elif char == "√x":
            try:
                val = float(self.current_entry)
                res = math.sqrt(val)
                self.current_entry = self.format_result(res)
                self.reset_on_next_input = True
            except Exception:
                self.current_entry = "Error"
        elif char == "x²":
            try:
                val = float(self.current_entry)
                res = val ** 2
                self.current_entry = self.format_result(res)
                self.reset_on_next_input = True
            except Exception:
                self.current_entry = "Error"
        elif char == "1/x":
            try:
                val = float(self.current_entry)
                if val == 0:
                    self.current_entry = "Cannot divide by 0"
                else:
                    self.current_entry = self.format_result(1.0 / val)
                self.reset_on_next_input = True
            except Exception:
                self.current_entry = "Error"
        elif char == "%":
            try:
                val = float(self.current_entry) / 100.0
                self.current_entry = self.format_result(val)
                self.reset_on_next_input = True
            except Exception:
                self.current_entry = "Error"

        self.result_lbl.set_text(self.current_entry)

    def calculate(self, expr_str):
        clean_expr = expr_str.replace("×", "*").replace("÷", "/")
        try:
            # Safe evaluation
            allowed_chars = "0123456789.+-*/() "
            if all(c in allowed_chars for c in clean_expr):
                result = eval(clean_expr)
                self.expr_lbl.set_text(expr_str + " =")
                self.current_entry = self.format_result(result)
                self.expression = ""
                self.reset_on_next_input = True
            else:
                self.current_entry = "Invalid"
        except ZeroDivisionError:
            self.current_entry = "Cannot divide by zero"
            self.expression = ""
        except Exception:
            self.current_entry = "Error"
            self.expression = ""

    def format_result(self, num):
        if isinstance(num, float):
            if num.is_integer():
                return str(int(num))
            return f"{num:.8g}"
        return str(num)

    def on_key_press(self, widget, event):
        val = event.keyval
        if Gdk.KEY_0 <= val <= Gdk.KEY_9:
            self.on_btn_click(None, chr(val))
            return True
        elif val == Gdk.KEY_plus:
            self.on_btn_click(None, "+")
            return True
        elif val == Gdk.KEY_minus:
            self.on_btn_click(None, "-")
            return True
        elif val == Gdk.KEY_asterisk:
            self.on_btn_click(None, "×")
            return True
        elif val == Gdk.KEY_slash:
            self.on_btn_click(None, "÷")
            return True
        elif val in (Gdk.KEY_Return, Gdk.KEY_KP_Enter, Gdk.KEY_equal):
            self.on_btn_click(None, "=")
            return True
        elif val == Gdk.KEY_BackSpace:
            self.on_btn_click(None, "⌫")
            return True
        elif val == Gdk.KEY_Escape:
            self.on_btn_click(None, "C")
            return True
        return False

def main():
    if not HAS_GTK:
        print("[Crossculator Error] PyGObject is required.")
        sys.exit(1)

    GLib.set_prgname("crossculator")
    GLib.set_application_name("Crossculator")

    app = CrossculatorWindow()
    app.connect("destroy", Gtk.main_quit)
    app.show_all()
    Gtk.main()

if __name__ == "__main__":
    main()
