# VDE Changelog — Milestone 8

All notable changes and architectural clarifications for VDE.

---

## [Milestone 8: Ubuntu Server Backbone Architecture & VM Integration] - 2026-10-27

### Clarified & Fixed
- **OS Backbone Clarification (Ubuntu Server / uS)**:
  - Documented that VDE is a desktop shell (dGUI) requiring an underlying Linux OS backbone (Ubuntu Server 24.04 noble minbase) containing the Linux kernel, systemd init, mesa-vulkan GPU drivers, pipewire audio, and labwc compositor.
  - Clarified that the raw `ubuntu-26.04.1-live-server-amd64.iso` by itself boots into Canonical's text-mode Subiquity installer unless the VDE live image is generated using `builder/build_iso.sh` (which strips snaps/telemetry, injects the VDE shell, and sets autologin into labwc).
- **VirtualBox Foregrounding & Management (`builder/test_iso_vm.ps1`)**:
  - Reconfigured VM registration to cleanly register `VDE-Live-Test` directly inside Oracle VirtualBox Manager.
  - Clarified Windows Session Isolation constraints: background CLI processes cannot force windows onto the active desktop station without user launch context.
  - Configured [`Launch_VDE_VM.bat`](file:///c:/Users/Victor/Antigravity%20Projects/Other/DEs/VDE/Launch_VDE_VM.bat) for 1-click execution directly from Windows Explorer.
