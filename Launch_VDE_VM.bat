@echo off
title VDE Virtual Machine Runner (Fullscreen)
echo ========================================================
echo   Victorious Desktop Environment (VDE) - VM Runner
echo ========================================================
echo.
echo 1. Clearing any stuck session locks or orphaned background processes...
taskkill /f /im VirtualBoxVM.exe >nul 2>&1
timeout /t 1 /nobreak >nul

echo 2. Ensuring GUI and Fullscreen mode are configured...
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" setextradata "VDE-Live-Test" "GUI/DefaultFrontend" "gui" >nul 2>&1
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" setextradata "VDE-Live-Test" "GUI/Fullscreen" "true" >nul 2>&1

echo.
echo 3. Launching VDE Virtual Machine in Fullscreen Window...
echo.
echo [HOTKEY] Press [Right Ctrl + F] on your keyboard to toggle Fullscreen!
echo.
start "" "C:\Program Files\Oracle\VirtualBox\VirtualBoxVM.exe" --startvm "VDE-Live-Test"

echo Launch signal dispatched.
echo.
echo If you prefer to launch from the VirtualBox Manager:
echo - Click 'VDE-Live-Test' in the list and click 'Start'.
echo ========================================================
timeout /t 4
