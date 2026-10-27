# VDE VirtualBox VM Test Runner (PowerShell / Windows Native)
# Launches a native Virtual Machine for testing VDE ISOs on top of Ubuntu Server backbone

param (
    [string]$IsoPath = "vde-live-amd64.iso",
    [string]$VmName = "VDE-Live-Test",
    [int]$RamMB = 2048,
    [int]$Cpus = 2
)

$VBoxManage = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
$VBoxGUI    = "C:\Program Files\Oracle\VirtualBox\VirtualBox.exe"

if (-not (Test-Path $VBoxManage)) {
    Write-Error "VirtualBox not found at $VBoxManage"
    exit 1
}

# Resolve ISO path: check for built VDE live ISO, or fallback to Ubuntu Server backbone ISO in C:\Users\Victor\ISO
if (-not (Test-Path $IsoPath)) {
    $fallbackIso = "C:\Users\Victor\ISO\ubuntu-26.04.1-live-server-amd64.iso"
    if (Test-Path $fallbackIso) {
        Write-Host "Notice: $IsoPath not yet generated. Attaching Ubuntu Server backbone ISO:" -ForegroundColor Yellow
        Write-Host "  $fallbackIso" -ForegroundColor Yellow
        $IsoPath = $fallbackIso
    } else {
        Write-Error "No valid ISO found at $IsoPath or $fallbackIso"
        exit 1
    }
}

$resolvedIso = (Resolve-Path $IsoPath).Path
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " VDE VirtualBox VM Manager" -ForegroundColor Cyan
Write-Host " Backbone ISO: $resolvedIso" -ForegroundColor Cyan
Write-Host " RAM: ${RamMB} MB | CPUs: $Cpus | Graphics: VMSVGA 128MB" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Terminate existing running instance if active
$running = & $VBoxManage list runningvms | Select-String "`"$VmName`""
if ($running) {
    Write-Host ">> Powering off active instance of '$VmName'..." -ForegroundColor Yellow
    & $VBoxManage controlvm $VmName poweroff 2>$null
    Start-Sleep -Seconds 1
}

# Check if VM definition exists; reconfigure or recreate
$existing = & $VBoxManage list vms | Select-String "`"$VmName`""
if (-not $existing) {
    Write-Host ">> Registering VM definition in VirtualBox..."
    & $VBoxManage createvm --name $VmName --ostype "Ubuntu_64" --register
}

# Configure VM Hardware
Write-Host ">> Setting VM hardware parameters..."
& $VBoxManage modifyvm $VmName `
    --cpus $Cpus `
    --memory $RamMB `
    --vram 128 `
    --graphicscontroller vmsvga `
    --accelerate3d off `
    --audio-enabled on `
    --audio-controller hda `
    --nic1 nat `
    --boot1 dvd `
    --boot2 disk `
    --boot3 none `
    --boot4 none

# Attach storage controller and ISO
& $VBoxManage storagectl $VmName --name "IDE Controller" --add ide 2>$null || true
& $VBoxManage storageattach $VmName `
    --storagectl "IDE Controller" `
    --port 0 `
    --device 0 `
    --type dvddrive `
    --medium $resolvedIso 2>$null || true

# Update 1-click batch launcher
$batPath = Join-Path (Get-Location) "Launch_VDE_VM.bat"
@"
@echo off
title VDE Virtual Machine Runner
echo ========================================================
echo  Launching VDE Live OS ($VmName)
echo  Backbone: Ubuntu Server 24.04
echo ========================================================
start "" "$VBoxGUI" --startvm "$VmName"
"@ | Set-Content -Path $batPath -Encoding ASCII

Write-Host "==========================================================" -ForegroundColor Green
Write-Host " VM '$VmName' is registered and ready in Oracle VirtualBox!" -ForegroundColor Green
Write-Host " To display the VM window interactively on your screen:" -ForegroundColor Cyan
Write-Host "   1. Open Oracle VirtualBox from your Windows Start Menu" -ForegroundColor White
Write-Host "   2. Click 'VDE-Live-Test' in the left pane and press Start" -ForegroundColor White
Write-Host "   OR double-click 'Launch_VDE_VM.bat' in your file explorer." -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Green
