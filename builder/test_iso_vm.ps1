# VDE VirtualBox VM Test Runner (PowerShell / Windows Native)
# Launches a native Virtual Machine for testing VDE ISOs without WSL or containers

param (
    [string]$IsoPath = "vde-live-amd64.iso",
    [string]$VmName = "VDE-Live-Test",
    [int]$RamMB = 2048,
    [int]$Cpus = 2
)

$VBoxManage = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"

if (-not (Test-Path $VBoxManage)) {
    Write-Error "VirtualBox not found at $VBoxManage"
    exit 1
}

# Resolve ISO path: fallback to local ISO folder if build ISO doesn't exist yet
if (-not (Test-Path $IsoPath)) {
    $fallbackIso = "C:\Users\Victor\ISO\ubuntu-26.04.1-live-server-amd64.iso"
    if (Test-Path $fallbackIso) {
        Write-Host "Notice: $IsoPath not found, using local ISO cache: $fallbackIso" -ForegroundColor Yellow
        $IsoPath = $fallbackIso
    } else {
        Write-Error "No valid ISO found at $IsoPath or $fallbackIso"
        exit 1
    }
}

$resolvedIso = (Resolve-Path $IsoPath).Path
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Launching VDE Native VirtualBox VM ($VmName)" -ForegroundColor Cyan
Write-Host " ISO: $resolvedIso" -ForegroundColor Cyan
Write-Host " RAM: ${RamMB} MB | CPUs: $Cpus | Graphics: VMSVGA 128MB" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Check if VM already exists; unregister/remove if recreating
$existing = & $VBoxManage list vms | Select-String "`"$VmName`""
if ($existing) {
    Write-Host ">> Powering off and replacing existing VM '$VmName'..." -ForegroundColor Yellow
    & $VBoxManage controlvm $VmName poweroff 2>$null
    Start-Sleep -Seconds 1
    & $VBoxManage unregistervm $VmName --delete 2>$null
}

# 1. Create VM
Write-Host ">> Creating VM definition..."
& $VBoxManage createvm --name $VmName --ostype "Ubuntu_64" --register

# 2. Configure Hardware (CPUs, RAM, Graphics, EFI/BIOS)
Write-Host ">> Configuring hardware specs..."
& $VBoxManage modifyvm $VmName `
    --cpus $Cpus `
    --memory $RamMB `
    --vram 128 `
    --graphicscontroller vmsvga `
    --accelerate3d on `
    --audio-enabled on `
    --audio-controller hda `
    --nic1 nat `
    --boot1 dvd `
    --boot2 disk `
    --boot3 none `
    --boot4 none

# 3. Attach Storage Controller and ISO
Write-Host ">> Attaching optical drive with ISO..."
& $VBoxManage storagectl $VmName --name "IDE Controller" --add ide
& $VBoxManage storageattach $VmName `
    --storagectl "IDE Controller" `
    --port 0 `
    --device 0 `
    --type dvddrive `
    --medium $resolvedIso

# 4. Start the VM in a native GUI window
Write-Host ">> Booting VM into GUI window..." -ForegroundColor Green
& $VBoxManage startvm $VmName --type gui

Write-Host "==========================================================" -ForegroundColor Green
Write-Host " VM '$VmName' is now running!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
