@echo off
title VDE Hardware-Accelerated Runner (WHPX + Fullscreen)
echo ========================================================
echo   Victorious Desktop Environment (VDE) - QEMU Runner
echo   Hardware Acceleration: WHPX (Windows Hypervisor Platform)
echo ========================================================
echo.

set QEMU_BIN=%~dp0tools\qemu\qemu-system-x86_64.exe
set DISK_PATH=C:\Users\Victor\ISO\Test\vde-disk.qcow2
set TRYOUT_ISO=C:\Users\Victor\ISO\Test\vde-live-tryout.iso
set SERVER_ISO=C:\Users\Victor\ISO\Test\vde-live-amd64.iso

echo Select Boot Mode:
echo   [1] Instant Live Desktop Tryout (Direct boot to VDE in RAM - Zero Install)
echo   [2] Ubuntu Server Backbone (With 20GB VirtIO disk attached)
echo.
set /p CHOICE="Enter choice [1 or 2, default is 1]: "

if "%CHOICE%"=="2" (
    set TARGET_ISO=%SERVER_ISO%
    echo Starting Ubuntu Server backbone with 20GB VirtIO disk...
) else (
    set TARGET_ISO=%TRYOUT_ISO%
    echo Starting Instant Live Desktop tryout (no disk install required)...
)

echo.
echo [QEMU HOTKEYS]
echo   - [Ctrl + Alt + F] : Toggle Fullscreen / Windowed mode
echo   - [Ctrl + Alt + G] : Release Mouse back to Windows
echo.

start "" "%QEMU_BIN%" ^
    -accel whpx ^
    -accel tcg ^
    -m 3072 ^
    -smp 4 ^
    -cdrom "%TARGET_ISO%" ^
    -drive file="%DISK_PATH%",if=virtio,format=qcow2 ^
    -boot d ^
    -vga virtio ^
    -display sdl ^
    -full-screen ^
    -name "Victorious Desktop Environment (VDE) - Fullscreen"

echo QEMU launched successfully.
echo ========================================================
timeout /t 3
