# VDE Compositor Configuration

Target compositor: **Labwc** (lightweight wlroots-based Wayland window manager).

## Contents
- `rc.xml`: Window snapping rules (`Super + Arrows`), keybindings, margin gaps, focus policies.
- `autostart`: Initialization script launching Astal taskbar daemon, Qt6 launcher daemon, and background services.
- `environment`: Wayland environment flags (`XDG_CURRENT_DESKTOP=VDE`, `QT_QPA_PLATFORM=wayland`).
- `systemd/`: User session service definitions (`vde-session.target`).
