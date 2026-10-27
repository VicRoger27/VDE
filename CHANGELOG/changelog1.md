# VDE Changelog

All notable changes and milestones for the Victor Desktop Environment (VDE) project are documented in this file.

---

## [Unreleased] - Phase 3 & 4

### Added
- **Astal GTK4 Shell (`vde-bar`)**:
  - Centered floating taskbar dock (`widget/Taskbar.tsx`) with 6px bottom margin and layer-shell integration.
  - Windows 11 Fluent Start button (`widget/StartButton.tsx`) with dynamic local AI status indication:
    - Idle monochrome state (`start-idle-dark.svg`).
    - Active AI inference state (`start-active-dark.svg`) with cyan halo and pulsing dot.
    - Offline/standby state (`start-offline-dark.svg`) with slashed circle glyph.
  - Pinned application launchers (`widget/TaskItems.tsx`) for File Explorer, Web Browser, Text Editor, and Terminal with running dot and focused pill indicators.
  - Quick Settings action center flyout (`widget/QuickSettings.tsx`) featuring 2x2 toggle grid (Wi-Fi, Bluetooth, Dark/Light Theme, Airplane Mode), WirePlumber volume & brightness sliders, battery readout, and power management actions (Sleep, Restart, Shutdown).
  - Taskbar right cluster pill (`widget/QuickSettingsPill.tsx`) and two-line Windows 11 clock (`widget/Clock.tsx`).
  - Session D-Bus IPC service (`services/dbus.ts`) connecting `org.vde.Shell` and `org.vde.Launcher`.
  - Compiled GTK4 CSS (`style.css`) and SCSS stylesheet (`style/style.scss`) with frosted dark acrylic and mica styling.
  - Standalone executable runner script (`vde-bar`).

---

## [Phase 2] - 2026-10-27

### Added
- **Labwc Compositor Configuration**:
  - Windows 11 snapping hotkeys in `compositor/rc.xml`:
    - `Super + Left / Right` for 50% split screen snap.
    - `Super + Up / Down` for maximize, restore, and minimize.
    - `Super + Alt + Arrows` for 4-corner quadrant snapping (0% 0% 50% 50%, etc.).
    - D-Bus bindings for `Super` / `Super + Space` (Start Menu), `Super + A` (Quick Settings), and `Super + N` (Calendar).
  - Server-side window frame rules suppressing borders on `vde-bar`, `vde-launcher`, and `vde-quicksettings`.
  - Dark Mica window theme in `compositor/themerc` (32px titlebar height, 8px corner radii, drop shadows).
  - Session environment variables in `compositor/environment` (`XDG_CURRENT_DESKTOP=VDE:wlroots`, `QT_QPA_PLATFORM=wayland;xcb`).
  - Compositor initialization script in `compositor/autostart` with D-Bus update and systemd target fallback.
  - Systemd user session units in `compositor/systemd/`:
    - `vde-session.target` (graphical session target).
    - `vde-bar.service` (Astal shell daemon).
    - `vde-launcher.service` (Qt6 runner daemon).
    - `vde-llama.service` (in-memory llama.cpp server for MiniCPM-V 4.7).
  - Linux automated session installer script `compositor/install_session.sh`.

---

## [Assets & Synchronization] - 2026-10-27

### Added
- **Vector Icon Asset Library**:
  - Integrated 74 production vector icons generated via GLM 5.3 Flash Effort Max and DeepSeek DeepThink.
  - Dual dark (`-dark.svg`) and light (`-light.svg`) variant coverage across all icons.
  - Window control titlebar buttons (minimize, maximize, restore, close).
  - Pinned application launchers (File Explorer, Web Browser, Text Editor, Gallery).
  - System tray indicators (Calendar, Lock, Microphone privacy indicator with amber glow, Airplane mode, Cast display).
  - Production icons organized into `assets/icons/` and `assets/icons/glm/`; alternative set archived in `assets/icons/dseek/`.
  - Asset manifest tracking in `assets/asset_manifest.json` and extraction scripts `assets/organize_icons.py`.

---

## [Phase 1] - 2026-10-27

### Added
- Initialized workspace structure (`compositor/`, `astal-shell/`, `qt-launcher/`, `tokens/`, `assets/`).
- Defined core Windows 11 Dark Mica / Acrylic design tokens in `tokens/theme.json`.
- Implemented Python token compilation engine `tokens/compile_tokens.py` exporting SCSS and QML tokens.
- Drafted comprehensive architecture blueprint and implementation roadmap in `IMPLEMENTATION_PLAN.md`.
- Established community governance and project repository foundation (`.github/`, `LICENCE.md`, `SECURITY.md`, `CODEOWNERS`).
