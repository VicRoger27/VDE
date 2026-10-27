# Changelog 19: One-Command Terminal Installer with Clean Desktop Replacement

## Summary
Created a universal terminal installation engine ([`install.sh`](file:///c:/Users/Victor/Antigravity%20Projects/Other/DEs/VDE/install.sh)) that can be executed directly inside any running Ubuntu Server, Ubuntu Desktop (GNOME), Debian, Mint, Arch, or Fedora installation. Supports clean replacement (`--replace` / `--wipe`) to purge heavy legacy desktop environments, GDM, and Canonical telemetry bloat, replacing them completely with VDE.

## Key Changes
1. **Universal Installer Script (`install.sh`)**:
   - Remote one-liner execution:
     ```bash
     curl -sSL https://raw.githubusercontent.com/VicRoger27/VDE/main/install.sh | sudo bash -s -- --replace
     ```
   - Automatically detects package manager (`apt-get`, `pacman`, `dnf`).
   - Wipes old desktops: purges `gnome-shell`, `gnome-session`, `gdm3`, `ubuntu-desktop`, and Canonical telemetry (`whoopsie`, `popularity-contest`, `ubuntu-report`, `apport`).
   - Deploys VDE assets, tokens, compositor files (`/etc/xdg/labwc/`), Astal shell, Qt runner, and Crossings settings app.
   - Installs system commands into `/usr/local/bin/`: `vde`, `vde-session`, `vde-bar`, `vde-launcher`, `crossings`.
   - Sets up automatic boot into VDE on tty1 and registers Wayland session `/usr/share/wayland-sessions/vde.desktop`.

2. **Removed Redundant VM Helper**:
   - Deleted `Kill_VM.bat` as requested.

3. **Documentation Updated (`README.md`)**:
   - Documented the one-command terminal installer and clean replacement workflow.
