#!/bin/sh
APP_DIR="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"

if command -v python3 >/dev/null 2>&1; then
    PYTHON="$(command -v python3)"
elif command -v python >/dev/null 2>&1; then
    PYTHON="$(command -v python)"
else
    echo "Error: Python is not installed."
    exit 1
fi

exec "$PYTHON" "$APP_DIR/connection_centre.py" "$@"
