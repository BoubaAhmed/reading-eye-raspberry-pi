#!/bin/bash

# Reading Eye - Main Run Script
# Wrapper for executing the application with proper environment setup
# Usage: bash run.sh [options]

set -e

# Detect script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
VENV_NAME="${VENV_NAME:-env_projet_7}"
VENV_DIR="${SCRIPT_DIR}/${VENV_NAME}"
APP_DIR="${SCRIPT_DIR}/scripts"

# Check if virtual environment exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Error: Virtual environment not found at $VENV_DIR"
    echo "Please run setup.sh first"
    exit 1
fi

# Activate virtual environment
source "$VENV_DIR/bin/activate"

# Change to app directory
cd "$APP_DIR"

# Run application
python3 app_main.py "$@"
