#!/usr/bin/env python3
"""
Compiles astal-shell/style/style.scss and tokens.scss into astal-shell/style.css.
Resolves SCSS variables into standard GTK4 CSS.
"""

from pathlib import Path
import json

ROOT_DIR = Path(__file__).resolve().parent
THEME_JSON = ROOT_DIR.parent / "tokens" / "theme.json"
OUT_CSS = ROOT_DIR / "style.css"

def build_css():
    with open(THEME_JSON, "r", encoding="utf-8") as f:
        theme = json.load(f)

    c = theme["colors"]["dark"]
    r = theme["radii"]
    t = theme["typography"]
    l = theme["layout"]

    css_content = f"""/* VDE Astal Shell - Compiled GTK4 CSS */
* {{
    font-family: {t['fontFamily']};
    font-size: {t['fontSizes']['body']};
    color: {c['text']['primary']};
    box-shadow: none;
    outline: none;
}}

/* ------------------------------------------------------------- */
/* Floating Taskbar Window & Container                           */
/* ------------------------------------------------------------- */
.vde-taskbar-window {{
    background: transparent;
}}

.vde-taskbar-container {{
    background-color: {c['surface']['taskbar']};
    border: 1px solid {c['border']['default']};
    border-radius: {r['lg']};
    min-height: {l['taskbarHeight']}px;
    padding: 0 6px;
    box-shadow: 0 4px 18px rgba(0, 0, 0, 0.32);
}}

.taskbar-left-zone {{
    padding-left: 6px;
}}

.taskbar-center-dock {{
    padding: 0 4px;
}}

.taskbar-right-zone {{
    padding-right: 4px;
}}

/* ------------------------------------------------------------- */
/* Start Button Widget                                           */
/* ------------------------------------------------------------- */
.vde-start-button {{
    min-width: {l['taskbarItemWidth']}px;
    min-height: 40px;
    border-radius: {r['md']};
    background: transparent;
    border: 1px solid transparent;
    padding: 0 8px;
}}

.vde-start-button:hover {{
    background-color: {c['surface']['cardHover']};
}}

.vde-start-button:active {{
    background-color: {c['surface']['cardPressed']};
}}

.vde-start-button.active-inference {{
    border: 1px solid rgba(96, 205, 255, 0.45);
    box-shadow: 0 0 10px {c['status']['aiInferenceGlow']};
}}

.start-icon-wrapper {{
    min-width: 24px;
    min-height: 24px;
}}

/* ------------------------------------------------------------- */
/* Pinned & Running Task Items                                   */
/* ------------------------------------------------------------- */
.vde-task-items {{
    padding: 0 2px;
}}

.vde-task-button {{
    min-width: {l['taskbarItemWidth']}px;
    min-height: 40px;
    border-radius: {r['md']};
    background: transparent;
    border: none;
    padding: 2px 8px 0 8px;
}}

.vde-task-button:hover {{
    background-color: {c['surface']['cardHover']};
}}

.vde-task-button:active {{
    background-color: {c['surface']['cardPressed']};
}}

.task-icon {{
    min-width: {l['taskbarIconSize']}px;
    min-height: {l['taskbarIconSize']}px;
}}

/* Indicators */
.indicator-line.idle {{
    min-width: 0px;
    min-height: 3px;
    background-color: transparent;
}}

.indicator-line.running {{
    min-width: 4px;
    min-height: 4px;
    border-radius: {r['full']};
    background-color: {c['status']['runningIndicator']};
    margin-top: 2px;
}}

.indicator-line.focused {{
    min-width: 16px;
    min-height: 3px;
    border-radius: {r['full']};
    background-color: {c['status']['focusedIndicator']};
    margin-top: 2px;
}}

.vde-workspace-pill {{
    min-width: 36px;
    min-height: 36px;
    border-radius: {r['md']};
    background: transparent;
    border: none;
}}

.vde-workspace-pill:hover {{
    background-color: {c['surface']['cardHover']};
}}

/* ------------------------------------------------------------- */
/* Quick Settings Pill & Clock Button                            */
/* ------------------------------------------------------------- */
.vde-quicksettings-pill {{
    min-height: 36px;
    border-radius: {r['md']};
    background: transparent;
    border: 1px solid transparent;
    padding: 4px 10px;
}}

.vde-quicksettings-pill:hover {{
    background-color: {c['surface']['cardHover']};
}}

.vde-quicksettings-pill:active {{
    background-color: {c['surface']['cardPressed']};
}}

.vde-clock-button {{
    min-height: 36px;
    border-radius: {r['md']};
    background: transparent;
    border: none;
    padding: 2px 8px;
}}

.vde-clock-button:hover {{
    background-color: {c['surface']['cardHover']};
}}

.clock-time {{
    font-size: {t['fontSizes']['body']};
    font-weight: 500;
    color: {c['text']['primary']};
}}

.clock-date {{
    font-size: {t['fontSizes']['caption']};
    color: {c['text']['tertiary']};
    margin-top: -2px;
}}

.show-desktop-strip {{
    min-width: 6px;
    min-height: 32px;
    border-radius: 2px;
    background: transparent;
    border: none;
    margin-left: 2px;
}}

.show-desktop-strip:hover {{
    background-color: rgba(255, 255, 255, 0.15);
}}

/* ------------------------------------------------------------- */
/* Quick Settings Flyout Window                                  */
/* ------------------------------------------------------------- */
.vde-flyout-window {{
    background: transparent;
}}

.quicksettings-card {{
    background-color: {c['surface']['flyout']};
    border: 1px solid {c['border']['strong']};
    border-radius: {r['xl']};
    min-width: {l['quickSettingsWidth']}px;
    padding: 16px;
    box-shadow: 0 16px 36px rgba(0, 0, 0, 0.45);
}}

.toggle-tile {{
    min-height: 48px;
    border-radius: {r['md']};
    background-color: {c['surface']['card']};
    border: 1px solid {c['border']['default']};
    padding: 8px 12px;
}}

.toggle-tile:hover {{
    background-color: {c['surface']['cardHover']};
}}

.toggle-tile.active {{
    background-color: {c['accent']['secondary']};
    border-color: {c['accent']['primary']};
}}

.toggle-tile.active .toggle-label,
.toggle-tile.active .toggle-status {{
    color: #ffffff;
}}

.toggle-label {{
    font-size: {t['fontSizes']['body']};
    font-weight: 600;
    color: {c['text']['primary']};
}}

.toggle-status {{
    font-size: {t['fontSizes']['caption']};
    color: {c['text']['tertiary']};
}}

.slider-icon-btn {{
    background: transparent;
    border: none;
    padding: 4px;
    border-radius: {r['sm']};
}}

.slider-icon-btn:hover {{
    background-color: {c['surface']['cardHover']};
}}

.fluent-slider trough {{
    background-color: #3e3e3e;
    border-radius: {r['full']};
    min-height: 4px;
}}

.fluent-slider highlight {{
    background-color: {c['accent']['primary']};
    border-radius: {r['full']};
    min-height: 4px;
}}

.fluent-slider slider {{
    background-color: #ffffff;
    border: 3px solid {c['accent']['primary']};
    border-radius: {r['full']};
    min-width: 14px;
    min-height: 14px;
}}

.divider {{
    min-height: 1px;
    background-color: {c['border']['divider']};
    margin: 4px 0;
}}

.battery-label {{
    font-size: {t['fontSizes']['body']};
    color: {c['text']['secondary']};
}}

.power-btn {{
    min-width: 32px;
    min-height: 32px;
    border-radius: {r['md']};
    background-color: {c['surface']['card']};
    border: 1px solid {c['border']['default']};
}}

.power-btn:hover {{
    background-color: {c['surface']['cardHover']};
}}

.power-btn.shutdown:hover {{
    background-color: #c42b1c;
    border-color: #c42b1c;
}}
"""

    with open(OUT_CSS, "w", encoding="utf-8") as f:
        f.write(css_content.strip() + "\n")
    print(f"Generated clean GTK4 CSS at: {OUT_CSS}")

if __name__ == "__main__":
    build_css()
