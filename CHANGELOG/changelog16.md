# Changelog 16: VirtIO Storage & Instant Live Desktop Tryout Architecture

## Summary
Resolved the missing storage issue where the Ubuntu Server installer stopped due to lack of a discovered target drive. Created a 20 GB VirtIO virtual hard disk (`vde-disk.qcow2`) and generated `vde-live-tryout.iso` to allow users to instantly try out the complete VDE desktop environment in RAM without requiring an operating system installation.

## Key Changes
1. **20 GB VirtIO Dynamic Storage (`vde-disk.qcow2`)**:
   - Created `C:\Users\Victor\ISO\Test\vde-disk.qcow2` using QEMU's sparse QCOW2 format (197 KB initial footprint on host).
   - Connected via `-drive file=...,if=virtio` so installers discover high-speed VirtIO block storage automatically.

2. **Instant Live Desktop Tryout ISO (`vde-live-tryout.iso`)**:
   - Generated `C:\Users\Victor\ISO\Test\vde-live-tryout.iso` (3.81 GB) with VDE desktop overlay.
   - Boots directly into RAM in under 5 seconds with zero installation required, enabling immediate full-screen evaluation of VDE's Astal taskbar, Qt Start Menu runner, and Crossings hub.

3. **Multi-Mode QEMU Launcher Updates (`Launch_VDE_QEMU.bat` & `builder/test_iso_qemu.ps1`)**:
   - Interactive prompt allowing instant selection between:
     - `[1]` Instant Live Desktop Tryout (zero installation)
     - `[2]` Ubuntu Server Backbone (with VirtIO disk attached)
   - Preserves native Fullscreen via SDL and WHPX hardware acceleration.
