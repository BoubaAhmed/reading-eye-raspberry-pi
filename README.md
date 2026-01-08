# Reading Eye - Raspberry Pi Setup Guide

Complete setup instructions for deploying Reading Eye on Raspberry Pi 5 via SSH.

## Quick Start

### 1. System-Level Setup (Run Once - Requires `sudo`)

```bash
ssh pi@<RASPBERRY_PI_IP>
# ssh raspberryens@192.168.43.197
cd Projet_7_Reading_eye
pwd
ls
sudo bash system_setup.sh
```

This installs:

- Tesseract OCR + language packs (English, French, Arabic)
- Python 3 development tools
- Picamera2 and camera support
- Audio libraries for TTS playback

### 2. Python Environment Setup

After system setup, configure your group's virtual environment:

```bash
bash setup.sh
source ../env_projet_7/bin/activate
```

This creates an isolated Python environment for your group.

### 3. Run the Application

**Single Capture:**

```bash
bash run.sh --single --lang fra+eng --save-image
```

**Continuous Loop (5-second interval):**

```bash
bash run.sh --loop --interval 5.0 --lang fra+eng
```

**Continuous Loop with Duration Limit (60 seconds):**

```bash
bash run.sh --loop --interval 5.0 --duration 60 --lang fra+eng
```

---

## Project Structure

```
raspberry_code/
├── README.md                    # This file
├── setup.sh                     # Python environment setup
├── run.sh                       # Application launcher
├── system_setup.sh             # System-level dependencies (sudo)
├── install_service.sh          # Optional: systemd service setup
│
├── scripts/                    # Main application code
│   ├── __init__.py
│   ├── app_main.py            # Main application entry point
│   ├── camera.py              # Picamera2 wrapper
│   ├── ocr.py                 # Tesseract OCR handler
│   └── tts.py                 # Text-to-Speech engine
│
├── config/                    # Configuration files
│   ├── reading_eye_config.json # Application settings
│   └── .env.example           # Environment variables template
│
├── logs/                      # Application logs
│   └── reading_eye.log
│
└── capture/                   # Captured images (--save-image)
```

---

## Installation Steps

### Prerequisites

- **Raspberry Pi 5** with Raspberry Pi OS (Bookworm or Bullseye)
- **Pi Camera 3** or **Pi Camera Module 3 Wide**
- **SSH Access** from your development machine
- **Python 3.13.5+** (pre-installed on Raspberry Pi OS)
- **Virtual environment** already created: `env_projet_7`

### Step 1: SSH Connection

From your development machine:

```bash
ssh pi@<RASPBERRY_PI_IP>
```

To find your Raspberry Pi's IP address:

```bash
# On the Pi itself
hostname -I

# Or from another machine on the network
ping raspberrypi.local
```

### Step 2: Download/Clone the Code

If using GitHub:

```bash
cd ~
git clone https://github.com/BoubaAhmed/reading-eye-raspberry-pi.git
cd reading-eye-raspberry-pi
```

Or copy via SCP:

```bash
# From your development machine
scp -r raspberry_code/ pi@<RASPBERRY_PI_IP>:~/reading_eye
ssh pi@<RASPBERRY_PI_IP> "cd ~/reading_eye && ls -la"
```

### Step 3: Install System Dependencies

```bash
cd ~/reading_eye
sudo bash system_setup.sh
```

**Output should show:**

- ✓ Camera support installed
- ✓ Tesseract OCR installed
- ✓ Language packs installed (eng, fra, ara)
- ✓ Python dev tools installed

**After this script, log out and back in:**

```bash
exit
ssh pi@<RASPBERRY_PI_IP>
```

### Step 4: Setup Python Environment

```bash
cd ~/reading_eye
bash setup.sh
```

This will:

1. Create virtual environment at `~/env_projet_7`
2. Install Python dependencies from `requirements.txt`
3. Verify all installations
4. Create necessary directories

**Verify installation:**

```bash
source ../env_projet_7/bin/activate
python3 -c "from scripts.ocr import OCR; print('✓ OCR module ready')"
python3 -c "from scripts.tts import TTS; print('✓ TTS module ready')"
python3 -c "from scripts.camera import PiCamera; print('✓ Camera module ready')"
```

---

## Usage

### Activate Virtual Environment

Before running any command, activate your group's environment:

```bash
source ~/env_projet_7/bin/activate
cd ~/reading_eye
```

### Single Frame Capture and Processing

Capture one frame, run OCR, and speak the result:

```bash
bash run.sh --single --lang fra+eng
```

Options:

- `--lang {language}` - OCR language: `eng`, `fra`, `ara`, or `eng+fra`
- `--save-image` - Save captured frame to `capture/` folder
- `--verbose` - Show debug information

Example:

```bash
bash run.sh --single --lang ara --save-image --verbose
```

### Continuous Capture Loop

Continuously capture and process frames at regular intervals:

```bash
bash run.sh --loop --interval 5.0 --lang fra+eng
```

Options:

- `--interval {seconds}` - Wait between captures (default: 5.0)
- `--duration {seconds}` - Total runtime (omit for infinite)
- `--lang {language}` - OCR language

Examples:

```bash
# Loop for 60 seconds, 3-second intervals
bash run.sh --loop --interval 3.0 --duration 60 --lang eng

# Infinite loop, 10-second intervals, French
bash run.sh --loop --interval 10.0 --lang fra

# Arabic, continuous
bash run.sh --loop --lang ara
```

### Stop Running Application

Press `Ctrl+C` to interrupt the application gracefully.

---

## Configuration

### Quick Settings

Edit `config/reading_eye_config.json`:

```json
{
  "ocr_language": "fra+eng", // OCR language
  "tts_language": "fr", // TTS language (fr, en, ar)
  "camera_resolution": [1280, 720], // Camera resolution
  "tts_rate": 150, // Speech rate (words/min)
  "tts_volume": 0.9 // Volume (0.0-1.0)
}
```

### Environment Variables

Copy template:

```bash
cp config/.env.example config/.env
```

Edit `config/.env` with your paths if needed.

---

## Supported Languages

### OCR (Tesseract)

- `eng` - English
- `fra` - French (Français)
- `ara` - Arabic (العربية)
- `deu` - German
- `spa` - Spanish
- `ita` - Italian
- Combinations: `fra+eng`, `ara+eng`, etc.

### Text-to-Speech

- `fr` - French
- `en` - English
- `ar` - Arabic

---

## Troubleshooting

### Camera Not Found

```bash
# Check camera status
libcamera-hello --version
vcgencmd get_camera

# Re-enable camera in raspi-config
sudo raspi-config
# → Interface Options → Camera → Enable
# → Reboot
```

### Tesseract Not Found

```bash
which tesseract
# Should output: /usr/bin/tesseract

# If not installed:
sudo apt install -y tesseract-ocr tesseract-ocr-eng tesseract-ocr-fra tesseract-ocr-ara
```

### Language Pack Missing

```bash
# Check installed languages
tesseract --list-langs

# Install additional language packs
sudo apt install -y tesseract-ocr-ara tesseract-ocr-deu tesseract-ocr-spa
```

### Audio Not Playing

```bash
# Test audio
speaker-test -t sine -f 1000 -l 1

# Install audio player if needed
sudo apt install -y mpg123

# Check ALSA configuration
alsamixer
```

### Virtual Environment Activation Failed

```bash
# Verify environment exists
ls -la ~/env_projet_7/bin/activate

# Re-create if necessary
python3 -m venv ~/env_projet_7
source ~/env_projet_7/bin/activate
pip install -r requirements.txt
```

### Module Import Errors

```bash
# Verify you're in the correct directory
cd ~/reading_eye
pwd

# Activate environment
source ../env_projet_7/bin/activate

# Reinstall packages
pip install --force-reinstall -r requirements.txt
```

---

## Logging

Application logs are saved to `logs/reading_eye.log`:

```bash
# View recent logs
tail -f logs/reading_eye.log

# Search for errors
grep "ERROR" logs/reading_eye.log

# Clear logs
rm logs/reading_eye.log
```

---

## Optional: Systemd Service Setup

To run Reading Eye automatically on startup:

```bash
sudo bash install_service.sh
sudo systemctl enable reading-eye
sudo systemctl start reading-eye
```

Check status:

```bash
sudo systemctl status reading-eye
sudo journalctl -u reading-eye -f
```

---

## Performance Notes

- **Resolution**: 1280x720 recommended (faster processing)
- **Interval**: 5-10 seconds for smooth operation
- **Languages**: Single language faster than combinations
- **CPU Usage**: Expect 30-50% CPU during capture/OCR

For heavy processing:

- Use lower resolution
- Increase capture interval
- Use single OCR language

---

## Security Notes

- **SSH**: Use SSH keys instead of passwords
- **Virtual Environment**: Each group's environment is isolated
- **Logs**: Check logs for sensitive information before sharing
- **Credentials**: Never commit passwords to version control

---

## Extending the Project

### Add Custom Pre/Post Processing

Edit `scripts/app_main.py` and modify:

- `_load_config()` - Add new configuration options
- `capture_single()` - Process before/after OCR
- `_speak_text()` - Custom TTS handling

### Add New Languages

Add to Tesseract:

```bash
sudo apt install -y tesseract-ocr-[LANG_CODE]
```

Update config:

```json
{
  "ocr_language": "fra+eng+ara"
}
```

### Custom Service Scripts

Create new scripts in `scripts/` and run via:

```bash
source ../env_projet_7/bin/activate
python3 scripts/your_script.py
```

---

## Support and Debugging

For detailed debug information:

```bash
bash run.sh --single --verbose
```

Check system health:

```bash
# CPU/Memory
top -b -n 1 | head -20

# Disk space
df -h

# Temperature
vcgencmd measure_temp
```

---

## References

- [Raspberry Pi OS Documentation](https://www.raspberrypi.com/documentation/)
- [Picamera2 Guide](https://www.raspberrypi.com/documentation/computers/camera_software.html)
- [Tesseract OCR](https://github.com/UB-Mannheim/pytesseract)
- [pyttsx3 Documentation](https://pyttsx3.readthedocs.io/)

---

## License and Attribution

Reading Eye - Accessibility Solution for Visually Impaired  
Raspberry Pi Implementation Version 1.0
"# reading-eye-raspberry-pi" 
