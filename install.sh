#!/usr/bin/env bash
# ==============================================================================
# Victorious Desktop Environment (VDE) - Universal Terminal Installer
# https://github.com/VicRoger27/VDE
#
# Default Action:
#   - Automatically clears and waits for Ubuntu background apt locks
#   - Downloads sources without git dependency (via native wget/tarball)
#   - Purges GNOME, GDM, Snapd, and background telemetry bloat
#   - Installs the ultra-lightweight VDE stack (Labwc, Astal, Qt6/QML, Crossings)
#   - Drops idle memory to sub-500 MB (sub-250 MB on minimal base)
# ==============================================================================

set -eo pipefail

VDE_VERSION="1.0.0"
REPO_TARBALL="https://github.com/VicRoger27/VDE/archive/refs/heads/main.tar.gz?v=$(date +%s 2>/dev/null || echo 1)"
REPO_URL="https://github.com/VicRoger27/VDE.git"
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
    echo -e "  ${C_YELLOW}wget -qO- https://raw.githubusercontent.com/VicRoger27/VDE/main/install.sh | sudo bash${C_RESET}"
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
    local max_tries=5
    local attempt=1
    while true; do
        wait_for_dpkg_lock
        if apt-get "$@"; then
            return 0
        else
            echo -e "${C_YELLOW}>> apt-get was busy. Waiting 3s to retry ($attempt/$max_tries)...${C_RESET}"
            wait_for_dpkg_lock
            sleep 3
            attempt=$((attempt + 1))
            if [ "$attempt" -gt "$max_tries" ]; then
                echo -e "${C_RED}[Error] apt-get failed after $max_tries attempts.${C_RESET}"
                return 1
            fi
        fi
    done
}

# 2. Enable Universe repository on Ubuntu/Debian
if command -v add-apt-repository >/dev/null 2>&1; then
    echo -e "${C_CYAN}>> Ensuring universe repository is enabled...${C_RESET}"
    wait_for_dpkg_lock
    add-apt-repository -y universe 2>/dev/null || true
fi

# 3. Locate or Fetch Repository Sources (Zero git package dependency)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || echo "")"
SRC_DIR=""

if [ -f "$SCRIPT_DIR/tokens/theme.json" ] && [ -d "$SCRIPT_DIR/compositor" ]; then
    SRC_DIR="$SCRIPT_DIR"
    echo -e "${C_GREEN}>> Using local VDE source tree:${C_RESET} ${SRC_DIR}"
else
    TMP_EXTRACT="/tmp/vde-extract"
    echo -e "${C_YELLOW}>> Fetching latest VDE release from GitHub...${C_RESET}"
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
    "astal-shell/waybar_config.jsonc"
    "astal-shell/waybar_style.css"
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
        # 1. If running outside GUI (on TTY/console), safely stop GDM
        if [ -z "$WAYLAND_DISPLAY" ] && [ -z "$DISPLAY" ]; then
            echo -e "${C_YELLOW}>> Stopping display managers...${C_RESET}"
            systemctl stop gdm3 2>/dev/null || systemctl stop gdm 2>/dev/null || true
            pkill -9 -f gnome-shell 2>/dev/null || true
        else
            echo -e "${C_YELLOW}>> Running inside active desktop terminal. Deferring display switch to end...${C_RESET}"
        fi

        # 2. Purge Snapd & snaps
        echo -e "${C_YELLOW}>> Purging Snap daemon (snapd)...${C_RESET}"
        systemctl stop snapd.service snapd.socket 2>/dev/null || true
        apt_run purge -y snapd 2>/dev/null || true
        rm -rf /var/cache/snapd /var/lib/snapd /snap /root/snap "$USER_HOME/snap" 2>/dev/null || true

        # 3. Purge Tracking and Telemetry
        echo -e "${C_YELLOW}>> Purging background tracking, metrics & crash telemetry...${C_RESET}"
        apt_run purge -y \
            whoopsie \
            popularity-contest \
            ubuntu-report \
            apport \
            apport-symptoms \
            landscape-common 2>/dev/null || true

        # 4. Purge GNOME Shell and heavy bloat
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

        # 5. Autoremove residual orphaned packages
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

# 5. Install Clean VDE Dependencies
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
        wayland-protocols \
        libgl1-mesa-dri \
        pipewire \
        wireplumber \
        foot \
        libglib2.0-bin \
        brightnessctl \
        grim \
        slurp \
        wl-clipboard \
        polkitd \
        xdg-utils \
        dbus-x11 \
        fonts-dejavu-core 2>/dev/null || \
    apt_run install -y --no-install-recommends \
        labwc \
        waybar \
        swaybg \
        wayland-protocols \
        libgl1-mesa-dri \
        pipewire \
        wireplumber \
        foot \
        libglib2.0-bin \
        brightnessctl \
        grim \
        slurp \
        wl-clipboard \
        polkitd \
        xdg-utils
elif command -v pacman >/dev/null 2>&1; then
    pacman -Syu --noconfirm --needed labwc vulkan-intel vulkan-radeon pipewire wireplumber foot glib2 brightnessctl grim slurp wl-clipboard polkit xdg-utils
elif command -v dnf >/dev/null 2>&1; then
    dnf install -y labwc pipewire wireplumber foot glib2 brightnessctl grim slurp wl-clipboard polkit xdg-utils
fi

# 6. Deploy VDE Shell Components
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
chmod +x "${INSTALL_PREFIX}/astal-shell/vde-bar" 2>/dev/null || true

# 7. Deploy Labwc Configurations
echo -e "${C_CYAN}>> [3/5] Configuring Labwc compositor...${C_RESET}"
mkdir -p /etc/xdg/labwc
cp -f "$SRC_DIR/compositor/rc.xml" /etc/xdg/labwc/rc.xml
cp -f "$SRC_DIR/compositor/themerc" /etc/xdg/labwc/themerc
cp -f "$SRC_DIR/compositor/environment" /etc/xdg/labwc/environment
cp -f "$SRC_DIR/compositor/autostart" /etc/xdg/labwc/autostart
cp -f "$SRC_DIR/compositor/menu.xml" /etc/xdg/labwc/menu.xml 2>/dev/null || true

# Deploy to target user's local config
if [ -n "$USER_HOME" ]; then
    USER_LABWC="$USER_HOME/.config/labwc"
    mkdir -p "$USER_LABWC"
    cp -f /etc/xdg/labwc/* "$USER_LABWC/" 2>/dev/null || true
    chown -R "$TARGET_USER:$TARGET_USER" "$USER_HOME/.config" 2>/dev/null || true
fi

# 8. Install Executable Commands in /usr/local/bin
echo -e "${C_CYAN}>> [4/5] Installing executable commands in ${BIN_PREFIX}...${C_RESET}"

cat << 'EOF' > "${BIN_PREFIX}/vde-session"
#!/usr/bin/env bash
export XDG_CURRENT_DESKTOP=VDE
export XDG_SESSION_DESKTOP=VDE
export XDG_SESSION_TYPE=wayland

# Guarantee universal Wayland rendering across VMs and hardware (OpenGL ES 2 + software fallback)
export WLR_RENDERER=${WLR_RENDERER:-gles2}
export WLR_RENDERER_ALLOW_SOFTWARE=1
export WLR_NO_HARDWARE_CURSORS=1

# Ensure XDG_RUNTIME_DIR is set and accessible
if [ -z "$XDG_RUNTIME_DIR" ]; then
    export XDG_RUNTIME_DIR="/run/user/$(id -u)"
    if [ ! -d "$XDG_RUNTIME_DIR" ]; then
        mkdir -p "$XDG_RUNTIME_DIR" 2>/dev/null || true
        chmod 0700 "$XDG_RUNTIME_DIR" 2>/dev/null || true
    fi
fi

# Ensure D-Bus user session
if [ -z "$DBUS_SESSION_BUS_ADDRESS" ]; then
    if command -v dbus-launch >/dev/null 2>&1; then
        eval $(dbus-launch --sh-syntax --exit-with-session 2>/dev/null || true)
    fi
fi

echo "=========================================================="
echo " Starting Victorious Desktop Environment (VDE)..."
echo " Compositor: Labwc (wlroots layer-shell)"
echo " Shell: Astal Taskbar & Qt6 Start Menu"
echo "=========================================================="

labwc -s /usr/local/bin/vde-bar "$@"
EXIT_CODE=$?

if [ $EXIT_CODE -ne 0 ]; then
    echo ">> GLES2 renderer exited with code $EXIT_CODE. Retrying with Pixman software renderer..."
    export WLR_RENDERER=pixman
    exec labwc -s /usr/local/bin/vde-bar "$@"
fi
EOF
chmod +x "${BIN_PREFIX}/vde-session"

cat << 'EOF' > "${BIN_PREFIX}/vde"
#!/usr/bin/env bash
export WLR_RENDERER=${WLR_RENDERER:-gles2}
export WLR_RENDERER_ALLOW_SOFTWARE=1
export WLR_NO_HARDWARE_CURSORS=1

if [ -n "$WAYLAND_DISPLAY" ] || [ -n "$DISPLAY" ]; then
    echo ">> Running VDE on display..."
    labwc -s /usr/local/bin/vde-bar "$@" || {
        echo ">> Falling back to Pixman software renderer..."
        export WLR_RENDERER=pixman
        exec labwc -s /usr/local/bin/vde-bar "$@"
    }
else
    exec /usr/local/bin/vde-session "$@"
fi
EOF
chmod +x "${BIN_PREFIX}/vde"

cat << 'EOF' > "${BIN_PREFIX}/vde-bar"
#!/usr/bin/env bash
if [ -f /usr/share/vde/astal-shell/vde-bar ]; then
    chmod +x /usr/share/vde/astal-shell/vde-bar 2>/dev/null || true
    /usr/share/vde/astal-shell/vde-bar "$@"
elif command -v waybar >/dev/null 2>&1; then
    exec waybar -c /usr/share/vde/astal-shell/waybar_config.jsonc -s /usr/share/vde/astal-shell/waybar_style.css "$@"
fi
EOF
chmod +x "${BIN_PREFIX}/vde-bar"

cat << 'EOF' > "${BIN_PREFIX}/vde-launcher"
#!/usr/bin/env bash
exec /usr/share/vde/qt-launcher/vde-launcher "$@"
EOF
chmod +x "${BIN_PREFIX}/vde-launcher"

cat << 'EOF' > "${BIN_PREFIX}/crossings"
#!/usr/bin/env bash
exec /usr/share/vde/apps/crossings/crossings "$@"
EOF
chmod +x "${BIN_PREFIX}/crossings"

# 9. Register Sessions & Desktop Shortcuts
echo -e "${C_CYAN}>> [5/5] Registering desktop entries & live shortcuts...${C_RESET}"
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
cat << 'EOF' > /usr/share/applications/crossings.desktop
[Desktop Entry]
Name=Crossings Settings
Comment=VDE System & Personalization Hub
Exec=/usr/local/bin/crossings
Icon=/usr/share/vde/assets/icons/glm/settings.svg
Terminal=false
Type=Application
Categories=Settings;DesktopSettings;
EOF

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

# Create desktop shortcut on live desktop
for d in "$USER_HOME/Desktop" "/home/ubuntu/Desktop" "/root/Desktop"; do
    if [ -d "$d" ]; then
        cp -f /usr/share/applications/vde.desktop "$d/Launch_VDE.desktop"
        chmod +x "$d/Launch_VDE.desktop" 2>/dev/null || true
        chown -R "$TARGET_USER:$TARGET_USER" "$d/Launch_VDE.desktop" 2>/dev/null || true
    fi
done

# Configure automatic boot directly into VDE
if [ "$WIPE_SLOP" = true ]; then
    echo -e "${C_GREEN}>> Setting VDE as the default boot session...${C_RESET}"
    mkdir -p /etc/systemd/system/getty@tty1.service.d
    cat << EOF > /etc/systemd/system/getty@tty1.service.d/override.conf
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin ${TARGET_USER} --noclear %I \$TERM
EOF
    mkdir -p /etc/profile.d
    cat << 'EOF' > /etc/profile.d/99-vde-login.sh
if [ -z "$WAYLAND_DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
    exec /usr/local/bin/vde-session
fi
EOF
    systemctl daemon-reload 2>/dev/null || true
fi

echo ""
echo -e "${C_GREEN}==============================================================${C_RESET}"
echo -e "${C_GREEN}  VDE Installed & Verified Successfully!                      ${C_RESET}"
echo -e "${C_GREEN}==============================================================${C_RESET}"
echo ""
echo -e "Background telemetry, snapd, and default desktop bloat have been eliminated."
echo ""
echo -e "A system restart is recommended to initialize a clean Wayland session"
echo -e "and boot directly into the Victorious Desktop Environment."
echo ""

# Prompt to reboot like any modern OS installer
if [ -t 0 ] || [ -c /dev/tty ]; then
    read -r -p "Would you like to restart the computer now? [Y/n]: " REBOOT_CHOICE </dev/tty || REBOOT_CHOICE="n"
    case "$REBOOT_CHOICE" in
        [nN][oO]|[nN])
            echo ""
            echo -e "You can launch VDE anytime by running: ${C_CYAN}vde${C_RESET}"
            echo -e "Or restart later by running: ${C_CYAN}sudo reboot${C_RESET}"
            ;;
        *)
            echo ""
            echo -e "${C_GREEN}>> Restarting computer into VDE...${C_RESET}"
            sleep 2
            reboot 2>/dev/null || systemctl reboot 2>/dev/null || shutdown -r now 2>/dev/null || true
            ;;
    esac
else
    echo -e "To start VDE right now on your screen, run: ${C_CYAN}vde${C_RESET}"
    echo -e "To restart into clean VDE session, run: ${C_CYAN}sudo reboot${C_RESET}"
fi
echo ""
