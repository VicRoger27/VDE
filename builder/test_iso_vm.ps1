# VDE VirtualBox VM Test Runner (PowerShell / Windows Native)
# Launches a native Virtual Machine for testing VDE ISOs on top of Ubuntu Server backbone

param (
    [string]$IsoPath = "",
    [string]$VmName = "VDE-Live-Test",
    [int]$RamMB = 2048,
    [int]$Cpus = 2,
    [ValidateSet("server", "lubuntu", "budgie", "vde", "custom")]
    [string]$Preset = "server"
)

$VBoxManage = "C:\Program Files\Oracle\VirtualBox\VBoxManage.exe"
$VBoxGUI    = "C:\Program Files\Oracle\VirtualBox\VirtualBox.exe"
$VBoxVM     = "C:\Program Files\Oracle\VirtualBox\VirtualBoxVM.exe"

if (-not (Test-Path $VBoxManage)) {
    Write-Error "VirtualBox not found at $VBoxManage"
    exit 1
}

# Resolve ISO path based on Preset or explicit IsoPath
if (-not $IsoPath) {
    switch ($Preset) {
        "server" {
            $IsoPath = "C:\Users\Victor\ISO\ubuntu-26.04.1-live-server-amd64.iso"
        }
        "lubuntu" {
            $IsoPath = "C:\Users\Victor\ISO\lubuntu-26.10-desktop-amd64.iso"
        }
        "budgie" {
            $IsoPath = "C:\Users\Victor\ISO\ubuntu-budgie-26.10-desktop-amd64.iso"
        }
        "vde" {
            $IsoPath = "vde-live-amd64.iso"
        }
        Default {
            $IsoPath = "C:\Users\Victor\ISO\ubuntu-26.04.1-live-server-amd64.iso"
        }
    }
}

if (-not (Test-Path $IsoPath)) {
    $fallbackIso = "C:\Users\Victor\ISO\ubuntu-26.04.1-live-server-amd64.iso"
    if (Test-Path $fallbackIso) {
        Write-Host "Notice: Selected ISO ($IsoPath) not found. Attaching Ubuntu Server backbone ISO:" -ForegroundColor Yellow
        Write-Host "  $fallbackIso" -ForegroundColor Yellow
        $IsoPath = $fallbackIso
    } else {
        Write-Error "No valid ISO found at $IsoPath or $fallbackIso"
        exit 1
    }
}

$resolvedIso = (Resolve-Path $IsoPath).Path
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " Victorious Desktop Environment (VDE) - VM Manager" -ForegroundColor Cyan
Write-Host " Backbone ISO: $resolvedIso" -ForegroundColor Cyan
Write-Host " RAM: ${RamMB} MB | CPUs: $Cpus | Graphics: VMSVGA 128MB" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# Terminate existing running instance if active and clear orphaned locks
$running = & $VBoxManage list runningvms | Select-String "`"$VmName`""
if ($running) {
    Write-Host ">> Powering off active instance of '$VmName'..." -ForegroundColor Yellow
    & $VBoxManage controlvm $VmName poweroff 2>$null
    Start-Sleep -Seconds 1
}
# Clear any lingering orphaned VM worker processes locking the session
Stop-Process -Name VirtualBoxVM -Force -ErrorAction SilentlyContinue

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

# Force clean standard windowed mode (avoids Windows 11 DWM fullscreen lock on boot)
& $VBoxManage setextradata $VmName "GUI/DefaultFrontend" "gui"
& $VBoxManage setextradata $VmName "GUI/Fullscreen" $null

# Attach storage controller and ISO
try {
    & $VBoxManage storagectl $VmName --name "IDE Controller" --add ide 2>$null
} catch {}

try {
    & $VBoxManage storageattach $VmName `
        --storagectl "IDE Controller" `
        --port 0 `
        --device 0 `
        --type dvddrive `
        --medium $resolvedIso 2>$null
} catch {}

Write-Host "==========================================================" -ForegroundColor Green
Write-Host " VM '$VmName' configured and ready in Oracle VirtualBox!" -ForegroundColor Green
Write-Host " Attached ISO: $resolvedIso" -ForegroundColor Green
Write-Host " Frontend Mode: Standard Window (Press Right Ctrl + F to toggle Fullscreen)" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
Write-Host " To start the VM:" -ForegroundColor Cyan
Write-Host "   - Double-click 'Launch_VDE_VM.bat' in the project folder" -ForegroundColor White
Write-Host "   OR" -ForegroundColor White
Write-Host "   - Open VirtualBox from Start Menu, select '$VmName' and click Start" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Cyan
