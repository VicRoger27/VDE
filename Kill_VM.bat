@echo off
title Emergency VM Killer
echo ========================================================
echo   Stopping any running Virtual Machine processes...
echo ========================================================
taskkill /f /im qemu-system-x86_64.exe >nul 2>&1
taskkill /f /im VirtualBoxVM.exe >nul 2>&1
taskkill /f /im VirtualBox.exe >nul 2>&1
echo Done. All VM processes terminated.
timeout /t 2
