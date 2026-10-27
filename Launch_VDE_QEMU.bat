@echo off
title VDE Hardware-Accelerated Runner (WHPX + Safe Window)
echo ========================================================
echo   Victorious Desktop Environment (VDE) - Safe VM Runner
echo   Hardware Acceleration: WHPX (Windows Hypervisor Platform)
echo ========================================================
echo.

set QEMU_BIN=%~dp0tools\qemu\qemu-system-x86_64.exe
set DISK_PATH=C:\Users\Victor\ISO\Test\vde-disk.qcow2
set TRYOUT_ISO=C:\Users\Victor\ISO\Test\vde-live-tryout.iso
set SERVER_ISO=C:\Users\Victor\ISO\Test\vde-live-amd64.iso

echo Select Boot Mode:
echo   [1] Instant Live Desktop Tryout - Direct boot to VDE in RAM
echo   [2] Ubuntu Server Backbone - With 20GB VirtIO disk
echo.
set CHOICE=1
set /p CHOICE="Enter choice [1 or 2, default is 1]: "

if "%CHOICE%"=="2" goto use_server
goto use_tryout

:use_server
set TARGET_ISO=%SERVER_ISO%
echo.
echo [*] Selected: Ubuntu Server with 20GB VirtIO disk
goto do_launch

:use_tryout
set TARGET_ISO=%TRYOUT_ISO%
echo.
echo [*] Selected: Instant Live Desktop Tryout
goto do_launch

:do_launch
echo.
echo [SAFETY CONTROLS]
echo   - Mouse: Absolute USB Tablet (smooth, seamless, no trapping)
echo   - Window: Standard window with Minimize / Maximize / Close [X]
echo   - Fullscreen: Click 'View' -^> 'Full Screen' or press [Ctrl + Alt + F]
echo   - Emergency Exit: Press [Alt + F4] or close window
echo.
echo Launching QEMU...

start "" "%QEMU_BIN%" -accel whpx -accel tcg -m 3072 -smp 4 -cdrom "%TARGET_ISO%" -drive "file=%DISK_PATH%,if=virtio,format=qcow2" -boot d -vga virtio -device usb-tablet -display gtk -name "Victorious Desktop Environment (VDE)"

echo.
echo VM launched in safe window.
echo ========================================================
pause
