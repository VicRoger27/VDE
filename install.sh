#!/usr/bin/env bash
# ==============================================================================
# Victorious Desktop Environment (VDE) - Universal Terminal Installer
# https://github.com/VicRoger27/VDE
#
# Optimized for:
#   - "Try Ubuntu" live USB / live sessions (instant live switch in RAM)
#   - Ubuntu Server & Ubuntu Desktop (GNOME replacement or coexistence)
#   - Debian, Linux Mint, Arch, Fedora
# ==============================================================================

set -eo pipefail

VDE_VERSION="1.0.0"
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
    echo -e "  ${C_YELLOW}curl -sSL https://raw.githubusercontent.com/VicRoger27/VDE/main/install.sh | sudo bash${C_RESET}"
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

# 2. Parse Arguments or Interactive Mode
WIPE_OLD=false
START_NOW=false

for arg in "$@"; do
    case "$arg" in
        --replace|--wipe|-r)
            WIPE_OLD=true
            ;;
        --start|-s)
            START_NOW=true
            ;;
    esac
done

# If live session and not explicitly passed, default to instant tryout
if [ "$IS_LIVE_SESSION" = true ]; then
    WIPE_OLD=false
fi

# 3. Enable Universe repository on Ubuntu/Debian if missing
if command -v add-apt-repository >/dev/null 2>&1; then
    echo -e "${C_CYAN}>> Ensuring universe repository is enabled...${C_RESET}"
    add-apt-repository -y universe 2>/dev/null || true
fi

# 4. Fetch or Locate Sources
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || echo "")"
SRC_DIR=""

if [ -f "$SCRIPT_DIR/tokens/theme.json" ] && [ -d "$SCRIPT_DIR/compositor" ]; then
    SRC_DIR="$SCRIPT_DIR"
    echo -e "${C_GREEN}>> Using local VDE source tree:${C_RESET} ${SRC_DIR}"
else
    TMP_SRC="/tmp/vde-install-src"
    echo -e "${C_YELLOW}>> Fetching latest VDE sources from GitHub into ${TMP_SRC}...${C_RESET}"
    rm -rf "$TMP_SRC"
    if command -v git >/dev/null 2>&1; then
        git clone --depth 1 "$REPO_URL" "$TMP_SRC"
    else
        apt-get update -y && apt-get install -y --no-install-recommends git ca-certificates
        git clone --depth 1 "$REPO_URL" "$TMP_SRC"
    fi
    SRC_DIR="$TMP_SRC"
fi

# 5. Wipe Old Desktop if requested
if [ "$WIPE_OLD" = true ]; then
    echo ""
    echo -e "${C_RED}>> [WIPE] Purging old desktop environment (GNOME) & telemetry...${C_RESET}"
    if command -v apt-get >/dev/null 2>&1; then
        export DEBIAN_FRONTEND=noninteractive
        systemctl stop gdm3 2>/dev/null || systemctl stop lightdm 2>/dev/null || true
        apt-get purge -y gnome-shell gnome-session gdm3 ubuntu-desktop ubuntu-desktop-minimal whoopsie popularity-contest ubuntu-report apport 2>/dev/null || true
        apt-get autoremove -y --purge 2>/dev/null || true
        apt-get clean
    fi
    echo -e "${C_GREEN}>> Old desktop purged.${C_RESET}"
fi

# 6. Install Core Dependencies
echo -e "${C_CYAN}>> [1/5] Installing VDE compositor & Wayland dependencies...${C_RESET}"
if command -v apt-get >/dev/null 2>&1; then
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -y
    apt-get install -y --no-install-recommends \
        labwc \
        wayland-protocols \
        mesa-vulkan-drivers \
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
        fonts-dejavu-core 2>/dev/null || \
    apt-get install -y --no-install-recommends \
        labwc \
        wayland-protocols \
        mesa-vulkan-drivers \
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

# 8. Deploy Labwc Configurations
echo -e "${C_CYAN}>> [3/5] Configuring Labwc compositor...${C_RESET}"
mkdir -p /etc/xdg/labwc
cp -f "$SRC_DIR/compositor/rc.xml" /etc/xdg/labwc/rc.xml
cp -f "$SRC_DIR/compositor/themerc" /etc/xdg/labwc/themerc
cp -f "$SRC_DIR/compositor/environment" /etc/xdg/labwc/environment
cp -f "$SRC_DIR/compositor/autostart" /etc/xdg/labwc/autostart

# Deploy to current user's ~/.config/labwc
if [ -n "$USER_HOME" ]; then
    USER_LABWC="$USER_HOME/.config/labwc"
    mkdir -p "$USER_LABWC"
    cp -f /etc/xdg/labwc/* "$USER_LABWC/" 2>/dev/null || true
    chown -R "$TARGET_USER:$TARGET_USER" "$USER_HOME/.config" 2>/dev/null || true
fi

# 9. Install Executable Binaries in /usr/local/bin
echo -e "${C_CYAN}>> [4/5] Installing executable commands in ${BIN_PREFIX}...${C_RESET}"

cat << 'EOF' > "${BIN_PREFIX}/vde-session"
#!/usr/bin/env bash
export XDG_CURRENT_DESKTOP=VDE
export XDG_SESSION_DESKTOP=VDE
export XDG_SESSION_TYPE=wayland

# Ensure D-Bus user session
if [ -z "$DBUS_SESSION_BUS_ADDRESS" ]; then
    eval $(dbus-launch --sh-syntax --exit-with-session 2>/dev/null || true)
fi

echo "=========================================================="
echo " Starting Victorious Desktop Environment (VDE)..."
echo " Compositor: Labwc (wlroots layer-shell)"
echo " Shell: Astal Taskbar & Qt6 Start Menu"
echo "=========================================================="

exec labwc -s /usr/local/bin/vde-bar
EOF
chmod +x "${BIN_PREFIX}/vde-session"

cat << 'EOF' > "${BIN_PREFIX}/vde"
#!/usr/bin/env bash
# Direct VDE launcher (runs nested if already in a desktop, or native if on TTY)
if [ -n "$WAYLAND_DISPLAY" ] || [ -n "$DISPLAY" ]; then
    echo ">> Running VDE nested inside current display..."
    exec labwc -s /usr/local/bin/vde-bar
else
    exec /usr/local/bin/vde-session "$@"
fi
EOF
chmod +x "${BIN_PREFIX}/vde"

cat << 'EOF' > "${BIN_PREFIX}/vde-bar"
#!/usr/bin/env bash
exec /usr/share/vde/astal-shell/vde-bar "$@"
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

# 10. Register Sessions & Desktop Shortcuts
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

# Create desktop shortcut on the live user's desktop
for d in "$USER_HOME/Desktop" "/home/ubuntu/Desktop" "/root/Desktop"; do
    if [ -d "$d" ]; then
        cp -f /usr/share/applications/vde.desktop "$d/Launch_VDE.desktop"
        chmod +x "$d/Launch_VDE.desktop" 2>/dev/null || true
        chown -R "$TARGET_USER:$TARGET_USER" "$d/Launch_VDE.desktop" 2>/dev/null || true
    fi
done

echo ""
echo -e "${C_GREEN}==============================================================${C_RESET}"
echo -e "${C_GREEN}  VDE is Ready in your Live Ubuntu Session!                   ${C_RESET}"
echo -e "${C_GREEN}==============================================================${C_RESET}"
echo ""
echo -e "You can launch VDE right now from this terminal:"
echo -e "  ${C_CYAN}vde${C_RESET}"
echo ""
echo -e "Or double-click the ${C_WHITE}'Launch VDE'${C_RESET} icon placed directly on your Desktop!"
echo ""
