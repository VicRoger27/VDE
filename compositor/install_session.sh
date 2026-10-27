#!/bin/sh
# VDE Labwc Session Installer
# Copies Labwc configurations and systemd units to user directories

set -e

CONFIG_DIR="${XDG_CONFIG_HOME:-$HOME/.config}"
LABWC_DIR="$CONFIG_DIR/labwc"
SYSTEMD_DIR="$CONFIG_DIR/systemd/user"
COMPOSITOR_SRC="$(dirname "$0")"

echo "Installing VDE Compositor Configuration..."

mkdir -p "$LABWC_DIR"
cp "$COMPOSITOR_SRC/rc.xml" "$LABWC_DIR/rc.xml"
cp "$COMPOSITOR_SRC/themerc" "$LABWC_DIR/themerc"
cp "$COMPOSITOR_SRC/environment" "$LABWC_DIR/environment"
cp "$COMPOSITOR_SRC/autostart" "$LABWC_DIR/autostart"
chmod +x "$LABWC_DIR/autostart"

echo "Installed labwc files to $LABWC_DIR"

mkdir -p "$SYSTEMD_DIR"
cp "$COMPOSITOR_SRC/systemd/"*.service "$SYSTEMD_DIR/" 2>/dev/null || true
cp "$COMPOSITOR_SRC/systemd/"*.target "$SYSTEMD_DIR/" 2>/dev/null || true

echo "Installed systemd user units to $SYSTEMD_DIR"
echo "VDE Compositor setup complete!"
