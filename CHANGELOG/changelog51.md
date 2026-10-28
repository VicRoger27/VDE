# Changelog 51: Windhawk Windows 11 Acrylic Start Menu & Quick Settings Suite

**Date:** 2026-10-28
**Commit Tag:** `[changelog51]`
**Repository:** `i2qq/VDE`

### Summary of Changes:
1. **Windows 11 Start Menu (`vde_startmenu.py`)**:
   - Engineered native Python 3 + GTK 3 Windows 11 Start Menu styled after Windhawk *Windows 11 Start Menu Styler*.
   - Features centered floating acrylic card (`rgba(28, 28, 34, 0.92)`), 14px rounded corners, search box with real-time app filtering, 6-column Pinned section for all 12 VDE native apps, Recommended section, user avatar, and power action menu (Lock, Sign out, Restart, Shut down).
   - Replaced legacy text-list launcher in `vde-launcher` with `vde_startmenu.py`.
2. **Windows 11 Quick Settings & Notification Center (`vde_quicksettings.py`)**:
   - Built native Quick Settings popup styled after Windhawk *Windows 11 Notification Center Styler*.
   - Features quick toggles (Wi-Fi, Night Light, Mute, Snipping, Settings, Lock), smooth volume and brightness sliders, and full calendar widget.
   - Connected to taskbar clock, pulseaudio, and network modules.
3. **Taskbar Stability & Self-Healing (`vde-bar` & `autostart`)**:
   - Added self-healing fallback `waybar_safe_config.jsonc` in `vde-bar` so if standard distribution Waybar packages fail on experimental modules (`wlr/taskbar`), Waybar automatically restarts into the safe pinned launcher configuration without leaving the desktop barren.
   - Added `sleep 0.5` in `autostart` to ensure the Wayland compositor socket is fully bound before shell launch.
4. **App Launch & Path Resolution Fixes**:
   - Fixed `apps/crossminal/crossminal` to properly check `/usr/share/vde/apps/crossminal/crossminal.py`.
   - Fixed `apps/crossings/crossings.desktop` `Exec` path to `/usr/local/bin/crossings`.
   - Updated `install.sh` to install `vde-quicksettings` and guarantee 755 execution permissions.
   - Updated `tests/verify_vde_stack.py` with syntax checks for the new shell components.
