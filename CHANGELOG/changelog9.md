# Changelog 9: VirtualBox Frontend Fix & Multi-Backbone ISO Preset Architecture

## Summary
Resolved the issue where launching the VirtualBox test virtual machine from background automation or CLI runners caused the process to default to `separate` (detached/headless) mode without an interactive GUI window. Hardened the launcher configuration to explicitly enforce `GUI/DefaultFrontend = gui` and added multi-backbone ISO preset switching.

## Key Changes
1. **VirtualBox Frontend Enforcement (`builder/test_iso_vm.ps1`)**:
   - Set VM extradata parameter `GUI/DefaultFrontend = gui` to guarantee VirtualBox allocates a visible host window station upon launch instead of detaching into a headless COM session.
   - Fixed PowerShell syntax compatibility (replaced bash-style `||` operator with robust try/catch blocks).
   - Added preset support (`-Preset server`, `-Preset lubuntu`, `-Preset budgie`, `-Preset vde`, `-Preset custom`) allowing seamless testing against minimal Ubuntu Server backbone or full desktop live ISOs located in `C:\Users\Victor\ISO\`.

2. **1-Click Interactive Desktop Launcher (`Launch_VDE_VM.bat`)**:
   - Updated launcher script to directly spawn `VirtualBoxVM.exe --startvm "VDE-Live-Test"` within the user's interactive Windows desktop session (`Session 7`).
   - Added safety pre-checks to ensure stale background locks are cleared and GUI frontend metadata is verified before display window initialization.

3. **Backbone Architecture Documentation**:
   - Documented the distinction between the VDE desktop shell layer (Labwc, Astal, Qt6/QML, Crossings) and the underlying OS backbone (Ubuntu Server minbase).
