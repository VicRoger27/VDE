# Changelog 62 - Root Menu Context, Taskbar Watchdog & Waybar Self-Healing

### Highlights & Modifications
1. **Desktop Right-Click Root Menu Binding**:
   - Added `<context name="Root">` with right-click `<action name="ShowMenu"><menu>root-menu</menu></action>` in `compositor/rc.xml`.
   - Right-clicking anywhere on the wallpaper canvas now immediately brings up the full VDE application launcher menu.

2. **Universal Waybar Configuration & Watchdog**:
   - Replaced fragile module dependencies in `waybar_config.jsonc` with universal Fluent Windows 11 pinned app buttons.
   - Refactored `waybar_style.css` to 100% compliant GTK 3 CSS (eliminated non-standard transitions and transforms).
   - Replaced fragile sleep logic in `astal-shell/vde-bar` with an automated watchdog loop that keeps Waybar running continuously.
   - Extended compositor settling delay in `compositor/autostart` to 1.2s to guarantee layer-shell socket readiness.
