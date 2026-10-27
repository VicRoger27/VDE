@echo off
title VDE Virtual Machine Runner (Fullscreen)
echo ========================================================
echo   Victorious Desktop Environment (VDE) - VM Runner
echo ========================================================
echo.
echo Ensuring GUI and Fullscreen mode are enabled...
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" setextradata "VDE-Live-Test" "GUI/DefaultFrontend" "gui" >nul 2>&1
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" setextradata "VDE-Live-Test" "GUI/Fullscreen" "true" >nul 2>&1

echo.
echo Launching VDE in Fullscreen Window...
echo.
echo [TIP] Press [Right Ctrl + F] on your keyboard to toggle in/out of Fullscreen!
echo.
start "" "C:\Program Files\Oracle\VirtualBox\VirtualBoxVM.exe" --startvm "VDE-Live-Test"

echo VM launch signal sent.
echo.
echo If the VM window does not appear in 3 seconds:
echo 1. Open "Oracle VM VirtualBox" from your Windows Start Menu.
echo 2. Click "VDE-Live-Test" in the machine list.
echo 3. Click the green "Start" button.
echo ========================================================
timeout /t 5
