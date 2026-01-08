# 📖 Reading Eye - Raspberry Pi Implementation

**Accessibility Solution for Visually Impaired Users**  
*OCR + Text-to-Speech running on Raspberry Pi 5 via SSH*

---

## ✨ Features

- 📷 **OCR with Tesseract** - Recognize text in 8+ languages (English, French, Arabic, German, Spanish, etc.)
- 🔊 **Text-to-Speech** - Convert text to speech in multiple languages
- 📱 **Pi Camera 3 Integration** - Capture images with Raspberry Pi official camera
- 🖥️ **SSH-Only Access** - No GUI needed, run everything remotely
- 🔐 **Isolated Environments** - Each group has its own Python virtual environment
- 📝 **Multiple Languages** - Arabic, French, English, and more
- 📊 **Logging & Debugging** - Comprehensive error tracking and debug mode

---

## 🚀 Quick Start

```bash
# 1. Connect via SSH
ssh pi@raspberrypi.local

# 2. Navigate to project
cd ~/reading_eye

# 3. Activate environment (first time: run setup.sh)
source ~/env_projet_7/bin/activate

# 4. Capture and read
bash run.sh --single --lang fra+eng

# 5. Or continuous loop
bash run.sh --loop --interval 5.0 --lang fra+eng
```

---

## 📋 Project Contents

```
raspberry_code/
├── 📚 Documentation
│   ├── README.md                    # Full documentation
│   ├── QUICK_START.md              # 5-minute reference
│   ├── SETUP_INSTRUCTIONS.md       # Detailed guide
│   ├── ADMIN_SETUP_CHECKLIST.md    # For admins
│   └── PROJECT_SUMMARY.md          # Project overview
│
├── 🐍 Python Application
│   ├── scripts/
│   │   ├── app_main.py             # Main application
│   │   ├── camera.py               # Camera handler
│   │   ├── ocr.py                  # OCR engine
│   │   └── tts.py                  # Text-to-speech
│   └── requirements.txt            # Python dependencies
│
├── ⚙️ Configuration
│   ├── config/reading_eye_config.json
│   ├── config/.env
│   └── config/.env.example
│
└── 🔧 Setup Scripts
    ├── setup.sh                    # Python environment setup
    ├── run.sh                      # Application launcher
    ├── system_setup.sh             # System dependencies
    └── install_service.sh          # Optional systemd service
```

---

## 🔧 Installation

### For System Administrators (One-Time)

```bash
# SSH into Raspberry Pi
ssh pi@raspberrypi.local

# Navigate to project folder
cd ~/reading_eye

# Install system dependencies (requires sudo)
sudo bash system_setup.sh

# Reboot to apply group changes
sudo reboot

# After reboot: Setup Python environment
ssh pi@raspberrypi.local
cd ~/reading_eye
bash setup.sh
```

### For Students (Each Session)

```bash
# SSH into Pi
ssh pi@raspberrypi.local

# Activate your group's virtual environment
source ~/env_projet_7/bin/activate

# Navigate to project
cd ~/reading_eye

# Run the application
bash run.sh --single --lang fra+eng
```

---

## 📖 Usage Examples

### Single Frame Capture
```bash
# Capture one frame and process it
bash run.sh --single --lang fra+eng

# Save the captured image
bash run.sh --single --lang fra+eng --save-image

# Debug mode with verbose output
bash run.sh --single --verbose
```

### Continuous Loop
```bash
# Capture every 5 seconds
bash run.sh --loop --interval 5.0 --lang fra+eng

# For 60 seconds only
bash run.sh --loop --interval 5.0 --duration 60 --lang ara

# Arabic, fast interval
bash run.sh --loop --interval 2.0 --lang ara

# Stop with Ctrl+C
```

### Language Options
```bash
--lang eng          # English only
--lang fra          # French only
--lang ara          # Arabic only
--lang eng+fra      # English + French
--lang ara+eng      # Arabic + English
--lang fra+eng+ara  # All three (slower)
```

---

## 🗂️ Folder Structure on Raspberry Pi

```
/home/pi/
├── env_projet_7/              # Shared virtual environment
│   ├── bin/python3
│   ├── lib/python3.13/site-packages/
│   └── bin/activate
│
└── reading_eye/               # Your project folder
    ├── scripts/               # Python code
    ├── config/                # Settings
    ├── logs/                  # Application logs
    ├── capture/               # Saved images (optional)
    └── setup.sh, run.sh, etc.
```

---

## 🛠️ Configuration

### JSON Settings (`config/reading_eye_config.json`)

```json
{
  "ocr_language": "fra+eng",              // Language for text recognition
  "tts_language": "fr",                   // Language for speech (fr, en, ar)
  "camera_resolution": [1280, 720],       // Camera resolution
  "tts_rate": 150,                        // Speech speed (words per minute)
  "tts_volume": 0.9                       // Volume (0.0 to 1.0)
}
```

### Environment Variables (`config/.env`)

Create from `.env.example` and customize paths/settings.

---

## 📱 Supported Languages

### OCR (Text Recognition)
- 🇬🇧 English (eng)
- 🇫🇷 French (fra)
- 🇸🇦 Arabic (ara)
- 🇩🇪 German (deu)
- 🇪🇸 Spanish (spa)
- 🇮🇹 Italian (ita)
- 🇵🇹 Portuguese (por)
- 🇷🇺 Russian (rus)

### Text-to-Speech
- 🇫🇷 French (fr)
- 🇬🇧 English (en)
- 🇸🇦 Arabic (ar)

---

## 🖥️ System Requirements

### Hardware
- Raspberry Pi 5 (4GB+ RAM recommended)
- Pi Camera 3 or Pi Camera Module 3 Wide
- Network connection (WiFi or Ethernet)
- Power supply (27W recommended)

### Software
- Raspberry Pi OS (Bookworm or Bullseye)
- Python 3.13.5+
- Tesseract OCR v5.x
- Git (for cloning repository)

---

## 🧪 Testing

### Verify Installation
```bash
# Activate environment
source ~/env_projet_7/bin/activate
cd ~/reading_eye

# Test single capture
bash run.sh --single --lang fra+eng

# Check logs
tail -f logs/reading_eye.log
```

### Test Different Languages
```bash
bash run.sh --single --lang eng      # English
bash run.sh --single --lang fra      # French
bash run.sh --single --lang ara      # Arabic
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| **Camera not found** | Enable in `sudo raspi-config` → Camera → Enable → Reboot |
| **Tesseract missing** | Run `sudo bash system_setup.sh` |
| **Import errors** | Activate environment: `source ~/env_projet_7/bin/activate` |
| **No audio** | Install: `sudo apt install mpg123` |
| **Disk full** | Clear logs: `rm logs/*.log` |

See **SETUP_INSTRUCTIONS.md** for detailed troubleshooting.

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| **README.md** | Full documentation with all details |
| **QUICK_START.md** | Quick 5-minute reference |
| **SETUP_INSTRUCTIONS.md** | Detailed step-by-step installation guide |
| **ADMIN_SETUP_CHECKLIST.md** | Checklist for system administrators |
| **PROJECT_SUMMARY.md** | Technical project overview |

---

## 🔐 Security Notes

- Uses SSH for secure remote access
- Each group's environment is isolated
- No credentials stored in code
- Check logs before sharing (may contain sensitive info)

---

## 📊 Performance

- **Processing time**: 2-5 seconds per capture
- **CPU usage**: 30-50% during capture/OCR
- **Memory**: ~200MB for Python process
- **Disk space needed**: 2GB+ free (for logs and captures)
- **Recommended resolution**: 1280x720 (balance of speed/quality)

---

## 🚀 Next Steps

1. **First time setup**: Follow SETUP_INSTRUCTIONS.md
2. **Daily usage**: Use QUICK_START.md
3. **Configuration**: Edit `config/reading_eye_config.json`
4. **Troubleshooting**: Check `logs/reading_eye.log`
5. **Extensions**: Modify `scripts/app_main.py` for custom features

---

## 📝 Code Structure

### Main Application (`scripts/app_main.py`)
- CLI interface with argparse
- Single capture and loop modes
- Configuration management
- Logging and error handling

### Camera Module (`scripts/camera.py`)
- Picamera2 wrapper
- Frame capture and conversion
- Grayscale processing for OCR

### OCR Module (`scripts/ocr.py`)
- Tesseract integration
- Multi-language support
- Text cleaning and normalization

### TTS Module (`scripts/tts.py`)
- pyttsx3 for offline speech
- gTTS as fallback
- Background worker for non-blocking speech
- Audio playback integration

---

## 🔗 Useful Links

- [Raspberry Pi Official Docs](https://www.raspberrypi.com/documentation/)
- [Picamera2 Documentation](https://www.raspberrypi.com/documentation/computers/camera_software.html)
- [Tesseract OCR](https://github.com/UB-Mannheim/pytesseract)
- [pyttsx3 Guide](https://pyttsx3.readthedocs.io/)

---

## 📄 License

This project is part of the Robotics course at MasterSIE.

---

## 👥 Contributors

**Reading Eye Development Team**  
MasterSIE - Semestre 3 - Robotics Project

---

## 💡 Tips & Tricks

### Keep SSH Connection Alive
```bash
# Add to ~/.ssh/config on your computer
Host raspberrypi.local
    ServerAliveInterval 60
    ServerAliveCountMax 2
```

### Use SSH Keys (More Secure)
```bash
# Generate key on your computer
ssh-keygen -t ed25519 -C "reading-eye"

# Copy to Pi
ssh-copy-id -i ~/.ssh/id_ed25519.pub pi@raspberrypi.local

# Now login without password
ssh pi@raspberrypi.local
```

### Run in Background
```bash
# Using screen
screen -S reading_eye bash run.sh --loop

# Detach: Ctrl+A + D
# Reconnect: screen -r reading_eye

# Using nohup
nohup bash run.sh --loop > logs/run.log 2>&1 &
```

### Transfer Files
```bash
# Download from Pi
scp pi@raspberrypi.local:~/reading_eye/capture/*.png ./

# Upload to Pi
scp ./my_script.py pi@raspberrypi.local:~/reading_eye/scripts/
```

---

## ❓ FAQ

**Q: Can multiple groups use the same Pi?**  
A: Yes! Each group uses the same `env_projet_7`, but you can create separate configs if needed.

**Q: How do I change languages?**  
A: Edit `config/reading_eye_config.json` or use `--lang` flag: `bash run.sh --single --lang ara`

**Q: Is my data private?**  
A: All processing happens locally on the Pi. Logs are stored locally, check before sharing.

**Q: Can I add more languages?**  
A: Yes! Install language packs: `sudo apt install tesseract-ocr-[lang-code]`

**Q: What if I get permission errors?**  
A: Run `sudo usermod -aG video pi` and reboot.

---

**Reading Eye - Making Reading Accessible** 🎯

