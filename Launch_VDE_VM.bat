@echo off
title VDE Virtual Machine Runner
echo ========================================================
echo   Victorious Desktop Environment (VDE) - VM Runner
echo ========================================================
echo.
echo Ensuring no stale background VM processes are locking the VM...
"C:\Program Files\Oracle\VirtualBox\VBoxManage.exe" setextradata "VDE-Live-Test" "GUI/DefaultFrontend" "gui" >nul 2>&1

echo.
echo Launching VDE Virtual Machine GUI Window...
start "" "C:\Program Files\Oracle\VirtualBox\VirtualBoxVM.exe" --startvm "VDE-Live-Test"

echo.
echo VM window launch signal sent!
echo.
echo If the VM window does not appear in 3 seconds:
echo 1. Open "Oracle VM VirtualBox" from your Windows Start Menu.
echo 2. Click "VDE-Live-Test" in the machine list.
echo 3. Click the green "Start" button on the toolbar.
echo ========================================================
timeout /t 5
