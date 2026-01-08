#!/bin/bash

# Reading Eye - Initial Setup Script for Raspberry Pi
# This script sets up the project environment on a Raspberry Pi
# Usage: bash setup.sh

set -e

echo "=========================================="
echo "Reading Eye - Raspberry Pi Setup"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Detect project directory
PROJECT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_NAME="${VENV_NAME:-env_projet_7}"
VENV_DIR="${PROJECT_DIR}/../${VENV_NAME}"

echo -e "${YELLOW}Project directory:${NC} $PROJECT_DIR"
echo -e "${YELLOW}Virtual environment:${NC} $VENV_DIR"
echo ""

# Step 1: Check for system dependencies
echo -e "${YELLOW}[1/5] Checking system dependencies...${NC}"

required_packages=(
    "python3"
    "tesseract-ocr"
    "python3-venv"
)

missing_packages=()

for package in "${required_packages[@]}"; do
    if ! command -v "$package" &> /dev/null && ! dpkg -l | grep -q "^ii.*$package"; then
        missing_packages+=("$package")
    fi
done

if [ ${#missing_packages[@]} -gt 0 ]; then
    echo -e "${RED}Missing system packages:${NC} ${missing_packages[*]}"
    echo "Please run:"
    echo "  sudo apt update && sudo apt upgrade -y"
    echo "  sudo apt install -y tesseract-ocr python3-picamera2 python3-venv python3-pip build-essential"
    echo "  sudo apt install -y tesseract-ocr-eng tesseract-ocr-fra tesseract-ocr-ara"
    echo ""
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    echo -e "${GREEN}✓ All system dependencies found${NC}"
fi

# Step 2: Create virtual environment if it doesn't exist
echo ""
echo -e "${YELLOW}[2/5] Setting up virtual environment...${NC}"

if [ -d "$VENV_DIR" ]; then
    echo -e "${GREEN}✓ Virtual environment exists:${NC} $VENV_DIR"
else
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
    echo -e "${GREEN}✓ Virtual environment created${NC}"
fi

# Step 3: Activate virtual environment and install dependencies
echo ""
echo -e "${YELLOW}[3/5] Installing Python dependencies...${NC}"

source "$VENV_DIR/bin/activate"

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install requirements
if [ -f "$PROJECT_DIR/requirements.txt" ]; then
    pip install -r "$PROJECT_DIR/requirements.txt"
    echo -e "${GREEN}✓ Dependencies installed${NC}"
else
    echo -e "${RED}✗ requirements.txt not found${NC}"
    exit 1
fi

# Step 4: Check installation
echo ""
echo -e "${YELLOW}[4/5] Verifying installation...${NC}"

python3 -c "import cv2; print('✓ OpenCV installed')" || echo "✗ OpenCV installation failed"
python3 -c "import pytesseract; print('✓ pytesseract installed')" || echo "✗ pytesseract installation failed"
python3 -c "import pyttsx3; print('✓ pyttsx3 installed')" || echo "✗ pyttsx3 installation failed"

# Check tesseract
if command -v tesseract &> /dev/null; then
    echo "✓ Tesseract OCR available"
    tesseract --version | head -1
else
    echo "✗ Tesseract not found"
fi

# Step 5: Create directories
echo ""
echo -e "${YELLOW}[5/5] Creating project directories...${NC}"

mkdir -p "$PROJECT_DIR/logs"
mkdir -p "$PROJECT_DIR/capture"
mkdir -p "$PROJECT_DIR/config"

echo -e "${GREEN}✓ Directories created${NC}"

# Final instructions
echo ""
echo -e "${GREEN}=========================================="
echo "Setup Complete!"
echo "==========================================${NC}"
echo ""
echo "Next steps:"
echo ""
echo "1. Activate the virtual environment:"
echo "   source $VENV_DIR/bin/activate"
echo ""
echo "2. Configure the application:"
echo "   Edit $PROJECT_DIR/config/reading_eye_config.json"
echo ""
echo "3. Run single capture test:"
echo "   python3 $PROJECT_DIR/scripts/app_main.py --single --lang fra+eng"
echo ""
echo "4. Run continuous capture loop:"
echo "   python3 $PROJECT_DIR/scripts/app_main.py --loop --interval 5.0 --lang fra+eng"
echo ""
echo "For more information, see README.md"
echo ""
