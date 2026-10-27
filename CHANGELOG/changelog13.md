# Changelog 13: Fix Executable Delegation for VirtualBox GUI Window Creation

## Summary
Corrected a critical executable delegation issue where scripts were invoking `VirtualBoxVM.exe` directly rather than through the primary `VirtualBox.exe` host interface. 

## Root Cause Analysis
In VirtualBox 7.x on Windows, `VirtualBoxVM.exe` is the internal headless hypervisor engine process spawned by the COM subsystem. When launched directly by third-party scripts, it runs the virtual machine in an isolated worker session without registering a top-level Qt desktop window on Windows Desktop Window Manager (`winsta0\default`). This left the VM running invisibly while rendering thumbnails in VirtualBox Manager and disabling the "Show" button.

## Key Changes
1. **Host Executable Correction (`Launch_VDE_VM.bat`)**:
   - Switched execution target from internal worker `VirtualBoxVM.exe` to `VirtualBox.exe --startvm "VDE-Live-Test"`.
   - Cleared all background worker processes to return `VDE-Live-Test` to clean Powered-Off status.
