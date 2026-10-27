# Changelog 15: QEMU Hardware-Accelerated Runner with Native Fullscreen & WHPX

## Summary
Integrated portable QEMU 11.1.0 with Windows Hypervisor Platform (WHPX) acceleration and true native fullscreen display, providing an instant alternative to VirtualBox without COM session locks or Windows DWM display conflicts.

## Key Features
1. **Portable QEMU Toolchain (`tools/qemu/`)**:
   - Extracted QEMU 11.1.0 (x86_64) supporting both WHPX hardware acceleration and SDL display backends.
   - Zero installation or registry requirements; portable within the workspace and excluded via `.gitignore`.

2. **1-Click Fullscreen Launcher (`Launch_VDE_QEMU.bat`)**:
   - Boots `C:\Users\Victor\ISO\Test\vde-live-amd64.iso` directly into true native Fullscreen via `-display sdl -full-screen`.
   - Utilizes `-accel whpx` for native Windows 11 Hypervisor Platform near-bare-metal execution.
   - Provides clear keybinding shortcuts for interactive control (`Ctrl + Alt + F` to toggle fullscreen, `Ctrl + Alt + G` to release mouse grab).

3. **PowerShell Runner (`builder/test_iso_qemu.ps1`)**:
   - Native PowerShell test runner with optional `-Windowed` switch, configurable RAM, and CPU parameters.
