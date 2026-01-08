# Reading Eye Raspberry Pi Implementation - Project Summary

## Project Overview

**Reading Eye** is an accessibility solution that combines:

- **OCR (Optical Character Recognition)** using Tesseract for text extraction from images
- **Text-to-Speech (TTS)** for audio output in multiple languages
- **Pi Camera 3 Integration** for capturing images on Raspberry Pi

The application helps visually impaired users read text from books, documents, and signs using a Raspberry Pi 5 accessed entirely via SSH.

### Supported Languages

- **OCR**: English (eng), French (fra), Arabic (ara), German, Spanish, Italian, Portuguese, Russian
- **TTS**: French, English, Arabic

---

## Project Structure

```
raspberry_code/
│
├── README.md                          # Full documentation
├── QUICK_START.md                     # Quick reference guide
├── SETUP_INSTRUCTIONS.md              # Detailed step-by-step guide
├── ADMIN_SETUP_CHECKLIST.md          # For system administrators
│
├── scripts/                           # Main Python application
│   ├── __init__.py                   # Package initialization
│   ├── app_main.py                   # Main application entry point
│   ├── camera.py                     # Picamera2 wrapper
│   ├── ocr.py                        # Tesseract OCR handler
│   └── tts.py                        # Text-to-Speech engine
│
├── config/                            # Configuration files
│   ├── reading_eye_config.json       # Application settings (JSON)
│   ├── .env.example                  # Environment variables template
│   └── .env                          # Environment variables (copy from example)
│
├── setup.sh                           # Python environment setup script
├── run.sh                             # Application launcher
├── system_setup.sh                    # System dependencies setup (requires sudo)
├── install_service.sh                 # Optional systemd service installer
│
├── logs/                              # Application logs (created at runtime)
│   └── reading_eye.log
│
├── capture/                           # Captured images (created at runtime)
│   └── capture_YYYYMMDD_HHMMSS.png
│
└── .gitignore                         # Git ignore file
```

---

## Key Features

### 1. **Multi-Language Support**

- OCR: 8+ languages with combinations (e.g., "fra+eng")
- TTS: French, English, Arabic
- Easy to add more languages via Tesseract

### 2. **SSH-Only Access**

- No GUI required - fully headless operation
- Works over network from any machine
- Secure remote access via SSH credentials or keys

### 3. **Isolated Virtual Environments**

- Each group can have separate Python environment
- No conflicts between student groups
- Easy dependency management

### 4. **Flexible Capture Modes**

- **Single capture**: Take one photo and process
- **Loop mode**: Continuous capture at intervals
- **Save images**: Optional image storage for analysis

### 5. **Easy Configuration**

- JSON-based settings
- Environment variables support
- Per-group customization

### 6. **Comprehensive Logging**

- All operations logged to `logs/reading_eye.log`
- Debug mode with verbose output
- Error tracking and troubleshooting

---

## Hardware Requirements

- **Raspberry Pi 5** (4GB+ RAM recommended)
- **Pi Camera 3** or **Pi Camera Module 3 Wide**
- **Network connection** (WiFi or Ethernet)
- **Power supply** (27W recommended)
- **Micro SD card** (32GB+ recommended)

---

## Software Stack

### System Level

- **OS**: Raspberry Pi OS (Bookworm/Bullseye)
- **Python**: 3.13.5+
- **Tesseract OCR**: v5.x
- **Camera Support**: Picamera2

### Python Packages

| Package                | Version | Purpose                  |
| ---------------------- | ------- | ------------------------ |
| numpy                  | 1.26.4  | Array operations         |
| opencv-python-headless | 4.8.1   | Image processing         |
| pytesseract            | 0.3.10  | OCR binding              |
| pyttsx3                | 2.90    | Text-to-speech (offline) |
| gTTS                   | 2.4.0   | Google TTS (online)      |
| pygame                 | 2.5.2   | Audio playback           |

---

## Usage Modes

### Mode 1: Single Capture (One-Shot)

```bash
bash run.sh --single --lang fra+eng
```

Perfect for testing, debugging, or reading a single document.

### Mode 2: Continuous Loop

```bash
bash run.sh --loop --interval 5.0 --lang fra+eng
```

Continuously reads text at regular intervals. Good for:

- Monitoring changing text
- Real-time document reading
- Accessibility for interactive use

### Mode 3: Timed Loop

```bash
bash run.sh --loop --interval 5.0 --duration 60 --lang ara
```

Runs for a specific duration, useful for demonstrations and testing.

---

## Installation Summary

### For Administrators (One-Time)

1. Flash Raspberry Pi OS
2. Connect camera
3. SSH into Pi
4. Run `sudo bash system_setup.sh`
5. Create virtual environment
6. Run `bash setup.sh`
7. Test with `bash run.sh --single`

### For Students (Each Session)

1. SSH into Raspberry Pi
2. Activate environment: `source ~/env_projet_7/bin/activate`
3. Navigate to project: `cd ~/reading_eye`
4. Run application: `bash run.sh --single` or `bash run.sh --loop`
5. Configure in `config/reading_eye_config.json` as needed

---

## Configuration Options

### application Settings (JSON)

```json
{
  "ocr_language": "fra+eng", // Tesseract language codes
  "tts_language": "fr", // TTS language (fr, en, ar)
  "camera_resolution": [1280, 720], // Width x Height
  "tts_rate": 150, // Speech speed (words/min)
  "tts_volume": 0.9, // Volume (0.0-1.0)
  "tesseract_path": "/usr/bin/tesseract",
  "tessdata_prefix": "/usr/share/tesseract-ocr"
}
```

### Environment Variables (.env)

Set in `config/.env` for alternative configuration:

```bash
OCR_LANGUAGE=ara+eng
TTS_LANGUAGE=ar
CAMERA_RESOLUTION=1280x720
TTS_RATE=120
TTS_VOLUME=0.8
```

---

## Troubleshooting Quick Reference

| Problem           | Solution                                            |
| ----------------- | --------------------------------------------------- |
| Camera not found  | Enable in `raspi-config`, reboot                    |
| Tesseract missing | `sudo apt install tesseract-ocr`                    |
| Import errors     | Activate venv: `source ~/env_projet_7/bin/activate` |
| No audio output   | Install: `sudo apt install mpg123 alsa-utils`       |
| Disk full         | Clear logs: `rm logs/*.log`                         |

See **SETUP_INSTRUCTIONS.md** for detailed troubleshooting.

---

## Performance Notes

- **Resolution**: 1280x720 is recommended (good speed/quality balance)
- **Capture Interval**: 5-10 seconds typical for smooth operation
- **Processing Time**: 2-5 seconds per capture depending on language
- **CPU Usage**: 30-50% during capture/OCR
- **Memory**: ~200MB for Python process

---

## Security Considerations

- ✓ Uses SSH for secure remote access
- ✓ Virtual environments isolate dependencies
- ✓ No sensitive credentials in code
- ✓ Logs stored locally (check before sharing)
- ✓ Camera access limited to video group

---

## Extension Points

The architecture is designed for easy extension:

1. **New Languages**: Add Tesseract language packs
2. **Custom Processing**: Edit `app_main.py` capture methods
3. **Alternative TTS**: Switch gTTS or add new TTS backend
4. **Robot Integration**: Add robot control in main loop
5. **Web Dashboard**: Add Flask/Django interface over SSH tunnel

---

## File Descriptions

### Python Scripts

**app_main.py** (350+ lines)

- Main entry point with CLI interface
- Handles single capture and continuous loop modes
- Configuration management
- Error handling and logging

**camera.py** (100+ lines)

- Picamera2 wrapper for Raspberry Pi camera
- Frame capture, grayscale conversion
- Image saving functionality
- Context manager for resource management

**ocr.py** (200+ lines)

- Tesseract OCR integration
- Multi-language support
- Text cleaning and normalization
- Language availability checking
- Auto-detection of paths

**tts.py** (250+ lines)

- pyttsx3 for offline TTS
- gTTS as fallback for better quality
- Background worker thread for non-blocking speech
- Multi-language support
- Audio playback integration

### Configuration Files

**reading_eye_config.json**

- Application-wide settings
- OCR and TTS parameters
- Camera resolution
- Paths to system tools

**.env / .env.example**

- Environment variable definitions
- Sensitive paths and credentials
- Language preferences

### Setup Scripts

**setup.sh**

- Creates/verifies virtual environment
- Installs Python dependencies
- Verifies installations
- Creates necessary directories

**run.sh**

- Simple wrapper for running app
- Activates virtual environment
- Passes arguments to app

**system_setup.sh** (requires sudo)

- Installs OS-level dependencies
- Installs Tesseract and languages
- Installs Python dev tools
- Sets up user permissions

**install_service.sh** (optional)

- Creates systemd service
- Allows auto-start on boot
- For persistent background operation

### Documentation

**README.md** (comprehensive)

- Complete usage documentation
- Troubleshooting guide
- Performance notes
- Extension guidelines

**QUICK_START.md** (quick reference)

- Quick 5-minute setup
- Common commands
- Minimal setup steps

**SETUP_INSTRUCTIONS.md** (detailed)

- Step-by-step installation
- Network configuration
- Advanced usage
- Security best practices

**ADMIN_SETUP_CHECKLIST.md**

- One-time setup checklist
- Maintenance procedures
- Backup procedures
- Monitoring commands

---

## Deployment Checklist

- [ ] Raspberry Pi 5 with current OS
- [ ] Pi Camera 3 connected and tested
- [ ] Network connectivity verified
- [ ] SSH access tested
- [ ] `system_setup.sh` completed
- [ ] Virtual environment created and tested
- [ ] `setup.sh` completed successfully
- [ ] Single capture test passes
- [ ] All languages working
- [ ] Logs being written correctly
- [ ] Disk space verified (2GB+ free)
- [ ] Documentation shared with students

---

## Success Criteria

The project is ready when:

✓ **Functionality**

- Single capture works with multiple languages
- Continuous loop runs without errors
- OCR detects text in images
- TTS speaks text clearly

✓ **Reliability**

- No crashes during normal operation
- Logs show clean operation
- Handles long capture sessions (30+ minutes)

✓ **Accessibility**

- Easy SSH access for students
- Clear documentation
- Quick setup (< 30 minutes)

✓ **Maintainability**

- Code is well-commented
- Configuration is flexible
- Easy to troubleshoot issues
- Simple to extend with new features

---

## Support and Maintenance

### For Students

- Use QUICK_START.md for fast reference
- Check logs for errors: `tail logs/reading_eye.log`
- Run with `--verbose` for debugging

### For Instructors/Admins

- Check ADMIN_SETUP_CHECKLIST.md for maintenance
- Monitor disk space weekly
- Update packages monthly
- Archive logs at semester end

---

## Version Information

- **Version**: 1.0.0
- **Created**: January 2025
- **Python**: 3.13.5+
- **Raspberry Pi OS**: Bookworm (Bullseye compatible)
- **Last Updated**: 2025-01-08

---

## Resources

- [Raspberry Pi Official Documentation](https://www.raspberrypi.com/documentation/)
- [Picamera2 Documentation](https://www.raspberrypi.com/documentation/computers/camera_software.html)
- [Tesseract OCR](https://github.com/UB-Mannheim/pytesseract)
- [pyttsx3 Documentation](https://pyttsx3.readthedocs.io/)
- [Google TTS (gTTS)](https://github.com/pndurette/gTTS)

---

**Reading Eye Project**  
Accessibility Solution for Visually Impaired Users  
Raspberry Pi 5 Implementation
