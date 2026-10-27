#!/usr/bin/env bash
# VDE Live System Chroot Configuration Script
# Configures the minimalist rootfs for instant <3s autologin into VDE

set -eo pipefail

export DEBIAN_FRONTEND=noninteractive
export HOME=/root

echo "=========================================================="
echo ">> Running VDE Chroot Configuration..."
echo "=========================================================="

# 1. Hostname and Network Configuration
echo "vde-os" > /etc/hostname
cat << 'EOF' > /etc/hosts
127.0.0.1   localhost vde-os
::1         localhost ip6-localhost ip6-loopback
EOF

# 2. Package Management & Purge Telemetry / Snaps
echo ">> Purging Canonical snapd, telemetry, and tracking packages..."
apt-get update -y

# Mask and remove snapd and ubuntu-report
systemctl mask snapd.service snapd.socket snapd.seeded.service 2>/dev/null || true
apt-get purge -y snapd ubuntu-report whoopsie apport popularity-contest unattended-upgrades cloud-init 2>/dev/null || true
apt-mark hold snapd ubuntu-report whoopsie apport 2>/dev/null || true

# 3. Create 'vde' Live User
echo ">> Setting up 'vde' default user..."
if ! id -u vde >/dev/null 2>&1; then
    useradd -m -s /bin/bash -U -G sudo,video,audio,input,render vde
    echo "vde:vde" | chpasswd
fi

# 4. Passwordless Sudo for Live User
mkdir -p /etc/sudoers.d
cat << 'EOF' > /etc/sudoers.d/99-vde-live
vde ALL=(ALL) NOPASSWD: ALL
EOF
chmod 0440 /etc/sudoers.d/99-vde-live

# 5. Configure Instant Autologin on tty1
echo ">> Configuring systemd tty1 autologin..."
mkdir -p /etc/systemd/system/getty@tty1.service.d
cat << 'EOF' > /etc/systemd/system/getty@tty1.service.d/override.conf
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin vde --noclear %I $TERM
Type=simple
EOF

# 6. Configure Autostart of VDE Compositor from tty1
echo ">> Configuring user shell autostart into Labwc..."
cat << 'EOF' > /home/vde/.bash_profile
# Autostart VDE Wayland session on tty1 login
if [ -z "$WAYLAND_DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
    export XDG_CURRENT_DESKTOP=VDE:wlroots
    export XDG_SESSION_TYPE=wayland
    export QT_QPA_PLATFORM=wayland;xcb
    export GDK_BACKEND=wayland,x11
    export MOZ_ENABLE_WAYLAND=1
    exec labwc
fi
EOF
chown vde:vde /home/vde/.bash_profile
chmod 0644 /home/vde/.bash_profile

# 7. Install VDE configs into user profile
mkdir -p /home/vde/.config/labwc
if [ -d "/usr/share/vde/compositor" ]; then
    cp -r /usr/share/vde/compositor/* /home/vde/.config/labwc/
    chmod +x /home/vde/.config/labwc/autostart 2>/dev/null || true
fi
chown -R vde:vde /home/vde/.config

# 8. Enable Essential Systemd Services
systemctl enable NetworkManager.service 2>/dev/null || true
systemctl enable systemd-resolved.service 2>/dev/null || true

# 9. Clean up rootfs size
echo ">> Cleaning package caches..."
apt-get autoremove -y --purge
apt-get clean
rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /var/log/*

echo ">> Chroot setup successfully finished!"
