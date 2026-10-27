# Changelog 10: Automatic Fullscreen Mode Configuration for VirtualBox VM

## Summary
Added automatic Fullscreen mode configuration to the VDE VirtualBox test runner and 1-click batch launcher, enabling an immersive native OS testing experience. Documented host key shortcuts for toggling between fullscreen and windowed modes.

## Key Changes
1. **Fullscreen Extradata Configuration (`builder/test_iso_vm.ps1`)**:
   - Added `-Fullscreen` switch (defaults to `$true`).
   - Sets VirtualBox VM metadata `GUI/Fullscreen = true` via `VBoxManage setextradata`.
   - Allows seamless toggling between true fullscreen immersion and windowed developer view.

2. **Launcher Update (`Launch_VDE_VM.bat`)**:
   - Automatically sets `GUI/Fullscreen = true` before launching `VirtualBoxVM.exe`.
   - Prominently displays host key reminder (`Right Ctrl + F`) to quickly toggle in and out of fullscreen mode.
