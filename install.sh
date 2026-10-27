#!/usr/bin/env bash
# ==============================================================================
# Victorious Desktop Environment (VDE) - Universal Terminal Installer
# https://github.com/VicRoger27/VDE
#
# Supports: Ubuntu Server, Ubuntu Desktop (GNOME), Debian, Mint, Arch, Fedora
# Wipes old heavy desktop environments (GNOME/Ubuntu Desktop) and replaces with VDE.
# Target idle RAM: < 500 MB (Sub-250 MB on minimal Ubuntu Server base)
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
    echo -e "Please re-run with: ${C_YELLOW}sudo ./install.sh${C_RESET}"
    echo -e "Or: ${C_YELLOW}curl -sSL https://raw.githubusercontent.com/VicRoger27/VDE/main/install.sh | sudo bash${C_RESET}"
    exit 1
fi

TARGET_USER="${SUDO_USER:-$USER}"
USER_HOME=$(getent passwd "$TARGET_USER" | cut -d: -f6)

echo -e "${C_GREEN}>> Target User:${C_RESET} ${TARGET_USER} (${USER_HOME})"

# Parse Flags or Interactive Prompt
WIPE_OLD=false
AUTO_YES=false

for arg in "$@"; do
    case "$arg" in
        --replace|--wipe|-r)
            WIPE_OLD=true
            ;;
        -y|--yes)
            AUTO_YES=true
            ;;
    esac
done

# If not passed via CLI flag and running in an interactive terminal, ask the user
if [ "$WIPE_OLD" = false ] && [ -t 0 ]; then
    echo ""
    echo -e "${C_YELLOW}Select Installation Mode:${C_RESET}"
    echo -e "  ${C_WHITE}[1] Clean Replace${C_RESET} - Wipe old heavy DE (GNOME/bloat/telemetry) and replace with VDE"
    echo -e "  ${C_WHITE}[2] Coexist${C_RESET}       - Keep existing desktop and install VDE alongside"
    echo ""
    read -rp "Enter choice [1 or 2, default is 1]: " MODE_CHOICE
    if [ "$MODE_CHOICE" = "2" ]; then
        WIPE_OLD=false
    else
        WIPE_OLD=true
    fi
fi

# 2. Locate or Clone Repository Sources
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" 2>/dev/null && pwd || echo "")"
SRC_DIR=""

if [ -f "$SCRIPT_DIR/tokens/theme.json" ] && [ -d "$SCRIPT_DIR/compositor" ]; then
    SRC_DIR="$SCRIPT_DIR"
    echo -e "${C_GREEN}>> Using local VDE source tree:${C_RESET} ${SRC_DIR}"
else
    TMP_SRC="/tmp/vde-install-src"
    echo -e "${C_YELLOW}>> Fetching latest VDE sources from GitHub into ${TMP_SRC}...${C_RESET}"
    rm -rf "$TMP_SRC"
    git clone --depth 1 "$REPO_URL" "$TMP_SRC"
    SRC_DIR="$TMP_SRC"
fi

# 3. Wipe Old Desktop (GNOME / Telemetry / Bloat) if requested
if [ "$WIPE_OLD" = true ]; then
    echo ""
    echo -e "${C_RED}==============================================================${C_RESET}"
    echo -e "${C_RED}>> [WIPE] Removing old desktop environment & telemetry bloat...${C_RESET}"
    echo -e "${C_RED}==============================================================${C_RESET}"

    if command -v apt-get >/dev/null 2>&1; then
        export DEBIAN_FRONTEND=noninteractive
        
        # Stop display manager
        systemctl stop gdm3 2>/dev/null || systemctl stop lightdm 2>/dev/null || true

        # Remove GNOME, telemetry, and heavy bloat
        echo -e "${C_YELLOW}>> Purging GNOME shell, GDM, and Canonical telemetry...${C_RESET}"
        apt-get purge -y \
            gnome-shell \
            gnome-session \
            gdm3 \
            ubuntu-desktop \
            ubuntu-desktop-minimal \
            whoopsie \
            popularity-contest \
            ubuntu-report \
            apport 2>/dev/null || true

        echo -e "${C_YELLOW}>> Cleaning orphaned packages and residual configurations...${C_RESET}"
        apt-get autoremove -y --purge 2>/dev/null || true
        apt-get clean
    elif command -v dnf >/dev/null 2>&1; then
        dnf remove -y @gnome-desktop gdm 2>/dev/null || true
    elif command -v pacman >/dev/null 2>&1; then
        pacman -Rns --noconfirm gnome gnome-extra gdm 2>/dev/null || true
    fi
    echo -e "${C_GREEN}>> Old desktop purged successfully.${C_RESET}"
fi

# 4. Detect Package Manager and Install VDE Dependencies
echo ""
echo -e "${C_CYAN}>> [1/5] Installing core VDE dependencies and Wayland stack...${C_RESET}"

if command -v apt-get >/dev/null 2>&1; then
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -y
    apt-get install -y --no-install-recommends \
        labwc \
        wayland-protocols \
        mesa-vulkan-drivers \
        mesa-utils \
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
        greetd \
        fonts-dejavu-core \
        fonts-noto-color-emoji 2>/dev/null || \
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
    pacman -Syu --noconfirm --needed \
        labwc \
        vulkan-intel \
        vulkan-radeon \
        pipewire \
        wireplumber \
        foot \
        glib2 \
        brightnessctl \
        grim \
        slurp \
        wl-clipboard \
        polkit \
        xdg-utils \
        noto-fonts
elif command -v dnf >/dev/null 2>&1; then
    dnf install -y \
        labwc \
        pipewire \
        wireplumber \
        foot \
        glib2 \
        brightnessctl \
        grim \
        slurp \
        wl-clipboard \
        polkit \
        xdg-utils
fi

# 5. Install VDE Desktop Files
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

# 6. Deploy System-Wide Compositor Configurations
echo -e "${C_CYAN}>> [3/5] Configuring Labwc compositor and theming rules...${C_RESET}"
mkdir -p /etc/xdg/labwc
cp -f "$SRC_DIR/compositor/rc.xml" /etc/xdg/labwc/rc.xml
cp -f "$SRC_DIR/compositor/themerc" /etc/xdg/labwc/themerc
cp -f "$SRC_DIR/compositor/environment" /etc/xdg/labwc/environment
cp -f "$SRC_DIR/compositor/autostart" /etc/xdg/labwc/autostart

# Deploy to target user's local config
if [ -n "$USER_HOME" ] && [ -d "$USER_HOME" ]; then
    USER_LABWC="$USER_HOME/.config/labwc"
    mkdir -p "$USER_LABWC"
    cp -f /etc/xdg/labwc/* "$USER_LABWC/"
    chown -R "$TARGET_USER:$TARGET_USER" "$USER_HOME/.config"
fi

# 7. Install Executable Commands in /usr/local/bin
echo -e "${C_CYAN}>> [4/5] Installing executable commands in ${BIN_PREFIX}...${C_RESET}"

# vde-session (master Wayland session launcher)
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

# Launch compositor with integrated VDE bar autostart
exec labwc -s /usr/local/bin/vde-bar
EOF
chmod +x "${BIN_PREFIX}/vde-session"

# 'vde' shorthand command (run from any terminal / TTY to enter VDE)
cat << 'EOF' > "${BIN_PREFIX}/vde"
#!/usr/bin/env bash
exec /usr/local/bin/vde-session "$@"
EOF
chmod +x "${BIN_PREFIX}/vde"

# Wrappers for subcomponents
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

# 8. Register Wayland Display Manager Session & Default Targets
echo -e "${C_CYAN}>> [5/5] Registering Wayland desktop session and boot defaults...${C_RESET}"
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

# Register Crossings Settings application
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

# Configure greetd or autologin if clean replace was selected
if [ "$WIPE_OLD" = true ]; then
    echo -e "${C_GREEN}>> Configuring automated boot directly into VDE...${C_RESET}"
    
    # Configure tty1 direct autologin into VDE
    mkdir -p /etc/systemd/system/getty@tty1.service.d
    cat << EOF > /etc/systemd/system/getty@tty1.service.d/override.conf
[Service]
ExecStart=
ExecStart=-/sbin/agetty --autologin ${TARGET_USER} --noclear %I \$TERM
EOF

    # Configure profile to start VDE on tty1
    mkdir -p /etc/profile.d
    cat << 'EOF' > /etc/profile.d/99-vde-login.sh
# Auto-start VDE on tty1 console login
if [ -z "$WAYLAND_DISPLAY" ] && [ "$(tty)" = "/dev/tty1" ]; then
    exec /usr/local/bin/vde-session
fi
EOF

    systemctl daemon-reload 2>/dev/null || true
fi

echo ""
echo -e "${C_GREEN}==============================================================${C_RESET}"
echo -e "${C_GREEN}  VDE Installation & System Replacement Complete!            ${C_RESET}"
echo -e "${C_GREEN}==============================================================${C_RESET}"
echo ""
echo -e "You can launch VDE immediately:"
echo -e "  ${C_CYAN}vde${C_RESET}"
echo ""
if [ "$WIPE_OLD" = true ]; then
    echo -e "The old desktop has been replaced. A reboot will take you directly into VDE:"
    echo -e "  ${C_YELLOW}sudo reboot${C_RESET}"
fi
echo ""
