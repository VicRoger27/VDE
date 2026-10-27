# Changelog 12: Resolve Pre-Boot Fullscreen Hang in VirtualBox

## Summary
Diagnosed and eliminated the startup freeze caused by forcing `GUI/Fullscreen = true` in VirtualBox extradata prior to guest OS boot. Configured reliable windowed startup mode with dynamic host-key fullscreen toggling.

## Root Cause Analysis
Forcing `GUI/Fullscreen = true` in VirtualBox metadata before guest display drivers initialize causes VirtualBox's DirectComposition rendering subsystem to attempt an exclusive display mode switch on the host monitor during early EFI/BIOS boot (640x480 unaccelerated text mode). On Windows 11 with Core Isolation and VMSVGA graphics, this results in a deadlock between the VirtualBox worker threads and the Windows Desktop Window Manager (DWM), causing `VirtualBoxVM.exe` to hang indefinitely and lock the COM machine session.

## Key Changes
1. **Removed Pre-Boot Fullscreen Extradata (`builder/test_iso_vm.ps1` & `Launch_VDE_VM.bat`)**:
   - Stripped `GUI/Fullscreen = true` from pre-boot metadata to allow clean virtual graphics modesetting.
   - Preserved instant post-boot fullscreen switching via standard host shortcut (`Right Ctrl + F`).

2. **Clean State Verification**:
   - Verified clean VM start and shutdown cycle with zero COM session locks.
