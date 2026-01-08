# Reading Eye - Detailed SSH Setup Instructions

## Overview

This guide provides step-by-step instructions for deploying Reading Eye on a shared Raspberry Pi 5 with multiple student groups, each using isolated Python virtual environments via SSH.

### Key Concepts

- **Shared Raspberry Pi**: One Pi serves multiple groups
- **Isolated Environments**: Each group has `env_projet_7` with separate dependencies
- **SSH Access**: All work done remotely via SSH (no monitor/keyboard on Pi)
- **Persistent Environment**: Virtual environment persists between sessions

---

## System Architecture

```
┌─────────────────────────┐
│   Raspberry Pi 5        │
├─────────────────────────┤
│ /home/pi/               │
│ ├── reading_eye/        │ (your project)
│ │   ├── scripts/        │ (Python code)
│ │   ├── config/         │ (JSON config)
│ │   └── logs/           │ (Application logs)
│ └── env_projet_7/       │ (Virtual environment)
└─────────────────────────┘
         ↑
         │ SSH
         │
    Your Computer
```

---

## Prerequisites

Before you start, verify:

- **Raspberry Pi 5** with Raspberry Pi OS (Bookworm or Bullseye recommended)
- **Pi Camera 3 Module** connected and enabled
- **Network connectivity** - Pi and your computer on same network
- **SSH enabled** on the Pi
- **Python 3.13.5+** (pre-installed on Raspberry Pi OS)
- **Virtual environment** `env_projet_7` already created by an admin

### Find Your Pi's IP Address

If you have physical access:

```bash
# On the Pi
hostname -I
```

From your development machine:

```bash
# Linux/Mac
ping raspberrypi.local

# Or scan network
nmap -sn 192.168.x.0/24

# Or check router's DHCP list
```

---

## Step 1: Initial SSH Connection

### From Linux/Mac:

```bash
ssh pi@raspberrypi.local
# or
ssh pi@192.168.1.XXX
```

### From Windows:

**Option A: PowerShell (Windows 10+)**

```powershell
ssh pi@raspberrypi.local
```

**Option B: PuTTY**

1. Download [PuTTY](https://www.putty.org/)
2. Host Name: `raspberrypi.local` (or IP address)
3. Port: 22
4. Connection Type: SSH
5. Click Open

**Option C: Visual Studio Code Remote SSH**

1. Install "Remote - SSH" extension
2. Click Remote Explorer icon
3. Add New SSH Host: `ssh pi@raspberrypi.local`
4. Click "Connect to Host"

### First Connection

When first connecting, you may see a security warning:

```
The authenticity of host 'raspberrypi.local' can't be established.
ECDSA key fingerprint is SHA256:xxx
Are you sure you want to continue connecting? (yes/no)
```

Type: `yes` and press Enter.

Default Credentials (if unchanged):

- **Username**: `pi`
- **Password**: `raspberry`

---

## Step 2: Verify System Setup

A system administrator should have already run:

```bash
sudo bash system_setup.sh
```

Verify system dependencies are installed:

```bash
# Check Tesseract
tesseract --version

# Check Python
python3 --version

# Check Camera
libcamera-hello --version

# Check language packs
tesseract --list-langs
```

Expected output for languages:

```
tesseract 5.x.x
...
eng
fra
ara
```

If any are missing, contact your administrator.

---

## Step 3: Verify Virtual Environment

The virtual environment should already exist at `~/env_projet_7`.

```bash
# Check it exists
ls -la ~/env_projet_7/bin/activate

# Activate it
source ~/env_projet_7/bin/activate

# Verify (should show (env_projet_7) in prompt)
python3 --version
pip list | head -10
```

---

## Step 4: Get the Project Code

### Option A: Clone from GitHub

If your project is on GitHub:

```bash
cd ~
git clone https://github.com/YOUR_ORG/reading-eye.git
cd reading-eye
```

Update later:

```bash
git pull origin main
```

### Option B: Copy from Your Computer

From your **development machine** (not on the Pi):

```bash
# Copy the entire raspberry_code folder
scp -r ./raspberry_code pi@raspberrypi.local:~/reading_eye

# Verify
ssh pi@raspberrypi.local "ls -la ~/reading_eye"
```

---

## Step 5: Setup Python Environment

```bash
# Navigate to project
cd ~/reading_eye

# Run setup
bash setup.sh
```

This script will:

1. ✓ Check system dependencies
2. ✓ Verify/create virtual environment at `~/env_projet_7`
3. ✓ Install Python packages from `requirements.txt`
4. ✓ Verify installations
5. ✓ Create necessary directories

**Expected Output:**

```
==========================================
Reading Eye - Raspberry Pi Setup
==========================================
[1/5] Checking system dependencies...
✓ All system dependencies found
[2/5] Setting up virtual environment...
✓ Virtual environment exists: ...
[3/5] Installing Python dependencies...
...
✓ Dependencies installed
[4/5] Verifying installation...
✓ OpenCV installed
✓ pytesseract installed
✓ pyttsx3 installed
✓ Tesseract OCR available
[5/5] Creating project directories...
✓ Directories created

Setup Complete!
```

---

## Step 6: First Test Run

### Activate Environment

```bash
source ~/env_projet_7/bin/activate
cd ~/reading_eye
```

You should see `(env_projet_7)` at the start of your prompt.

### Test Single Capture

```bash
bash run.sh --single --lang fra+eng
```

Expected output:

```
--- Detected text ---
[Text from camera or blank if no text in frame]
---------------------
Speaking text...
```

---

## Step 7: Configure for Your Group

Edit configuration file:

```bash
nano config/reading_eye_config.json
```

Customize settings:

```json
{
  "ocr_language": "fra+eng", // Your preferred OCR language
  "tts_language": "fr", // Your preferred TTS language
  "camera_resolution": [1280, 720],
  "tts_rate": 150, // Slower: lower number
  "tts_volume": 0.9 // 0.0 to 1.0
}
```

Press `Ctrl+X`, then `Y`, then `Enter` to save (nano editor).

---

## Normal Usage

Each time you work:

```bash
# SSH into Pi
ssh pi@raspberrypi.local

# Navigate to project
cd ~/reading_eye

# Activate environment
source ~/env_projet_7/bin/activate

# Run application
bash run.sh --single --lang fra+eng
# or
bash run.sh --loop --interval 5.0 --lang fra+eng

# Press Ctrl+C to stop
```

---

## Command Reference

### Single Frame Capture

```bash
# Basic
bash run.sh --single

# With language selection
bash run.sh --single --lang ara
bash run.sh --single --lang eng
bash run.sh --single --lang fra
bash run.sh --single --lang fra+eng

# Save captured image
bash run.sh --single --save-image

# Debug mode
bash run.sh --single --verbose
```

### Continuous Loop

```bash
# Default: 5-second interval
bash run.sh --loop

# Custom interval
bash run.sh --loop --interval 10.0

# With duration limit (60 seconds)
bash run.sh --loop --interval 5.0 --duration 60

# Arabic continuous loop
bash run.sh --loop --lang ara --interval 3.0
```

### View Logs

```bash
# Last 20 lines
tail -20 logs/reading_eye.log

# Real-time updates
tail -f logs/reading_eye.log

# Search for errors
grep "ERROR" logs/reading_eye.log
```

### File Management

```bash
# View captured images
ls -la capture/

# Download captured images to your computer
scp pi@raspberrypi.local:~/reading_eye/capture/*.png ./

# Clear old logs
rm logs/*.log
```

---

## Troubleshooting

### Issue: Command not found: bash

**Solution**: You might be using a restricted shell. Try:

```bash
bash setup.sh
bash run.sh --single
```

### Issue: Permission denied on camera

**Solution**: User wasn't added to video group. Contact admin or:

```bash
sudo usermod -aG video pi
# Then log out and back in
exit
ssh pi@raspberrypi.local
```

### Issue: Tesseract not found

**Solution**: System setup wasn't run. Contact admin:

```bash
# If you have sudo access
sudo apt install -y tesseract-ocr
tesseract --list-langs
```

### Issue: Virtual environment not found

**Solution**: Environment at different path:

```bash
# Find it
ls -la ~/
ls -la ~/env_*

# If found, edit run.sh and setup.sh with correct path
# Or create new one:
python3 -m venv ~/env_projet_7
source ~/env_projet_7/bin/activate
pip install -r requirements.txt
```

### Issue: Python module import errors

**Solution**: Ensure environment is activated:

```bash
# Check prompt shows (env_projet_7)
source ~/env_projet_7/bin/activate

# Reinstall packages
pip install --upgrade -r requirements.txt
```

### Issue: No audio output

**Solution**: Check audio setup:

```bash
# Test audio
speaker-test -t sine -f 1000 -l 1
# Ctrl+C to stop

# Check volume
alsamixer
# Use arrow keys, ESC to exit

# Install audio player
sudo apt install -y mpg123
```

### Issue: Camera error "Picamera2 not available"

**Solution**: Camera not properly initialized:

```bash
# Check camera
libcamera-hello -v

# Enable in raspi-config
sudo raspi-config
# Interface Options → Camera → Enable

# Reboot
sudo reboot
```

### Issue: Network disconnection during long run

**Solution**: SSH disconnects after inactivity:

```bash
# Use screen to detach session
screen

# Run your command
bash run.sh --loop --interval 5.0

# Detach: Ctrl+A then D

# Reconnect later
screen -r
```

Or use `nohup`:

```bash
nohup bash run.sh --loop > logs/run.log 2>&1 &
```

---

## Network Best Practices

### SSH Key Authentication (More Secure)

Instead of password each time:

**Generate key on your computer:**

```bash
ssh-keygen -t ed25519 -C "reading-eye-student"
# Just press Enter for default location and no passphrase
```

**Copy to Pi:**

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub pi@raspberrypi.local
```

**Now connect without password:**

```bash
ssh pi@raspberrypi.local
```

### Keep SSH Connection Alive

Add to `~/.ssh/config` on your computer:

```
Host raspberrypi.local
    User pi
    ServerAliveInterval 60
    ServerAliveCountMax 2
```

---

## File Transfer Examples

### Download Captured Images

```bash
# Single image
scp pi@raspberrypi.local:~/reading_eye/capture/capture_20250108_123456.png ./

# All images
scp pi@raspberrypi.local:~/reading_eye/capture/*.png ./

# Download logs
scp pi@raspberrypi.local:~/reading_eye/logs/reading_eye.log ./
```

### Upload Modified Code

```bash
# Upload single file
scp ./my_script.py pi@raspberrypi.local:~/reading_eye/scripts/

# Upload entire scripts folder
scp -r ./scripts pi@raspberrypi.local:~/reading_eye/
```

---

## Advanced: Persistent Background Process

To keep Reading Eye running after SSH disconnect:

```bash
# Using screen
screen -S reading_eye bash run.sh --loop --interval 5.0

# Detach: Ctrl+A + D

# Reconnect:
screen -r reading_eye

# List sessions:
screen -ls
```

Or using `nohup`:

```bash
nohup bash run.sh --loop > logs/background.log 2>&1 &
jobs
```

---

## Data Backup and Sharing

### Backup Your Work

```bash
# On your computer, backup captured data
scp -r pi@raspberrypi.local:~/reading_eye/capture ./backup_capture_$(date +%Y%m%d)/
scp pi@raspberrypi.local:~/reading_eye/logs/reading_eye.log ./backup_logs_$(date +%Y%m%d).log
```

### Share with Group Members

```bash
# You can all access the same ~/reading_eye folder
# Just use different config files if needed

# Create group-specific config:
cp config/reading_eye_config.json config/reading_eye_config_GROUP_A.json
# Edit with your settings
# Use: bash run.sh --config config/reading_eye_config_GROUP_A.json
```

---

## Additional Resources

- **Raspberry Pi Official**: https://www.raspberrypi.com/documentation/
- **Picamera2**: https://www.raspberrypi.com/documentation/computers/camera_software.html
- **Tesseract OCR**: https://github.com/UB-Mannheim/pytesseract
- **SSH Guide**: https://www.digitalocean.com/community/tutorials/how-to-use-ssh-to-connect-to-a-remote-server

---

## Getting Help

1. **Check logs first**: `tail -f logs/reading_eye.log`
2. **Run verbose mode**: `bash run.sh --single --verbose`
3. **Check system health**: `top -b -n 1` and `df -h`
4. **Contact teaching assistant** with:
   - Error message from logs
   - Output of `bash run.sh --single --verbose`
   - Output of `tesseract --version`

---

## FAQ

**Q: Can I use a different Python version?**
A: The project requires Python 3.13.5+. Check with `python3 --version`.

**Q: Can multiple groups work simultaneously?**
A: Yes, each group has isolated virtual environment. Avoid simultaneous camera access.

**Q: How do I change languages?**
A: Edit `config/reading_eye_config.json` or use `--lang` flag: `bash run.sh --single --lang ara`

**Q: Is the code persistent between sessions?**
A: Yes. Everything saved in `~/reading_eye` persists. Virtual environment at `~/env_projet_7` also persists.

**Q: How do I reset to default settings?**
A: Replace config with defaults:

```bash
cp config/reading_eye_config.json.bak config/reading_eye_config.json
# or edit manually
```

---

## Next Steps

1. ✓ Complete this setup
2. ✓ Test with `bash run.sh --single --lang fra+eng`
3. ✓ Customize `config/reading_eye_config.json`
4. ✓ Create your own test scripts in `scripts/`
5. ✓ Document any changes you make

---
