#!/bin/sh
set -eu

SCRIPT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
APP_DIR="$HOME/.local/share/xfce-connection-centre"
DESKTOP_DIR="$HOME/.local/share/applications"

echo "Installing XFCE Connection Centre..."

if [ ! -f "$SCRIPT_DIR/connection_centre.py" ]; then
    echo "Error: connection_centre.py not found."
    exit 1
fi

if ! command -v python3 >/dev/null 2>&1; then
    echo "Error: Python 3 is required."
    exit 1
fi

if ! python3 -c 'import tkinter' >/dev/null 2>&1; then
    echo "Error: Python Tkinter is missing."
    echo "Install python3-tk in Debian/Ubuntu."
    exit 1
fi

mkdir -p "$APP_DIR" "$DESKTOP_DIR"

cp "$SCRIPT_DIR/connection_centre.py" "$APP_DIR/"
cp "$SCRIPT_DIR/launch.sh" "$APP_DIR/"
cp "$SCRIPT_DIR/icon.svg" "$APP_DIR/"

chmod 755 "$APP_DIR/launch.sh"

# Create XFCE desktop launcher
cat > "$DESKTOP_DIR/xfce-connection-centre.desktop" <<DESKTOP
[Desktop Entry]
Version=1.0
Type=Application
Name=XFCE Connection Centre
GenericName=Connectivity Dashboard
Comment=Android and Linux connectivity dashboard
Exec="$APP_DIR/launch.sh"
Icon=$APP_DIR/icon.svg
Terminal=false
StartupNotify=true
Categories=Settings;System;
Keywords=WiFi;Bluetooth;Ethernet;Network;Android;
DESKTOP

chmod 644 "$DESKTOP_DIR/xfce-connection-centre.desktop"

if command -v update-desktop-database >/dev/null 2>&1; then
    update-desktop-database "$DESKTOP_DIR" || true
fi

echo ""
echo "Installation completed."
echo "Application: $APP_DIR"
echo "Launcher: $DESKTOP_DIR/xfce-connection-centre.desktop"
echo "Find XFCE Connection Centre in Applications Menu."
