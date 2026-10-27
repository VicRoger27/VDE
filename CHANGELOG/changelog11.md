# Changelog 11: COM Session Lock Auto-Recovery & Process Cleanup

## Summary
Resolved an issue where powering down or toggling a VirtualBox virtual machine left orphaned `VirtualBoxVM.exe` worker processes running in the background. These orphaned processes caused COM session lock errors (`VBOX_E_INVALID_OBJECT_STATE 0x80bb0007`), preventing the VM from powering back up.

## Key Changes
1. **Automated Session Lock Recovery (`Launch_VDE_VM.bat`)**:
   - Added pre-launch cleanup step (`taskkill /f /im VirtualBoxVM.exe`) to automatically terminate hung or lingering VM worker processes before dispatching a launch request.
   - Cleans up locks seamlessly without disrupting the main VirtualBox Manager application.

2. **PowerShell Test Runner Hardening (`builder/test_iso_vm.ps1`)**:
   - Added automated worker process cleanup to guarantee clean VM registration and parameter modifications across consecutive test runs.
   - Re-verified clean configuration and registration of `VDE-Live-Test`.
