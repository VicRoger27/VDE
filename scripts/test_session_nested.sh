#!/usr/bin/env bash
# VDE Nested Session Test Runner
# Spawns Labwc in a nested window with VDE compositor rules and shell daemons

set -eo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo "=========================================================="
echo " Starting VDE Nested Session Test"
echo " Target: <500 MB RAM | Zero Telemetry | Windows 11 Shell"
echo "=========================================================="

# 1. Create temporary isolated config directory for nested session
NESTED_DIR="$(mktemp -d /tmp/vde-session-XXXXXX)"
LABWC_CONFIG="$NESTED_DIR/labwc"
mkdir -p "$LABWC_CONFIG"

# 2. Copy compositor files
cp "$ROOT_DIR/compositor/rc.xml" "$LABWC_CONFIG/rc.xml"
cp "$ROOT_DIR/compositor/themerc" "$LABWC_CONFIG/themerc"
cp "$ROOT_DIR/compositor/environment" "$LABWC_CONFIG/environment"

# 3. Create nested-specific autostart
cat << 'EOF' > "$LABWC_CONFIG/autostart"
#!/bin/sh
# Nested session autostart
export XDG_CURRENT_DESKTOP=VDE:wlroots
export QT_QPA_PLATFORM=wayland
export GDK_BACKEND=wayland

SCRIPT_DIR="$(dirname "$0")"
ROOT_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"

# Launch Astal Taskbar & Quick Settings
if [ -x "$ROOT_DIR/astal-shell/vde-bar" ]; then
    "$ROOT_DIR/astal-shell/vde-bar" &
fi

# Launch Qt6 Start Menu Runner in background
if [ -x "$ROOT_DIR/qt-launcher/vde-launcher" ]; then
    "$ROOT_DIR/qt-launcher/vde-launcher" --daemon &
fi
EOF
chmod +x "$LABWC_CONFIG/autostart"

# 4. Clean up on exit
cleanup() {
    echo ""
    echo ">> Shutting down VDE nested session..."
    kill $(jobs -p) 2>/dev/null || true
    pkill -P $$ 2>/dev/null || true
    rm -rf "$NESTED_DIR"
    echo ">> Cleanup complete."
}
trap cleanup EXIT INT TERM

# 5. Check dependencies
if ! command -v labwc >/dev/null 2>&1; then
    echo "[Error] 'labwc' command not found." >&2
    echo "Please install labwc (e.g., sudo apt install labwc || sudo pacman -S labwc)." >&2
    exit 1
fi

echo ">> Configuration isolated at: $LABWC_CONFIG"
echo ">> Spawning nested Labwc window (press Alt+F4 or close window to exit)..."

# 6. Launch nested labwc
exec labwc -C "$LABWC_CONFIG"
