# Changelog 20: 'Try Ubuntu' Live Session Support & Desktop Launcher

## Summary
Optimized the universal terminal installer ([`install.sh`](file:///c:/Users/Victor/Antigravity%20Projects/Other/DEs/VDE/install.sh)) specifically for "Try Ubuntu" live USB/RAM environments. Enabled nested and native Wayland launching and added automatic desktop shortcuts.

## Key Changes
1. **Live Environment Auto-Detection (`install.sh`)**:
   - Detects Casper / live rootfs (`/rofs`, `/run/casper-iso-path`, `ubuntu`/`lubuntu` live users).
   - Automatically enables the Ubuntu `universe` repository if not yet indexed on the live medium.
   - Deploys a 1-click **Launch VDE** shortcut directly to `/home/ubuntu/Desktop/` with executable permissions.

2. **Smart Session Launching (`/usr/local/bin/vde`)**:
   - Detects active display environments (`$WAYLAND_DISPLAY` or `$DISPLAY`):
     - When run inside an existing GNOME/Ubuntu desktop, it launches a nested hardware-accelerated VDE session in a window.
     - When run from a TTY or console, it launches the full bare-metal Wayland desktop session.

3. **Documentation Updated (`README.md`)**:
   - Added dedicated quick-start instructions for live USB / "Try Ubuntu" testing.
