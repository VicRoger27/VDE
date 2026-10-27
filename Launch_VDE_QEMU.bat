@echo off
title VDE QEMU Hardware-Accelerated Runner
echo ========================================================
echo   Victorious Desktop Environment (VDE) - QEMU Runner
echo   Hardware Acceleration: WHPX (Windows Hypervisor Platform)
echo   Target ISO: C:\Users\Victor\ISO\Test\vde-live-amd64.iso
echo ========================================================
echo.
echo [QEMU HOTKEYS]
echo   - [Ctrl + Alt + F] : Toggle in/out of Fullscreen mode!
echo   - [Ctrl + Alt + G] : Release mouse cursor back to Windows!
echo.
echo Launching VDE directly into Fullscreen with WHPX acceleration...

set QEMU_BIN=%~dp0tools\qemu\qemu-system-x86_64.exe
set ISO_PATH=C:\Users\Victor\ISO\Test\vde-live-amd64.iso

if not exist "%ISO_PATH%" (
    echo [Notice] Custom ISO not found in Test folder, using primary ISO...
    set ISO_PATH=C:\Users\Victor\ISO\ubuntu-26.04.1-live-server-amd64.iso
)

start "" "%QEMU_BIN%" ^
    -accel whpx ^
    -accel tcg ^
    -m 2048 ^
    -smp 2 ^
    -cdrom "%ISO_PATH%" ^
    -boot d ^
    -vga virtio ^
    -display sdl ^
    -full-screen ^
    -name "Victorious Desktop Environment (VDE) - Fullscreen"

echo.
echo QEMU VM window dispatched!
echo ========================================================
timeout /t 3
