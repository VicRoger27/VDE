# VDE QEMU Hardware-Accelerated Runner (Windows Native)
# Runs the live ISO in QEMU with WHPX acceleration and native fullscreen

param (
    [ValidateSet("tryout", "server")]
    [string]$Mode = "tryout",
    [int]$RamMB = 3072,
    [int]$Cpus = 4,
    [switch]$Windowed
)

$QemuBin = Join-Path (Split-Path (Split-Path $MyInvocation.MyCommand.Path)) "tools\qemu\qemu-system-x86_64.exe"
$DiskPath = "C:\Users\Victor\ISO\Test\vde-disk.qcow2"

if ($Mode -eq "server") {
    $IsoPath = "C:\Users\Victor\ISO\Test\vde-live-amd64.iso"
} else {
    $IsoPath = "C:\Users\Victor\ISO\Test\vde-live-tryout.iso"
}

if (-not (Test-Path $QemuBin)) {
    Write-Error "QEMU executable not found at $QemuBin"
    exit 1
}

$resolvedIso = (Resolve-Path $IsoPath).Path
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " VDE QEMU VM Test Runner (Hardware-Accelerated)" -ForegroundColor Cyan
Write-Host " Target ISO:   $resolvedIso" -ForegroundColor Cyan
Write-Host " Virtual Disk: $DiskPath (20 GB VirtIO)" -ForegroundColor Cyan
Write-Host " Accelerator:  WHPX (Windows Hypervisor Platform)" -ForegroundColor Cyan
Write-Host " RAM:          ${RamMB} MB | CPUs: $Cpus" -ForegroundColor Cyan
Write-Host " Display Mode: $(if ($Windowed) { 'Windowed' } else { 'Native Fullscreen' })" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " [HOTKEYS]" -ForegroundColor Yellow
Write-Host "   - [Ctrl + Alt + F] : Toggle Fullscreen" -ForegroundColor White
Write-Host "   - [Ctrl + Alt + G] : Release Mouse cursor" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Cyan

$qemuArgs = @(
    "-accel", "whpx",
    "-accel", "tcg",
    "-m", $RamMB,
    "-smp", $Cpus,
    "-cdrom", $resolvedIso,
    "-drive", "file=$DiskPath,if=virtio,format=qcow2",
    "-boot", "d",
    "-vga", "virtio",
    "-display", "sdl",
    "-name", "Victorious Desktop Environment (VDE) - QEMU"
)

if (-not $Windowed) {
    $qemuArgs += "-full-screen"
}

Start-Process -FilePath $QemuBin -ArgumentList $qemuArgs
Write-Host ">> QEMU process launched successfully!" -ForegroundColor Green
