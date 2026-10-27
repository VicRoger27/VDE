# VDE Changelog — Milestone 6

All notable changes introduced in Milestone 6 of VDE.

---

## [Milestone 6: ISO Builder Toolchain & Crossings Settings App] - 2026-10-27

### Added
- **ISO Builder Toolchain (`builder/`)**:
  - **`builder/build_iso.sh`**: Master live ISO builder supporting both offline generation from local ISO cache (`C:\Users\Victor\ISO\ubuntu-26.04.1-live-server-amd64.iso`) and `debootstrap noble minbase`. Completely purges Canonical snapd, telemetry, whoopsie, ubuntu-report, and cloud-init. Injects VDE desktop binaries, compresses with `mksquashfs -comp zstd -Xcompression-level 19`, and generates hybrid live bootable ISO (`vde-live-amd64.iso`).
  - **`builder/chroot_setup.sh`**: Configures dedicated `vde` user with passwordless sudo, systemd tty1 autologin, and `.bash_profile` execution directly into `labwc` for instant <3s cold boots under 250 MB idle RAM.
  - **`builder/test_iso_vm.ps1`**: Native VirtualBox runner executing directly on Windows with hardware-accelerated 3D (VMSVGA, 2 CPUs, 2048 MB RAM) without requiring WSL or containers.
  - **`builder/test_iso_qemu.sh`**: Hardware-accelerated QEMU VM runner with virtio graphics and audio support.

- **Crossings Native Settings Hub (`apps/crossings/`)**:
  - Windows 11-style native settings application adhering strictly to the two-pane interactive Card architecture (zero KDE-style multi-tier sidebar trees or Apply buttons; instant D-Bus and token persistence).
  - **`CrossingsWindow.qml`**: Resizable frameless window (`1000x700px`) with Windows 11 titlebar controls (minimize, maximize, close) using GLM vector icons.
  - **`CategorySidebar.qml`**: Left pane (`260px`) featuring user profile chip, settings search input, and category navigation with active accent indicators.
  - **`SettingsCard.qml`**: Reusable interactive setting card component with smooth hover scaling and slots for switches, sliders, and selectors.
  - **`pages/SystemPage.qml`**: Sound and display cards, power management, and VDE system specifications banner (~240 MB idle RAM, 100% offline telemetry status).
  - **`pages/PersonalizationPage.qml`**: Dark/Light mode toggle, Windows 11 accent color palette picker (Cyan, Sapphire, Emerald, Amber, Ruby), taskbar alignment, and frosted acrylic translucency switches.
  - **`pages/PrivacyPage.qml`**: Zero Cloud Telemetry security badge, microphone privacy dot indicator toggle, and local offline AI vision search settings (MiniCPM-V 4.7 via localhost:8080).
  - **`crossings` & `crossings.desktop`**: Standalone runner script and XDG desktop entry for Start Menu integration.
