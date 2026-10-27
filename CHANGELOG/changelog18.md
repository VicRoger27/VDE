# Changelog 18: Safe Windowed QEMU Runner & Absolute Pointer (USB Tablet) Integration

## Summary
Diagnosed and eliminated the critical mouse-trapping and cursor oscillation bug in QEMU. Switched the display backend to native GTK windowing with standard window chrome (minimize/maximize/close) and integrated absolute USB tablet pointing emulation (`-device usb-tablet`).

## Root Cause Analysis
Running QEMU in exclusive fullscreen via SDL (`-display sdl -full-screen`) without an absolute pointing device defaults to relative PS/2 mouse packet emulation. On high-DPI Windows 11 systems, relative motion events wrap at the display boundaries, flooding the SDL input event queue in an infinite loop (rapid vertical oscillation) and locking the keyboard grab thread. This prevented `Ctrl + Alt + G` and `Ctrl + Alt + F` from processing.

## Key Changes
1. **Absolute USB Tablet Pointer (`-device usb-tablet`)**:
   - Added `-device usb-tablet` to both [`Launch_VDE_QEMU.bat`](file:///c:/Users/Victor/Antigravity%20Projects/Other/DEs/VDE/Launch_VDE_QEMU.bat) and [`builder/test_iso_qemu.ps1`](file:///c:/Users/Victor/Antigravity%20Projects/Other/DEs/VDE/builder/test_iso_qemu.ps1).
   - Eliminates mouse warp oscillation and provides seamless, uncaptured pointer movement.

2. **Safe GTK Display Backend (`-display gtk`)**:
   - Replaced raw exclusive SDL fullscreen with standard GTK windowing.
   - Preserves standard Windows title bar controls (Minimize, Maximize, Close `X`), menu bar options (`View -> Full Screen`), and standard `Alt + F4` termination.

3. **Emergency Failsafe Script ([`Kill_VM.bat`](file:///c:/Users/Victor/Antigravity%20Projects/Other/DEs/VDE/Kill_VM.bat))**:
   - Added a 1-click batch script to instantly terminate all QEMU and VirtualBox processes if needed.
