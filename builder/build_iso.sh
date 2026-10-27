#!/usr/bin/env bash
# VDE Live ISO Builder
# Builds a bootable hybrid live ISO (Ubuntu 24.04 noble minbase, sub-250MB idle RAM, zero snaps)
# Supports offline generation from local ISO cache without downloading anything

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

WORK_DIR="/tmp/vde-iso-build"
ROOTFS="$WORK_DIR/rootfs"
ISODIR="$WORK_DIR/iso"
OUTPUT_ISO="$ROOT_DIR/vde-live-amd64.iso"
UBUNTU_RELEASE="noble"
UBUNTU_MIRROR="http://archive.ubuntu.com/ubuntu/"

LOCAL_ISO_CANDIDATES=(
    "$1"
    "/mnt/c/Users/Victor/ISO/ubuntu-26.04.1-live-server-amd64.iso"
    "/mnt/c/Users/Victor/ISO/lubuntu-26.10-desktop-amd64.iso"
)

LOCAL_ISO=""
for cand in "${LOCAL_ISO_CANDIDATES[@]}"; do
    if [ -n "$cand" ] && [ -f "$cand" ]; then
        LOCAL_ISO="$cand"
        break
    fi
done

echo "=========================================================="
echo " VDE Live ISO Builder"
echo " Target ISO:  $OUTPUT_ISO"
if [ -n "$LOCAL_ISO" ]; then
    echo " Source Mode: OFFLINE from Local ISO ($LOCAL_ISO)"
else
    echo " Source Mode: ONLINE debootstrap ($UBUNTU_RELEASE)"
fi
echo " Quality:     Zero Snaps, Zero Telemetry, Sub-250MB RAM"
echo "=========================================================="

if [ "$EUID" -ne 0 ]; then
    echo "[Error] This script must be run as root (e.g., sudo ./builder/build_iso.sh)." >&2
    exit 1
fi

# 1. Clean and Prepare Work Directories
echo ">> Cleaning and preparing build directories in $WORK_DIR..."
rm -rf "$WORK_DIR"
mkdir -p "$ROOTFS" "$ISODIR/live" "$ISODIR/boot/grub"

if [ -n "$LOCAL_ISO" ]; then
    # OFFLINE PATH: Extract directly from existing local ISO
    echo ">> Extracting rootfs offline from local ISO: $LOCAL_ISO..."
    MNT_ISO="$WORK_DIR/mnt_iso"
    mkdir -p "$MNT_ISO"
    mount -o loop,ro "$LOCAL_ISO" "$MNT_ISO"

    # Find squashfs inside ISO
    SQUASH_SRC=$(find "$MNT_ISO" -name "*.squashfs" | head -n 1)
    if [ -n "$SQUASH_SRC" ]; then
        echo ">> Unpacking live squashfs ($SQUASH_SRC)..."
        unsquashfs -d "$ROOTFS" -f "$SQUASH_SRC"
    else
        echo "[Error] No squashfs found inside $LOCAL_ISO." >&2
        umount "$MNT_ISO" 2>/dev/null || true
        exit 1
    fi
    umount "$MNT_ISO"
else
    # ONLINE PATH: Bootstrap Minimal Ubuntu 24.04 Rootfs
    echo ">> Bootstrapping minimal Ubuntu ($UBUNTU_RELEASE) via debootstrap..."
    debootstrap --variant=minbase \
        --components=main,universe \
        --include=linux-generic,live-boot,systemd-sysv,udev,kmod,dbus,network-manager,sudo,labwc,mesa-vulkan-drivers,pipewire,wireplumber,polkitd,foot,iproute2,libglib2.0-bin,brightnessctl,grim,slurp,wl-clipboard,swaylock \
        "$UBUNTU_RELEASE" "$ROOTFS" "$UBUNTU_MIRROR"
fi

# 2. Inject VDE Components into Rootfs
echo ">> Injecting VDE desktop components and configurations..."
mkdir -p "$ROOTFS/usr/share/vde"
mkdir -p "$ROOTFS/usr/share/vde/assets"
mkdir -p "$ROOTFS/usr/share/vde/tokens"
mkdir -p "$ROOTFS/usr/share/vde/compositor"
mkdir -p "$ROOTFS/usr/share/vde/astal-shell"
mkdir -p "$ROOTFS/usr/share/vde/qt-launcher"
mkdir -p "$ROOTFS/usr/share/vde/apps"

# Copy project files
cp -r "$ROOT_DIR/assets/"* "$ROOTFS/usr/share/vde/assets/" 2>/dev/null || true
cp -r "$ROOT_DIR/tokens/"* "$ROOTFS/usr/share/vde/tokens/" 2>/dev/null || true
cp -r "$ROOT_DIR/compositor/"* "$ROOTFS/usr/share/vde/compositor/" 2>/dev/null || true
cp -r "$ROOT_DIR/astal-shell/"* "$ROOTFS/usr/share/vde/astal-shell/" 2>/dev/null || true
cp -r "$ROOT_DIR/qt-launcher/"* "$ROOTFS/usr/share/vde/qt-launcher/" 2>/dev/null || true
if [ -d "$ROOT_DIR/apps" ]; then
    cp -r "$ROOT_DIR/apps/"* "$ROOTFS/usr/share/vde/apps/" 2>/dev/null || true
fi

# Symlink binaries to /usr/local/bin
mkdir -p "$ROOTFS/usr/local/bin"
cp "$ROOT_DIR/astal-shell/vde-bar" "$ROOTFS/usr/local/bin/vde-bar" 2>/dev/null || true
cp "$ROOT_DIR/qt-launcher/vde-launcher" "$ROOTFS/usr/local/bin/vde-launcher" 2>/dev/null || true
chmod +x "$ROOTFS/usr/local/bin/"* 2>/dev/null || true

# 3. Execute Chroot Setup
echo ">> Running chroot configuration..."
cp "$SCRIPT_DIR/chroot_setup.sh" "$ROOTFS/tmp/chroot_setup.sh"
chmod +x "$ROOTFS/tmp/chroot_setup.sh"

mount --bind /dev "$ROOTFS/dev"
mount --bind /dev/pts "$ROOTFS/dev/pts"
mount --bind /proc "$ROOTFS/proc"
mount --bind /sys "$ROOTFS/sys"

chroot "$ROOTFS" /tmp/chroot_setup.sh

umount -lf "$ROOTFS/sys" 2>/dev/null || true
umount -lf "$ROOTFS/proc" 2>/dev/null || true
umount -lf "$ROOTFS/dev/pts" 2>/dev/null || true
umount -lf "$ROOTFS/dev" 2>/dev/null || true
rm -f "$ROOTFS/tmp/chroot_setup.sh"

# 4. Extract Kernel & Initrd for Bootloader
echo ">> Extracting kernel and initramfs for live boot..."
VMLINUZ=$(ls -1 "$ROOTFS/boot"/vmlinuz-* 2>/dev/null | sort -V | tail -n 1)
INITRD=$(ls -1 "$ROOTFS/boot"/initrd.img-* 2>/dev/null | sort -V | tail -n 1)

if [ -z "$VMLINUZ" ] || [ -z "$INITRD" ]; then
    echo "[Error] Kernel or initramfs not found in rootfs boot directory." >&2
    exit 1
fi

cp "$VMLINUZ" "$ISODIR/live/vmlinuz"
cp "$INITRD" "$ISODIR/live/initrd"

# 5. Compress SquashFS (zstd high compression)
echo ">> Generating compressed live filesystem (zstd high-density)..."
mksquashfs "$ROOTFS" "$ISODIR/live/filesystem.squashfs" \
    -comp zstd \
    -Xcompression-level 19 \
    -noappend \
    -e boot

# 6. Configure GRUB Live Bootloader
echo ">> Configuring GRUB bootloader..."
cat << 'EOF' > "$ISODIR/boot/grub/grub.cfg"
set default="0"
set timeout=3

search --set=root --file /live/vmlinuz

insmod all_video
insmod gfxterm

set menu_color_normal=white/black
set menu_color_highlight=black/cyan

menuentry "VDE Live (Victorious Desktop Environment) - Ultra-lightweight" {
    linux /live/vmlinuz boot=live quiet splash loglevel=3 rd.systemd.show_status=false ---
    initrd /live/initrd
}

menuentry "VDE Live (Safe Graphics / Software Rendering)" {
    linux /live/vmlinuz boot=live nomodeset quiet splash ---
    initrd /live/initrd
}

menuentry "Reboot System" {
    reboot
}
EOF

# 7. Create Hybrid Bootable ISO with xorriso
echo ">> Creating bootable hybrid ISO image via xorriso..."
xorriso -as mkisofs \
    -iso-level 3 \
    -full-iso9660-filenames \
    -volid "VDE_LIVE" \
    -eltorito-boot boot/grub/bios.img \
    -no-emul-boot \
    -boot-load-size 4 \
    -boot-info-table \
    --eltorito-catalog boot/grub/boot.cat \
    -output "$OUTPUT_ISO" \
    -graft-points \
    "$ISODIR" 2>/dev/null || \
grub-mkrescue -o "$OUTPUT_ISO" "$ISODIR"

echo "=========================================================="
echo ">> Build Complete!"
echo ">> ISO location: $OUTPUT_ISO"
echo ">> Size: $(du -h "$OUTPUT_ISO" 2>/dev/null | awk '{print $1}')"
echo "=========================================================="
