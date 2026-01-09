#!/bin/bash

# Reading Eye - System Setup Script for Raspberry Pi
# Installs all system-level dependencies
# Must be run with sudo privileges
# Usage: sudo bash system_setup.sh

if [ "$EUID" -ne 0 ]; then
    echo "This script must be run with sudo"
    exit 1
fi

echo "=========================================="
echo "Reading Eye - System Setup"
echo "=========================================="
echo ""

# Update system
echo "Updating system packages..."
apt update && apt upgrade -y

# Install camera support
echo "Installing camera support..."
apt install -y libcamera-apps python3-picamera2 v4l-utils

# Install Tesseract OCR and language packs
echo "Installing Tesseract OCR..."
apt install -y tesseract-ocr libtesseract-dev libleptonica-dev

# Install language packs
echo "Installing language packs..."
apt install -y \
    tesseract-ocr-eng \
    tesseract-ocr-fra \
    tesseract-ocr-ara \
    tesseract-ocr-deu \
    tesseract-ocr-spa \
    tesseract-ocr-ita

# Install Python development tools
echo "Installing Python development tools..."
apt install -y \
    python3-venv \
    python3-pip \
    python3-dev \
    build-essential \
    libjpeg-dev \
    libatlas-base-dev \
    libopenjp2-7

# Install audio support (for gTTS playback)
echo "Installing audio support..."
apt install -y mpg123 alsa-utils sox

# Install ffmpeg for additional audio support
echo "Installing ffmpeg..."
apt install -y ffmpeg

# Add current user to video group (for camera access)
CURRENT_USER="${SUDO_USER:-$USER}"
echo "Adding $CURRENT_USER to video group..."
usermod -aG video "$CURRENT_USER"

echo ""
echo "=========================================="
echo "System Setup Complete!"
echo "=========================================="
echo ""
echo "IMPORTANT: You may need to log out and back in"
echo "for group changes to take effect."
echo ""
echo "Next step: Run setup.sh to configure the Python environment"
echo ""
