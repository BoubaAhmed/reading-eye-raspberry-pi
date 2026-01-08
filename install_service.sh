#!/bin/bash

# Reading Eye - Systemd Service Installer
# Creates a systemd service for automatic startup
# Usage: sudo bash install_service.sh

if [ "$EUID" -ne 0 ]; then 
    echo "This script must be run with sudo"
    exit 1
fi

PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_NAME="${VENV_NAME:-env_projet_7}"
VENV_DIR="${PROJECT_DIR}/../${VENV_NAME}"
PI_USER="${SUDO_USER:-pi}"

echo "Creating systemd service..."

# Create service file
cat > /etc/systemd/system/reading-eye.service << EOF
[Unit]
Description=Reading Eye - OCR and TTS for Raspberry Pi
After=network.target

[Service]
Type=simple
User=$PI_USER
WorkingDirectory=$PROJECT_DIR/scripts
ExecStart=$VENV_DIR/bin/python3 $PROJECT_DIR/scripts/app_main.py --loop --interval 5.0
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Set permissions
chmod 644 /etc/systemd/system/reading-eye.service

# Reload systemd
systemctl daemon-reload

echo "Service installed successfully!"
echo ""
echo "Available commands:"
echo "  sudo systemctl start reading-eye      - Start service"
echo "  sudo systemctl stop reading-eye       - Stop service"
echo "  sudo systemctl restart reading-eye    - Restart service"
echo "  sudo systemctl enable reading-eye     - Enable on boot"
echo "  sudo systemctl disable reading-eye    - Disable on boot"
echo "  sudo systemctl status reading-eye     - Check status"
echo "  sudo journalctl -u reading-eye -f     - View logs"
echo ""
