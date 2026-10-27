# Changelog 29: Permission Hardening, Shell Launcher Fallback & Autostart Independence

## Summary
Resolved the execution errors observed during live session execution:
1. **Quote `QT_QPA_PLATFORM` (`compositor/environment`)**:
   - Quoted `export QT_QPA_PLATFORM="wayland;xcb"` to eliminate the `xcb: not found` shell parse error caused by unquoted semicolons.
2. **Permission Hardening (`install.sh`)**:
   - Added recursive executable bits (`chmod -R +x`) across `/usr/share/vde/astal-shell`, `qt-launcher`, and `apps`.
   - Hardened `/usr/local/bin/vde-bar` to self-heal executable permissions on the shell runner and fall back directly to `waybar`.
3. **Autostart Independence (`compositor/autostart`)**:
   - Removed blocking dependence on non-existent `vde-session.target`, ensuring `swaybg`, `pipewire`, `wireplumber`, and `vde-bar` spawn unconditionally on every session launch.
