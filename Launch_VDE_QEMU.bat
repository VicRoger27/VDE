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
echo   [1] Boot Installed Hard Disk (vde-disk.qcow2) - Fast, Permanent & No GDM Freeze [RECOMMENDED]
echo   [2] Instant Live Desktop Tryout - Boot from ISO into RAM
echo   [3] Ubuntu Server Backbone - With 20GB VirtIO disk
echo.
set CHOICE=1
set /p CHOICE="Enter choice [1, 2 or 3, default is 1]: "

if "%CHOICE%"=="2" goto use_tryout
if "%CHOICE%"=="3" goto use_server
goto use_disk

:use_disk
echo.
echo [*] Selected: Boot Installed Hard Disk (vde-disk.qcow2)
start "" "%QEMU_BIN%" -accel whpx -accel tcg -m 3072 -smp 4 -drive "file=%DISK_PATH%,if=virtio,format=qcow2" -boot c -vga virtio -device usb-tablet -display gtk -name "Victorious Desktop Environment (VDE)"
goto done

:use_server
set TARGET_ISO=%SERVER_ISO%
echo.
echo [*] Selected: Ubuntu Server with 20GB VirtIO disk
start "" "%QEMU_BIN%" -accel whpx -accel tcg -m 3072 -smp 4 -cdrom "%TARGET_ISO%" -drive "file=%DISK_PATH%,if=virtio,format=qcow2" -boot d -vga virtio -device usb-tablet -display gtk -name "Victorious Desktop Environment (VDE)"
goto done

:use_tryout
set TARGET_ISO=%TRYOUT_ISO%
echo.
echo [*] Selected: Instant Live Desktop Tryout (ISO)
start "" "%QEMU_BIN%" -accel whpx -accel tcg -m 3072 -smp 4 -cdrom "%TARGET_ISO%" -drive "file=%DISK_PATH%,if=virtio,format=qcow2" -boot d -vga virtio -device usb-tablet -display gtk -name "Victorious Desktop Environment (VDE)"
goto done

:done
echo.
echo VM launched in safe window.
echo ========================================================
pause
