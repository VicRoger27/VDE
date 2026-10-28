# Changelog 47: Window Controls (Minimize, Maximize, Close), Wayland App ID Taskbar Icons & Font Awesome Suite

## Summary
Resolved missing window controls (minimize/maximize buttons) and taskbar icon resolution across all 12 native VDE applications:

1. **Window Control Buttons (Minimize, Maximize, Close)**:
   - Configured `self.header.set_decoration_layout(":minimize,maximize,close")` across all 12 Python desktop applications.
   - Configured global `/etc/gtk-3.0/settings.ini` and `~/.config/gtk-3.0/settings.ini` with `gtk-decoration-layout = :minimize,maximize,close`.
   - Set `<titleLayout>NLIMC</titleLayout>` in Labwc compositor theme (`compositor/rc.xml`) for comprehensive server-side and client-side decoration parity.

2. **Native Wayland App ID & Taskbar Icons**:
   - Replaced generic `python3` process title by calling `GLib.set_prgname("<app_name>")` and `GLib.set_application_name("<App Title>")` at startup for all 12 applications.
   - Added `StartupWMClass=<app_name>` and `Icon=<app_name>` across all 12 `.desktop` files.
   - Deployed high-resolution vector SVG icons for all applications to `assets/icons/glm/` and `/usr/share/icons/hicolor/scalable/apps/` with standard freedesktop fallback aliases.

3. **Taskbar Launcher Icons (Font Awesome & Emojis)**:
   - Added `fonts-font-awesome` and `fonts-noto-color-emoji` to `install.sh` dependencies.
   - Updated `waybar_config.jsonc` center modules with Font Awesome glyphs (``, ``, ``, ``, ``) and expanded `waybar_style.css` font stack to prevent missing glyph fallback rectangles.
