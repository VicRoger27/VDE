# VDE Changelog — Milestone 7

All notable changes and VM launch enhancements for VDE.

---

## [Milestone 7: VirtualBox Foreground GUI Spawner] - 2026-10-27

### Fixed & Enhanced
- **Virtual Machine Window Foregrounding (`builder/test_iso_vm.ps1`)**:
  - Resolved VirtualBox 7 headless isolation where VM processes started from background agent sessions were suppressed by Windows foreground lock policies.
  - Switched graphics acceleration flag to `accelerate3d off` with VMSVGA to prevent blank screen failures on live ISO boot without guest additions.
  - Integrated interactive Windows shell spawner using `explorer.exe` to guarantee the VirtualBox GUI window appears on the user's active desktop session.
  - Generated standalone [`Launch_VDE_VM.bat`](file:///c:/Users/Victor/Antigravity%20Projects/Other/DEs/VDE/Launch_VDE_VM.bat) in the project root for 1-click execution directly from Windows Explorer.
