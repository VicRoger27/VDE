@echo off
title VDE Virtual Machine Runner
echo ========================================================
echo   Victorious Desktop Environment (VDE) - VM Runner
echo ========================================================
echo.
echo 1. Clearing any stuck locks...
taskkill /f /im VirtualBoxVM.exe >nul 2>&1
timeout /t 1 /nobreak >nul

echo 2. Setting clean windowed startup (prevents DWM fullscreen hang)...
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" setextradata "VDE-Live-Test" "GUI/DefaultFrontend" "gui" >nul 2>&1
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" setextradata "VDE-Live-Test" "GUI/Fullscreen" "" >nul 2>&1

echo.
echo 3. Launching VDE Virtual Machine window...
echo.
echo [TIP] Once the VM window opens, press [Right Ctrl + F] to enter Fullscreen!
echo.
start "" "C:\Program Files\Oracle\VirtualBox\VirtualBoxVM.exe" --startvm "VDE-Live-Test"

echo Window dispatched successfully.
echo ========================================================
timeout /t 3
