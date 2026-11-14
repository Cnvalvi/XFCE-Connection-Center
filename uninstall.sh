#!/bin/sh
set -eu

APP_DIR="$HOME/.local/share/xfce-connection-centre"
DESKTOP_FILE="$HOME/.local/share/applications/xfce-connection-centre.desktop"

echo "Removing XFCE Connection Centre..."

rm -f "$DESKTOP_FILE"
rm -rf "$APP_DIR"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$HOME/.local/share/applications" || true
fi

echo "Uninstallation completed."
echo "Project source files have not been deleted."
