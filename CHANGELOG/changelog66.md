# Changelog 66: Native Python GTK Windows 11 Taskbar Engine & System Dock

1. **Native Fluent Windows 11 Taskbar (`astal-shell/vde_taskbar.py`)**:
   - Implemented a zero-dependency, native Python GTK3 taskbar docked at screen bottom (height 48px), featuring Windows 11 Fluent Dark Mica styling (`rgba(18, 18, 22, 0.88)` with `1px solid rgba(255, 255, 255, 0.12)` top border).
   - **Universal Wayland Layer-Shell & X11 Dock**: Utilizes `GtkLayerShell` (with exclusive zone reservation) on Wayland compositors and falls back smoothly to `Gdk.WindowTypeHint.DOCK` on X11 / standard window managers with automatic multi-monitor repositioning.
   - **Left Zone**: Added VDE Brand Pill (`❖ VDE`) with translucent blue hover effect and Task View icon (`❐`).
   - **Center Dock**:
     - Windows 11 Start Menu button (`⊞`) that toggles `/usr/local/bin/vde-launcher`.
     - Search button (`🔍`) launching Start Menu search.
     - Pinned launchers for Terminal, Files, Notepad, Settings, Paint, Calculator, and Snipping Tool.
     - Dynamic **Windhawk Active Indicator Pills**: Scans running tasks to light up glowing 16px cyan bottom pills (`#38bdf8`) under active applications.
   - **Right Zone**:
     - System Tray overflow chevron (`^`).
     - Combined Quick Settings Pill displaying real-time Network (Wi-Fi/Ethernet), Volume, and Battery state, linking to `/usr/local/bin/vde-quicksettings`.
     - Two-line Windows 11 Date & Time clock widget.
     - "Show Desktop" peek strip at the far right corner.

2. **Self-Healing Taskbar Runner (`astal-shell/vde-bar`)**:
   - Refactored `/usr/local/bin/vde-bar` into a robust priority runner: runs native `vde_taskbar.py` under an automated watchdog loop, falling back to Waybar and AGS if ever required.

3. **Installer & Autostart Integration (`install.sh`, `compositor/autostart`, `compositor/menu.xml`)**:
   - Added `vde_taskbar.py` to cryptographically verified core components.
   - Installed `/usr/local/bin/vde-taskbar` executable wrapper into system binaries.
   - Updated session autostart and root context menu "Reload VDE Shell" to seamlessly manage the taskbar process lifecycle.
