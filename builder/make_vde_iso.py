#!/usr/bin/env python3
r"""
VDE Live ISO Builder for Ubuntu Server (uS) Backbone
Generates a bootable hybrid ISO in C:\Users\Victor\ISO\Test\vde-live-amd64.iso
using C:\Users\Victor\ISO\ubuntu-26.04.1-live-server-amd64.iso as the template.
"""

import os
import sys
import shutil
import subprocess
import io
import pycdlib

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATE_ISO = r"C:\Users\Victor\ISO\ubuntu-26.04.1-live-server-amd64.iso"
OUTPUT_DIR = r"C:\Users\Victor\ISO\Test"
OUTPUT_ISO = os.path.join(OUTPUT_DIR, "vde-live-amd64.iso")
OVERLAY_DIR = os.path.join(ROOT_DIR, "builder", "vde_overlay")
SQUASHFS_FILE = os.path.join(ROOT_DIR, "builder", "vde.squashfs")

print("==========================================================")
print(" VDE Live ISO Builder (Ubuntu Server Backbone)")
print(f" Template ISO: {TEMPLATE_ISO}")
print(f" Output ISO:   {OUTPUT_ISO}")
print("==========================================================")

if not os.path.exists(TEMPLATE_ISO):
    print(f"[Error] Template ISO not found at {TEMPLATE_ISO}")
    sys.exit(1)

os.makedirs(OUTPUT_DIR, exist_ok=True)

# 1. Stage VDE Overlay Files
print(">> Staging VDE filesystem overlay...")
if os.path.exists(OVERLAY_DIR):
    shutil.rmtree(OVERLAY_DIR)

# System structure
usr_vde = os.path.join(OVERLAY_DIR, "usr", "share", "vde")
etc_labwc = os.path.join(OVERLAY_DIR, "etc", "xdg", "labwc")
usr_bin = os.path.join(OVERLAY_DIR, "usr", "local", "bin")
profile_d = os.path.join(OVERLAY_DIR, "etc", "profile.d")
getty_d = os.path.join(OVERLAY_DIR, "etc", "systemd", "system", "getty@tty1.service.d")
sudoers_d = os.path.join(OVERLAY_DIR, "etc", "sudoers.d")
etc_skel = os.path.join(OVERLAY_DIR, "etc", "skel")
desktop_dir = os.path.join(etc_skel, "Desktop")

for d in [usr_vde, etc_labwc, usr_bin, profile_d, getty_d, sudoers_d, desktop_dir]:
    os.makedirs(d, exist_ok=True)

# Copy VDE components into /usr/share/vde
for comp in ["assets", "tokens", "compositor", "astal-shell", "qt-launcher", "apps"]:
    src = os.path.join(ROOT_DIR, comp)
    if os.path.exists(src):
        dst = os.path.join(usr_vde, comp)
        shutil.copytree(src, dst)

# Copy Labwc configs into /etc/xdg/labwc
for cfg in ["rc.xml", "themerc", "autostart", "environment"]:
    src = os.path.join(ROOT_DIR, "compositor", cfg)
    if os.path.exists(src):
        shutil.copy2(src, os.path.join(etc_labwc, cfg))

# Create vde-session script
vde_session_path = os.path.join(usr_bin, "vde-session")
with open(vde_session_path, "w", encoding="utf-8", newline="\n") as f:
    f.write("""#!/usr/bin/env bash
# VDE Master Session Launcher
export XDG_CURRENT_DESKTOP=VDE
export XDG_SESSION_DESKTOP=VDE
export WAYLAND_DISPLAY=wayland-0

echo ">> Starting Victorious Desktop Environment (VDE)..."
/usr/share/vde/astal-shell/vde-bar &
/usr/share/vde/qt-launcher/vde-launcher &

wait
""")

# Create wrappers in /usr/local/bin
with open(os.path.join(usr_bin, "vde-bar"), "w", encoding="utf-8", newline="\n") as f:
    f.write("""#!/usr/bin/env bash
exec /usr/share/vde/astal-shell/vde-bar "$@"
""")

with open(os.path.join(usr_bin, "vde-launcher"), "w", encoding="utf-8", newline="\n") as f:
    f.write("""#!/usr/bin/env bash
exec /usr/share/vde/qt-launcher/vde-launcher "$@"
""")

with open(os.path.join(usr_bin, "crossings"), "w", encoding="utf-8", newline="\n") as f:
    f.write("""#!/usr/bin/env bash
exec /usr/share/vde/apps/crossings/crossings "$@"
""")

# Create tty1 autologin override
with open(os.path.join(getty_d, "override.conf"), "w", encoding="utf-8", newline="\n") as f:
    f.write("""[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin vde --noclear %I $TERM
""")

# Create profile autostart for tty1
with open(os.path.join(profile_d, "99-vde-autostart.sh"), "w", encoding="utf-8", newline="\n") as f:
    f.write("""# Auto-launch VDE on tty1
if [ -z "$WAYLAND_DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
    echo "=========================================================="
    echo " Starting Victorious Desktop Environment (VDE)..."
    echo " Backbone: Ubuntu Server (Noble minimal)"
    echo "=========================================================="
    if command -v labwc >/dev/null 2>&1; then
        exec labwc -s /usr/local/bin/vde-session
    else
        echo "Labwc compositor ready. Run 'labwc -s /usr/local/bin/vde-session' to start."
    fi
fi
""")

# Sudoers without password
with open(os.path.join(sudoers_d, "vde"), "w", encoding="utf-8", newline="\n") as f:
    f.write("vde ALL=(ALL) NOPASSWD:ALL\n")

# Desktop shortcuts in /etc/skel/Desktop
with open(os.path.join(desktop_dir, "crossings.desktop"), "w", encoding="utf-8", newline="\n") as f:
    f.write("""[Desktop Entry]
Type=Application
Name=Crossings Settings
Comment=VDE System & Personalization Hub
Exec=/usr/local/bin/crossings
Icon=/usr/share/vde/assets/icons/glm/settings.svg
Terminal=false
Categories=Settings;DesktopSettings;
""")

print(">> Staging complete.")

# 2. Build SquashFS via WSL
print(">> Compressing overlay into squashfs...")
if os.path.exists(SQUASHFS_FILE):
    os.remove(SQUASHFS_FILE)

# Convert path for WSL
overlay_wsl = OVERLAY_DIR.replace("\\", "/").replace("C:", "/mnt/c")
squash_wsl = SQUASHFS_FILE.replace("\\", "/").replace("C:", "/mnt/c")

cmd = ["wsl", "mksquashfs", overlay_wsl, squash_wsl, "-comp", "zstd", "-noappend"]
subprocess.check_call(cmd)

squash_size_kb = os.path.getsize(SQUASHFS_FILE) / 1024
print(f">> Created vde.squashfs ({squash_size_kb:.1f} KB)")

# 3. Patch Ubuntu Server ISO
print(f">> Opening base Ubuntu Server ISO: {TEMPLATE_ISO}")
iso = pycdlib.PyCdlib()
iso.open(TEMPLATE_ISO)

# Customized GRUB menu
print(">> Customizing GRUB bootloader menu...")
new_grub = b"""set timeout=5
loadfont unicode

set menu_color_normal=white/black
set menu_color_highlight=black/cyan

menuentry "Victorious Desktop Environment (VDE) - Live on Ubuntu Server" {
    set gfxpayload=keep
    linux  /casper/vmlinuz quiet splash systemd.mask=subiquity.service systemd.mask=subiquity-server.service --- 
    initrd /casper/initrd
}

menuentry "Victorious Desktop Environment (VDE) - Safe Graphics Mode" {
    set gfxpayload=keep
    linux  /casper/vmlinuz nomodeset systemd.mask=subiquity.service systemd.mask=subiquity-server.service --- 
    initrd /casper/initrd
}

menuentry "Ubuntu Server Standard Installer (Subiquity)" {
    set gfxpayload=keep
    linux  /casper/vmlinuz --- 
    initrd /casper/initrd
}

grub_platform
if [ "$grub_platform" = "efi" ]; then
menuentry 'Boot from next volume' {
    exit 1
}
menuentry 'UEFI Firmware Settings' {
    fwsetup
}
fi
"""

grub_fp = io.BytesIO(new_grub)
iso.update_file_contents_fp(grub_fp, len(new_grub), iso_path='/BOOT/GRUB/GRUB.CFG;1')

# Add vde.squashfs into /CASPER
print(">> Injecting vde.squashfs into /casper...")
iso.add_file(SQUASHFS_FILE,
             iso_path='/CASPER/VDE.SQUASHFS;1',
             rr_name='vde.squashfs',
             joliet_path='/casper/vde.squashfs')

# Write output ISO
print(f">> Writing bootable ISO to {OUTPUT_ISO}...")
iso.write(OUTPUT_ISO)
iso.close()

iso_size_mb = os.path.getsize(OUTPUT_ISO) / (1024 * 1024)
print("==========================================================")
print(">> BUILD SUCCESSFUL!")
print(f">> Target ISO: {OUTPUT_ISO}")
print(f">> Size:       {iso_size_mb:.2f} MB")
print("==========================================================")
