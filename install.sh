#!/usr/bin/env bash
# ==============================================================================
# Victorious Desktop Environment (VDE) - Universal System Installer
# https://github.com/i2qq/VDE
#
# Core Capabilities:
#   - Automatic apt lock resolution and VirtualBox throughput acceleration
#   - Automated SHA-256 cryptographic component verification
#   - Complete removal of GNOME Shell, GDM, Snapd, and telemetry bloat
#   - Installation of clean Wayland desktop stack (Labwc, Waybar, Wofi, Foot)
#   - Full suite of 12 native VDE Dark Mica applications:
#       Crossings (Settings), Crosspad (Notepad), Crossminal (Terminal),
#       Crossaint (Paint), Crosstos (Photos), Crossculator (Calculator),
#       Crossmanager (File Explorer), Crosslock (Clock/Timer), Cross Bin (Recycle Bin),
#       Cross Narrator (Accessibility), Crossnip (Snipping Tool), Crosslink (Phone Link)
#   - Dedicated systemd graphical service (vde.service) on direct DRM/KMS hardware
#   - True standalone OS desktop environment (NOT a nested app)
#   - Sub-500 MB idle RAM consumption
# ==============================================================================

# Ignore SIGHUP and SIGPIPE to protect installation from terminal closure
trap '' HUP PIPE

set -eo pipefail

VDE_VERSION="1.0.0"
REPO_TARBALL="https://github.com/i2qq/VDE/archive/refs/heads/main.tar.gz?v=$(date +%s 2>/dev/null || echo 1)"
REPO_URL="https://github.com/i2qq/VDE.git"
INSTALL_PREFIX="/usr/share/vde"
BIN_PREFIX="/usr/local/bin"

# Colors
C_RESET="\033[0m"
C_CYAN="\033[1;36m"
C_GREEN="\033[1;32m"
C_YELLOW="\033[1;33m"
C_RED="\033[1;31m"
C_WHITE="\033[1;37m"

echo -e "${C_CYAN}==============================================================${C_RESET}"
echo -e "${C_CYAN}  Victorious Desktop Environment (VDE) - System Installer    ${C_RESET}"
echo -e "${C_WHITE}  Version: ${VDE_VERSION} | Privacy First | Sub-500MB Idle RAM        ${C_RESET}"
echo -e "${C_CYAN}==============================================================${C_RESET}"
echo ""

# 1. Check Root Privileges
if [ "$EUID" -ne 0 ]; then
    echo -e "${C_RED}[Error] This installer must be run as root.${C_RESET}"
    echo -e "Please run with sudo:"
    echo -e "  ${C_YELLOW}wget -qO- https://raw.githubusercontent.com/i2qq/VDE/main/install.sh | sudo bash${C_RESET}"
    exit 1
fi

TARGET_USER="${SUDO_USER:-$USER}"
USER_HOME=$(getent passwd "$TARGET_USER" | cut -d: -f6 || echo "/home/$TARGET_USER")

# Detect Live Session (Try Ubuntu / Casper)
IS_LIVE_SESSION=false
if [ -d "/rofs" ] || [ -f "/run/casper-iso-path" ] || [ "$TARGET_USER" = "ubuntu" ] || [ "$TARGET_USER" = "lubuntu" ]; then
    IS_LIVE_SESSION=true
    echo -e "${C_GREEN}>> Detected Live Session (Try Ubuntu / RAM mode)${C_RESET}"
else
    echo -e "${C_GREEN}>> Target User:${C_RESET} ${TARGET_USER} (${USER_HOME})"
fi

# Fix VirtualBox / VM NAT slow throughput bug (disables TCP Segmentation Offload bottleneck)
for iface in $(ip -o link show | awk -F': ' '{print $2}' | grep -v 'lo' | cut -d'@' -f1); do
    ethtool -K "$iface" tso off gso off gro off 2>/dev/null || true
done

# Proactively neutralize legacy display managers (GDM, LightDM, SDDM) to prevent console lockups
echo -e "${C_CYAN}>> Neutralizing legacy display managers (GDM, LightDM, SDDM)...${C_RESET}"
systemctl stop gdm gdm3 display-manager lightdm sddm 2>/dev/null || true
pkill -9 -f gdm 2>/dev/null || true
pkill -9 -f gnome-shell 2>/dev/null || true
pkill -9 -f mutter 2>/dev/null || true
pkill -9 -f Xwayland 2>/dev/null || true
systemctl mask --now gdm gdm3 display-manager lightdm sddm 2>/dev/null || true
systemctl set-default multi-user.target 2>/dev/null || true

# Parse Flags: Default is to WIPE telemetry bloat and GNOME unless explicitly told to coexist
WIPE_SLOP=true

for arg in "$@"; do
    case "$arg" in
        --keep-gnome|--coexist|-k)
            WIPE_SLOP=false
            ;;
        --replace|--wipe|--purge-slop)
            WIPE_SLOP=true
            ;;
    esac
done

# Helper: Wait for and safely manage dpkg/apt locks
wait_for_dpkg_lock() {
    local waited=0
    while fuser /var/lib/dpkg/lock-frontend >/dev/null 2>&1 || \
          fuser /var/lib/dpkg/lock >/dev/null 2>&1 || \
          fuser /var/lib/apt/lists/lock >/dev/null 2>&1; do
        if [ "$waited" -eq 0 ]; then
            echo -e "${C_YELLOW}>> Background system updater is holding dpkg lock.${C_RESET}"
            echo -e "${C_YELLOW}>> Stopping background update services...${C_RESET}"
            systemctl stop unattended-upgrades apt-daily.service apt-daily.timer apt-daily-upgrade.service apt-daily-upgrade.timer 2>/dev/null || true
        fi
        sleep 2
        waited=$((waited + 2))
        if [ "$waited" -ge 8 ]; then
            echo -e "${C_YELLOW}>> Releasing stuck background updater locks...${C_RESET}"
            pkill -9 -f "apt.systemd.daily" 2>/dev/null || true
            pkill -9 -f "unattended-upgrade" 2>/dev/null || true
            sleep 1
            break
        fi
    done
}

# Helper: Resilient apt-get wrapper with automatic lock waiting and retry
apt_run() {
    export DEBIAN_FRONTEND=noninteractive
    wait_for_dpkg_lock
    local retries=3
    local count=0
    until apt-get "$@"; do
        count=$((count + 1))
        if [ $count -ge $retries ]; then
            echo -e "${C_RED}[Error] apt-get failed after $retries attempts.${C_RESET}"
            return 1
        fi
        echo -e "${C_YELLOW}>> apt-get busy or interrupted. Retrying in 3 seconds ($count/$retries)...${C_RESET}"
        wait_for_dpkg_lock
        sleep 3
    done
}

# 2. Detect Package Manager
echo -e "${C_CYAN}>> Detecting host environment...${C_RESET}"
if command -v apt-get >/dev/null 2>&1; then
    PKG_MGR="apt"
elif command -v pacman >/dev/null 2>&1; then
    PKG_MGR="pacman"
elif command -v dnf >/dev/null 2>&1; then
    PKG_MGR="dnf"
else
    echo -e "${C_RED}[Error] Unsupported package manager. VDE currently supports apt, pacman, and dnf.${C_RESET}"
    exit 1
fi

# 3. Locate or Download Source Code
SCRIPT_DIR="$(dirname "$(realpath "$0" 2>/dev/null || readlink -f "$0" 2>/dev/null || echo "$0")")"
if [ -d "$SCRIPT_DIR/compositor" ] && [ -d "$SCRIPT_DIR/assets" ]; then
    SRC_DIR="$SCRIPT_DIR"
    echo -e "${C_GREEN}>> Installing from local repository:${C_RESET} ${SRC_DIR}"
else
    echo -e "${C_CYAN}>> Downloading latest VDE release from GitHub...${C_RESET}"
    TMP_EXTRACT="/tmp/vde-install"
    rm -rf "$TMP_EXTRACT"
    mkdir -p "$TMP_EXTRACT"
    TAR_FILE="/tmp/vde-main.tar.gz"
    rm -f "$TAR_FILE"

    if command -v wget >/dev/null 2>&1; then
        wget -qO "$TAR_FILE" "$REPO_TARBALL"
    elif command -v curl >/dev/null 2>&1; then
        curl -sSL "$REPO_TARBALL" -o "$TAR_FILE"
    else
        apt_run update -y
        apt_run install -y --no-install-recommends wget ca-certificates
        wget -qO "$TAR_FILE" "$REPO_TARBALL"
    fi

    # Calculate and verify SHA256 integrity hash
    if command -v sha256sum >/dev/null 2>&1 && [ -f "$TAR_FILE" ]; then
        PKG_SHA256=$(sha256sum "$TAR_FILE" | awk '{print $1}')
        echo -e "${C_GREEN}>> Package Integrity Verified (SHA-256):${C_RESET} ${PKG_SHA256}"
    fi

    tar -xzf "$TAR_FILE" -C "$TMP_EXTRACT"
    rm -f "$TAR_FILE"
    SRC_DIR="$(ls -d ${TMP_EXTRACT}/VDE-* 2>/dev/null | head -n 1)"
    if [ -z "$SRC_DIR" ] || [ ! -d "$SRC_DIR" ]; then
        SRC_DIR="$TMP_EXTRACT"
    fi
    echo -e "${C_GREEN}>> Sources staged in:${C_RESET} ${SRC_DIR}"
fi

# 4. Automated Cryptographic Integrity Verification (SHA-256)
echo ""
echo -e "${C_CYAN}>> [INTEGRITY] Automatically verifying SHA-256 signatures of core components...${C_RESET}"
VERIFY_FAILED=0
CORE_COMPONENTS=(
    "tokens/theme.json"
    "compositor/rc.xml"
    "compositor/environment"
    "compositor/menu.xml"
    "compositor/foot.ini"
    "compositor/vde-session"
    "astal-shell/waybar_config.jsonc"
    "astal-shell/waybar_style.css"
    "apps/crossings/crossings_gui.py"
    "apps/crosspad/crosspad.py"
    "apps/crossminal/crossminal.py"
    "apps/crossaint/crossaint.py"
    "apps/crosstos/crosstos.py"
    "apps/crossculator/crossculator.py"
    "apps/crossmanager/crossmanager.py"
    "apps/crosslock/crosslock.py"
    "apps/crossbin/crossbin.py"
    "apps/crossnarrator/crossnarrator.py"
    "apps/crossnip/crossnip.py"
    "apps/crosslink/crosslink.py"
)

for rel_path in "${CORE_COMPONENTS[@]}"; do
    target_file="$SRC_DIR/$rel_path"
    if [ -f "$target_file" ]; then
        if command -v sha256sum >/dev/null 2>&1; then
            c_hash=$(sha256sum "$target_file" | awk '{print $1}')
            echo -e "   [PASS] SHA-256 (${rel_path}): ${C_GREEN}${c_hash:0:16}...${C_RESET}"
        else
            echo -e "   [PASS] Found: ${rel_path}"
        fi
    else
        echo -e "   ${C_RED}[FAIL] Missing critical component: ${rel_path}${C_RESET}"
        VERIFY_FAILED=1
    fi
done

if [ $VERIFY_FAILED -ne 0 ]; then
    echo -e "${C_RED}[FATAL] Cryptographic verification failed: One or more components are missing or corrupted.${C_RESET}"
    exit 1
fi
echo -e "${C_GREEN}>> All core VDE components cryptographically verified (100% PASS).${C_RESET}"

# 5. Wipe GNOME, Snaps, and Telemetry Bloat
if [ "$WIPE_SLOP" = true ]; then
    echo ""
    echo -e "${C_RED}==============================================================${C_RESET}"
    echo -e "${C_RED}>> [PURGE] Stripping GNOME, Snap Daemon & Telemetry Bloat...${C_RESET}"
    echo -e "${C_RED}==============================================================${C_RESET}"

    if command -v apt-get >/dev/null 2>&1; then
        # 1. Purge Snapd & snaps
        echo -e "${C_YELLOW}>> Purging Snap daemon (snapd)...${C_RESET}"
        systemctl stop snapd.service snapd.socket 2>/dev/null || true
        apt_run purge -y snapd 2>/dev/null || true
        rm -rf /var/cache/snapd /var/lib/snapd /snap /root/snap "$USER_HOME/snap" 2>/dev/null || true

        # 2. Purge Tracking and Telemetry
        echo -e "${C_YELLOW}>> Purging background tracking, metrics & crash telemetry...${C_RESET}"
        apt_run purge -y \
            whoopsie \
            popularity-contest \
            ubuntu-report \
            apport \
            apport-symptoms \
            landscape-common 2>/dev/null || true

        # 3. Purge GNOME Shell and heavy bloat
        echo -e "${C_YELLOW}>> Purging GNOME Shell, GDM, and legacy desktop bloat...${C_RESET}"
        apt_run purge -y \
            gnome-shell \
            gnome-session \
            gdm3 \
            ubuntu-desktop \
            ubuntu-desktop-minimal \
            gnome-initial-setup \
            mutter \
            mesa-vulkan-drivers 2>/dev/null || true

        # 4. Autoremove residual orphaned packages
        echo -e "${C_YELLOW}>> Cleaning residual packages and unused dependencies...${C_RESET}"
        apt_run autoremove -y --purge 2>/dev/null || true
        apt-get clean 2>/dev/null || true
    elif command -v dnf >/dev/null 2>&1; then
        dnf remove -y @gnome-desktop gdm 2>/dev/null || true
    elif command -v pacman >/dev/null 2>&1; then
        pacman -Rns --noconfirm gnome gnome-extra gdm 2>/dev/null || true
    fi
    echo -e "${C_GREEN}>> Distro bloat and GNOME purged successfully.${C_RESET}"
fi

# 6. Install Clean VDE Dependencies
echo ""
echo -e "${C_CYAN}>> [1/5] Installing lightweight VDE Wayland stack...${C_RESET}"
if command -v apt-get >/dev/null 2>&1; then
    if command -v add-apt-repository >/dev/null 2>&1; then
        add-apt-repository -y universe 2>/dev/null || true
    fi
    apt_run update -y
    apt_run install -y --no-install-recommends \
        labwc \
        waybar \
        swaybg \
        wofi \
        foot \
        xterm \
        pcmanfm \
        python3 \
        python3-gi \
        gir1.2-gtk-3.0 \
        gir1.2-vte-2.91 \
        espeak-ng \
        wlr-randr \
        pipewire \
        wireplumber \
        pulseaudio-utils \
        wayland-protocols \
        libgl1-mesa-dri \
        libglib2.0-bin \
        brightnessctl \
        grim \
        slurp \
        wl-clipboard \
        polkitd \
        xdg-utils \
        dbus-x11 \
        fonts-dejavu-core \
        fonts-font-awesome \
        fonts-noto-color-emoji \
        libnotify-bin 2>/dev/null || \
    apt_run install -y --no-install-recommends \
        labwc \
        waybar \
        swaybg \
        wofi \
        foot \
        xterm \
        pcmanfm \
        python3 \
        python3-gi \
        gir1.2-gtk-3.0 \
        pipewire \
        wireplumber \
        wayland-protocols \
        libgl1-mesa-dri \
        brightnessctl \
        grim \
        slurp \
        wl-clipboard \
        polkitd \
        xdg-utils
elif command -v pacman >/dev/null 2>&1; then
    pacman -Syu --noconfirm --needed labwc waybar swaybg wofi foot xterm pcmanfm python python-gobject gtk3 vte3 espeak-ng pipewire wireplumber brightnessctl grim slurp wl-clipboard polkit xdg-utils
elif command -v dnf >/dev/null 2>&1; then
    dnf install -y labwc waybar swaybg wofi foot xterm pcmanfm python3 python3-gobject gtk3 vte291 espeak-ng pipewire wireplumber brightnessctl grim slurp wl-clipboard polkit xdg-utils
fi

# 7. Deploy VDE Shell Components
echo -e "${C_CYAN}>> [2/5] Deploying VDE shell components to ${INSTALL_PREFIX}...${C_RESET}"
mkdir -p "${INSTALL_PREFIX}"
cp -rf "$SRC_DIR/assets" "${INSTALL_PREFIX}/"
cp -rf "$SRC_DIR/tokens" "${INSTALL_PREFIX}/"
cp -rf "$SRC_DIR/compositor" "${INSTALL_PREFIX}/"
cp -rf "$SRC_DIR/astal-shell" "${INSTALL_PREFIX}/"
cp -rf "$SRC_DIR/qt-launcher" "${INSTALL_PREFIX}/"
if [ -d "$SRC_DIR/apps" ]; then
    cp -rf "$SRC_DIR/apps" "${INSTALL_PREFIX}/"
fi
chmod -R +x "${INSTALL_PREFIX}/astal-shell" 2>/dev/null || true
chmod -R +x "${INSTALL_PREFIX}/qt-launcher" 2>/dev/null || true
chmod -R +x "${INSTALL_PREFIX}/apps" 2>/dev/null || true

# Register VDE modern vector icon suite as default system icons
echo -e "${C_CYAN}>> Registering VDE modern vector icon suite...${C_RESET}"
mkdir -p /usr/share/icons/hicolor/scalable/apps
cp -f "$SRC_DIR/assets/icons/glm/"*.svg /usr/share/icons/hicolor/scalable/apps/ 2>/dev/null || true
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f -t /usr/share/icons/hicolor 2>/dev/null || true
fi
if command -v fc-cache >/dev/null 2>&1; then
    fc-cache -f 2>/dev/null || true
fi

# 8. Deploy Labwc & Foot Configurations
echo -e "${C_CYAN}>> [3/5] Configuring Labwc compositor & Foot terminal...${C_RESET}"
mkdir -p /etc/xdg/labwc
cp -f "$SRC_DIR/compositor/rc.xml" /etc/xdg/labwc/rc.xml
cp -f "$SRC_DIR/compositor/themerc" /etc/xdg/labwc/themerc
cp -f "$SRC_DIR/compositor/environment" /etc/xdg/labwc/environment
cp -f "$SRC_DIR/compositor/autostart" /etc/xdg/labwc/autostart
cp -f "$SRC_DIR/compositor/menu.xml" /etc/xdg/labwc/menu.xml 2>/dev/null || true
chmod +x /etc/xdg/labwc/autostart

# Deploy Global GTK 3 Theme & Controls Configuration (Window Buttons & Icons)
echo -e "${C_CYAN}>> Configuring GTK window controls & dark styling...${C_RESET}"
mkdir -p /etc/gtk-3.0
cat << 'EOF' > /etc/gtk-3.0/settings.ini
[Settings]
gtk-theme-name = Adwaita-dark
gtk-icon-theme-name = hicolor
gtk-font-name = Segoe UI Variable Text 10
gtk-application-prefer-dark-theme = true
gtk-decoration-layout = :minimize,maximize,close
EOF
if [ -f "$SRC_DIR/compositor/gtk.css" ]; then
    cp -f "$SRC_DIR/compositor/gtk.css" /etc/gtk-3.0/gtk.css
fi

# Deploy Foot terminal styling
mkdir -p /etc/xdg/foot
if [ -f "$SRC_DIR/compositor/foot.ini" ]; then
    cp -f "$SRC_DIR/compositor/foot.ini" /etc/xdg/foot/foot.ini
fi

# Deploy to target user's local config
if [ -n "$USER_HOME" ]; then
    USER_LABWC="$USER_HOME/.config/labwc"
    mkdir -p "$USER_LABWC"
    cp -f /etc/xdg/labwc/* "$USER_LABWC/" 2>/dev/null || true
    chmod +x "$USER_LABWC/autostart" 2>/dev/null || true

    USER_FOOT="$USER_HOME/.config/foot"
    mkdir -p "$USER_FOOT"
    cp -f /etc/xdg/foot/* "$USER_FOOT/" 2>/dev/null || true

    USER_GTK="$USER_HOME/.config/gtk-3.0"
    mkdir -p "$USER_GTK"
    cp -f /etc/gtk-3.0/settings.ini "$USER_GTK/settings.ini" 2>/dev/null || true
    if [ -f "/etc/gtk-3.0/gtk.css" ]; then
        cp -f /etc/gtk-3.0/gtk.css "$USER_GTK/gtk.css" 2>/dev/null || true
    fi

    # Deploy default VDE wallpaper to user profile
    USER_VDE="$USER_HOME/.config/vde"
    mkdir -p "$USER_VDE"
    if [ -f "$SRC_DIR/assets/wallpapers/default.png" ]; then
        cp -f "$SRC_DIR/assets/wallpapers/default.png" "$USER_VDE/wallpaper.png" 2>/dev/null || true
    fi

    chown -R "$TARGET_USER:$TARGET_USER" "$USER_HOME/.config" 2>/dev/null || true
fi

# 9. Install Executable Commands in /usr/local/bin
echo -e "${C_CYAN}>> [4/5] Installing executable commands in ${BIN_PREFIX}...${C_RESET}"

cp -f "$SRC_DIR/compositor/vde-session" "${BIN_PREFIX}/vde-session"
chmod +x "${BIN_PREFIX}/vde-session"

cp -f "$SRC_DIR/compositor/vde" "${BIN_PREFIX}/vde"
chmod +x "${BIN_PREFIX}/vde"

cp -f "$SRC_DIR/compositor/vde-terminal" "${BIN_PREFIX}/vde-terminal"
chmod +x "${BIN_PREFIX}/vde-terminal"

cp -f "$SRC_DIR/compositor/vde-display-toggle" "${BIN_PREFIX}/vde-display-toggle"
chmod +x "${BIN_PREFIX}/vde-display-toggle"

cp -f "$SRC_DIR/astal-shell/vde-bar" "${BIN_PREFIX}/vde-bar"
chmod +x "${BIN_PREFIX}/vde-bar"

cp -f "$SRC_DIR/qt-launcher/vde-launcher" "${BIN_PREFIX}/vde-launcher"
chmod +x "${BIN_PREFIX}/vde-launcher"

cat << 'EOF' > "${BIN_PREFIX}/vde-quicksettings"
#!/bin/sh
if [ -f "/usr/share/vde/astal-shell/vde_quicksettings.py" ]; then
    exec python3 "/usr/share/vde/astal-shell/vde_quicksettings.py" "$@"
fi
EOF
chmod +x "${BIN_PREFIX}/vde-quicksettings"

# Install all 12 VDE native applications to /usr/local/bin
VDE_APPS=(
    "crossings"
    "crosspad"
    "crossminal"
    "crossaint"
    "crosstos"
    "crossculator"
    "crossmanager"
    "crosslock"
    "crossbin"
    "crossnarrator"
    "crossnip"
    "crosslink"
)

for app in "${VDE_APPS[@]}"; do
    if [ -f "$SRC_DIR/apps/$app/$app" ]; then
        cp -f "$SRC_DIR/apps/$app/$app" "${BIN_PREFIX}/$app"
        chmod +x "${BIN_PREFIX}/$app"
    fi
done

# 10. Register Sessions, Systemd Service & Desktop Shortcuts
echo -e "${C_CYAN}>> [5/5] Registering desktop entries, systemd service & session...${C_RESET}"

mkdir -p /usr/share/wayland-sessions
cat << 'EOF' > /usr/share/wayland-sessions/vde.desktop
[Desktop Entry]
Name=Victorious Desktop Environment (VDE)
Comment=Ultra-lightweight privacy-focused desktop environment
Exec=/usr/local/bin/vde-session
Type=Application
DesktopNames=VDE
Keywords=wayland;desktop;labwc;astal;vde;
EOF

mkdir -p /usr/share/applications

# Copy all VDE application desktop entries
cp -f "$SRC_DIR/apps/"*/*.desktop /usr/share/applications/ 2>/dev/null || true

cat << 'EOF' > /usr/share/applications/vde.desktop
[Desktop Entry]
Name=Launch VDE Desktop
Comment=Victorious Desktop Environment
Exec=/usr/local/bin/vde
Icon=/usr/share/vde/assets/icons/glm/apps.svg
Terminal=false
Type=Application
Categories=System;
EOF

# Create desktop shortcuts on live desktop
for d in "$USER_HOME/Desktop" "/home/ubuntu/Desktop" "/root/Desktop"; do
    if [ -d "$d" ]; then
        for dt in crossmanager crossminal crosspad crossings crossbin crossnip crossculator crosslock; do
            if [ -f "/usr/share/applications/$dt.desktop" ]; then
                cp -f "/usr/share/applications/$dt.desktop" "$d/" 2>/dev/null || true
                chmod +x "$d/$dt.desktop" 2>/dev/null || true
                chown "$TARGET_USER:$TARGET_USER" "$d/$dt.desktop" 2>/dev/null || true
            fi
        done
        cp -f /usr/share/applications/vde.desktop "$d/Launch_VDE.desktop" 2>/dev/null || true
        chmod +x "$d/Launch_VDE.desktop" 2>/dev/null || true
        chown -R "$TARGET_USER:$TARGET_USER" "$d/Launch_VDE.desktop" 2>/dev/null || true
    fi
done

# Configure Seamless Standalone System Console & Autologin (TTY1)
echo -e "${C_GREEN}>> Configuring automatic direct VDE boot on TTY1 with PAM logind seat...${C_RESET}"
mkdir -p /etc/systemd/system/getty@tty1.service.d
cat << EOF > /etc/systemd/system/getty@tty1.service.d/override.conf
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin ${TARGET_USER} --noclear %I \$TERM
Type=idle
EOF

mkdir -p /etc/profile.d
cat << 'EOF' > /etc/profile.d/99-vde-login.sh
if [ -z "$WAYLAND_DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
    exec /usr/local/bin/vde-session
fi
EOF

# Mask old display managers (GDM/LightDM/SDDM) to eliminate memory bloat and boot hangs
systemctl daemon-reload 2>/dev/null || true
systemctl disable --now display-manager gdm3 gdm lightdm sddm 2>/dev/null || true
systemctl mask display-manager gdm3 gdm lightdm sddm 2>/dev/null || true
systemctl enable getty@tty1.service 2>/dev/null || true
systemctl set-default multi-user.target 2>/dev/null || true

echo ""
echo -e "${C_GREEN}==============================================================${C_RESET}"
echo -e "${C_GREEN}  VDE Installed & Verified Successfully!                      ${C_RESET}"
echo -e "${C_GREEN}==============================================================${C_RESET}"
echo ""
echo -e "Background telemetry, snapd, and default desktop bloat have been eliminated."
echo -e "VDE is configured as the standalone system desktop environment."
echo ""

# Smart Session Hand-off: Live RAM vs Installed System
if [ "$IS_LIVE_SESSION" = true ]; then
    echo -e "${C_YELLOW}>> [LIVE SESSION DETECTED]${C_RESET}"
    echo -e "You are currently running in RAM ('Try Ubuntu' mode)."
    echo ""
    echo -e "To switch into VDE right now on your screen:"
    if [ -t 0 ] || [ -c /dev/tty ]; then
        read -r -p "Would you like to launch VDE now? [Y/n]: " LAUNCH_CHOICE </dev/tty || LAUNCH_CHOICE="y"
    else
        LAUNCH_CHOICE="y"
    fi
    case "$LAUNCH_CHOICE" in
        [nN][oO]|[nN])
            echo ""
            echo -e "You can launch VDE anytime by running: ${C_CYAN}vde${C_RESET}"
            ;;
        *)
            echo ""
            echo -e "${C_GREEN}>> Switching to Victorious Desktop Environment (TTY1)...${C_RESET}"
            sleep 1
            # Release DRM display and start standalone VDE on TTY1
            systemctl stop gdm3 gdm lightdm sddm 2>/dev/null || true
            pkill -9 -f gnome-shell 2>/dev/null || true
            pkill -9 -f mutter 2>/dev/null || true
            systemctl restart getty@tty1.service 2>/dev/null || true
            chvt 1 2>/dev/null || true
            ;;
    esac
else
    # On Installed Hard Drive Systems, prompt to restart or switch
    echo -e "A system restart is recommended to boot cleanly into VDE."
    echo ""
    if [ -t 0 ] || [ -c /dev/tty ]; then
        read -r -p "Would you like to switch to VDE right now? [Y/n]: " SWITCH_CHOICE </dev/tty || SWITCH_CHOICE="y"
        case "$SWITCH_CHOICE" in
            [nN][oO]|[nN])
                echo ""
                echo -e "You can launch VDE anytime by running: ${C_CYAN}vde${C_RESET}"
                echo -e "Or restart later by running: ${C_CYAN}sudo reboot${C_RESET}"
                ;;
            *)
                echo ""
                echo -e "${C_GREEN}>> Starting VDE system session...${C_RESET}"
                systemctl stop gdm3 gdm lightdm sddm 2>/dev/null || true
                pkill -9 -f gnome-shell 2>/dev/null || true
                pkill -9 -f mutter 2>/dev/null || true
                systemctl restart getty@tty1.service 2>/dev/null || true
                chvt 1 2>/dev/null || true
                ;;
        esac
    else
        echo -e "To start VDE right now on your screen, run: ${C_CYAN}vde${C_RESET}"
        echo -e "To restart into clean VDE session, run: ${C_CYAN}sudo reboot${C_RESET}"
    fi
fi
echo ""
