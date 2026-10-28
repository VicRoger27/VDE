# Changelog 41: Standalone OS Desktop Environment & Native Core Applications

## Summary
Eliminated nested-app execution and established VDE as the true, standalone operating system desktop environment across the physical display:
1. **Standalone Systemd Display Service (`vde.service`)**:
   - Deployed `/etc/systemd/system/vde.service` running directly on `/dev/tty1` via systemd-logind and DRM/KMS hardware master.
   - Disabled and masked legacy display managers (`gdm3`, `gdm`, `lightdm`, `sddm`) and set VDE as the default `graphical.target`.
   - Replaced nested terminal window execution with clean hardware TTY switching (`chvt 1`).
2. **Direct DRM/KMS Backend Initialization**:
   - Purged remote display variables (`unset WAYLAND_DISPLAY DISPLAY`) in `vde-session`, `vde`, and `install.sh`.
   - Prevents Labwc from attempting to attach to zombie Wayland sockets, resolving `Could not connect to remote display: Connection refused`.
3. **Crossings Settings Hub (`crossings_gui.py`)**:
   - Created full native Python 3 + GTK 3 desktop settings application with Fluent Dark Mica styling.
   - Features interactive controls for Display Resolution & Scaling (`wlr-randr`), Brightness (`brightnessctl`), Personalization (wallpapers with instant `swaybg` switching, accent colors), Sound (`wpctl`/PipeWire volume slider), Zero-Telemetry audit status, and System Specs (real-time RAM consumption showing sub-500 MB idle target).
   - Wired to `Super+I`, `Super+S`, and taskbar Settings icon.
4. **VDE Terminal Emulator (`vde-terminal` & `foot.ini`)**:
   - Deployed Fluent Dark Mica configuration for `foot` (`compositor/foot.ini`).
   - Created `/usr/local/bin/vde-terminal` wrapper with automatic fallbacks (`foot`, `xterm`).
   - Wired to `Super+Return`, `Super+T`, `Ctrl+Alt+T`, and taskbar Terminal icon.
5. **Mirror & Display Projection Hotkey**:
   - Created `compositor/vde-display-toggle` bound to `Super+P` and laptop hardware `XF86Display` key.
6. **Taskbar & Start Menu Integration**:
   - Updated `waybar_config.jsonc` and `vde-bar` with direct action runners.
   - Updated `vde-launcher` to toggle `wofi` on `Super_L`, `Super_R`, `Super+Space`, and Start button clicks.
7. **Installer Signal Protection & Dependencies**:
   - Added `trap '' HUP PIPE` in `install.sh` to protect installation against terminal closure when purging GNOME.
   - Added `pcmanfm`, `python3-gi`, `gir1.2-gtk-3.0`, and `wlr-randr` to default package payload.
