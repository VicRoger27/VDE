# Changelog 25: Mica Waybar Fallback Engine, Wallpaper Canvas & Desktop Context Menu

## Summary
Resolved the blank dark screen resulting from missing Astal/AGS runtime by introducing native Waybar taskbar fallback, solid dark Mica wallpaper rendering, and Labwc desktop context menu:
1. **Waybar Taskbar Fallback (`astal-shell/vde-bar`)**:
   - Added automatic fallback to Waybar when AGS / Astal is uncompiled or missing.
   - Designed Windows 11 style centered taskbar layout (`waybar_config.jsonc`) with Start button, app launcher icons, tasklist, tray, audio volume, and clock.
   - Styled with VDE Mica dark tokens (`waybar_style.css`) featuring translucent `#18181b` acrylic backdrop, rounded pills, and hover feedback.
2. **Wallpaper Canvas (`compositor/autostart`)**:
   - Integrated `swaybg -c '#18181b'` to paint a cohesive dark Mica background canvas instead of an empty black frame.
3. **Right-Click Context Menu (`compositor/menu.xml`)**:
   - Added Labwc root context menu accessible via desktop right-click with quick launchers for Terminal (`foot`), Start Menu, Settings (`crossings`), and Session control.
4. **Installer Modernization (`install.sh`)**:
   - Ensured `universe` repository is enabled and bundled `waybar`, `swaybg`, and `menu.xml` deployment.
