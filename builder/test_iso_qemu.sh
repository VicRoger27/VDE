#!/usr/bin/env bash
# VDE QEMU Virtual Machine Test Runner
# Boots the VDE live ISO in a hardware-accelerated VM window

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

ISO_PATH="${1:-$ROOT_DIR/vde-live-amd64.iso}"
RAM_MB=2048
CPUS=2

echo "=========================================================="
echo " VDE QEMU VM Test Runner"
echo " Target ISO: $ISO_PATH"
echo " RAM:        ${RAM_MB} MB"
echo " CPUs:       ${CPUS}"
echo "=========================================================="

if [ ! -f "$ISO_PATH" ]; then
    # Check fallback to local Windows ISO directory if mounted
    FALLBACK="/mnt/c/Users/Victor/ISO/ubuntu-26.04.1-live-server-amd64.iso"
    if [ -f "$FALLBACK" ]; then
        echo "Notice: $ISO_PATH not found, using local ISO cache: $FALLBACK"
        ISO_PATH="$FALLBACK"
    else
        echo "[Error] ISO file not found at: $ISO_PATH" >&2
        exit 1
    fi
fi

# Detect acceleration
ACCEL_OPTS=()
if [ -e /dev/kvm ] && [ -w /dev/kvm ]; then
    echo ">> KVM hardware acceleration enabled."
    ACCEL_OPTS+=("-enable-kvm" "-cpu" "host")
elif grep -q Microsoft /proc/version 2>/dev/null; then
    echo ">> Running under Windows/WSL; using WHPX / TCG acceleration."
    ACCEL_OPTS+=("-cpu" "max")
else
    echo ">> Software emulation mode (TCG)."
    ACCEL_OPTS+=("-cpu" "max")
fi

# Launch QEMU VM
exec qemu-system-x86_64 \
    "${ACCEL_OPTS[@]}" \
    -m "${RAM_MB}" \
    -smp "${CPUS}" \
    -cdrom "$ISO_PATH" \
    -boot d \
    -vga virtio \
    -display gtk,gl=on \
    -device intel-hda -device hda-duplex \
    -net nic,model=virtio -net user \
    -name "VDE Live OS (Victorious Desktop Environment)"
