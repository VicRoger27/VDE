@echo off
title VDE Virtual Machine Runner
echo ========================================================
echo   Victorious Desktop Environment (VDE) - VM Runner
echo ========================================================
echo.
echo Launching VDE in VirtualBox GUI...
start "" "C:\Program Files\Oracle\VirtualBox\VirtualBox.exe" --startvm "VDE-Live-Test"
echo.
echo If the VM does not start:
echo Select 'VDE-Live-Test' in VirtualBox Manager and click the green 'Start' button.
echo ========================================================
timeout /t 3
