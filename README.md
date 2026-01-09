# Reading Eye — Raspberry Pi (Projet_7_Reading_eye)

This repository contains the Raspberry Pi code for the Reading Eye project.
The project folder name used in these instructions is `Projet_7_Reading_eye` and the Python virtual environment name is `env_projet_7`.

**Goal:** capture images with the Pi camera, run Tesseract OCR, and speak detected text via TTS.

## Quick Start (Raspberry Pi)

1. SSH to your Pi:

```bash
ssh raspberryens@<RASPBERRY_PI_IP>
# ssh raspberryens@raspberryens
# ssh raspberryens@192.168.43.197
```

2. Go to the project folder (create or copy the project here):

```bash
cd ~/Projet_7_Reading_eye
```

Clone the repository into this folder (recommended: clone first into an empty folder, then create the venv). Example — clean flow:

```bash
# create project folder and clone into it
mkdir -p ~/Projet_7_Reading_eye
cd ~/Projet_7_Reading_eye
git clone https://github.com/BoubaAhmed/reading-eye-raspberry-pi.git .

# then create venv and activate
python3 -m venv env_projet_7
source env_projet_7/bin/activate
```

If you already created the `env_projet_7` virtualenv inside the folder, you can still clone the repo into the same folder:

```bash
cd ~/Projet_7_Reading_eye
git clone https://github.com/BoubaAhmed/reading-eye-raspberry-pi.git .
# env_projet_7 remains untouched; just activate it
source env_projet_7/bin/activate
```

Note: add `env_projet_7/` to `.gitignore` to avoid committing the virtual environment.

3. Create and activate the virtual environment inside the project folder:

```bash
python3 -m venv env_projet_7
source env_projet_7/bin/activate
```

4. (Optional) Install system-level dependencies (once, requires sudo):

```bash
sudo bash system_setup.sh
```

5. Install Python dependencies:

```bash
pip install -r requirements.txt
```

6. Run the application (examples):

Single capture:

```bash
bash run.sh --single --lang fra+eng --save-image
```

Continuous loop (every 5 s):

```bash
bash run.sh --loop --interval 5.0 --lang fra+eng
```

Press Ctrl+C to stop.

---

## Project layout

```
raspberry_code/
├── README.md
├── setup.sh            # helper: creates venv / installs deps
├── run.sh              # launches capture/OCR/TTS
├── system_setup.sh     # installs system packages (Tesseract, camera libs, audio)
├── install_service.sh  # optional: configure systemd service
├── requirements.txt    # Python dependencies
├── scripts/
│   ├── __init__.py
│   ├── app_main.py
│   ├── camera.py
│   ├── ocr.py
│   └── tts.py
├── config/
│   ├── reading_eye_config.json
│   └── .env.example
├── logs/
└── capture/
```

---

## Important notes (consistency with your environment)

- Project folder: `~/Projet_7_Reading_eye`
- Virtual environment: `env_projet_7` (created inside the project folder)
- Activate the venv with: `source env_projet_7/bin/activate`

If you created the project folder and venv as you described, the exact commands are:

```bash
mkdir -p ~/Projet_7_Reading_eye
cd ~/Projet_7_Reading_eye
python3 -m venv env_projet_7
source env_projet_7/bin/activate
```

Once activated, install Python packages:

```bash
pip install -r requirements.txt
```

---

## Configuration and usage

- Edit settings in `config/reading_eye_config.json` (ocr_language, tts_language, camera resolution, etc.).
- If you need environment variables, copy `config/.env.example` to `config/.env` and edit.

Example config keys:

```json
{
  "ocr_language": "fra+eng",
  "tts_language": "fr",
  "camera_resolution": [1280, 720],
  "tts_rate": 150,
  "tts_volume": 0.9
}
```

---

## Systemd service (optional)

To run the app on boot (optional):

```bash
sudo bash install_service.sh
sudo systemctl enable reading-eye
sudo systemctl start reading-eye
sudo systemctl status reading-eye
```

---

## Troubleshooting (short)

- Virtualenv not found: ensure you ran `python3 -m venv env_projet_7` inside `~/Projet_7_Reading_eye` and activated it with `source env_projet_7/bin/activate`.
- Camera: enable via `sudo raspi-config` → Interface Options → Camera, then reboot.
- Tesseract: `which tesseract` and `tesseract --list-langs` to check installed languages; install via `sudo apt install tesseract-ocr tesseract-ocr-fra tesseract-ocr-eng`.
- Audio: test with `speaker-test` or `mpg123`.

---

If you want, I can also:

- commit these README changes, or
- update `setup.sh` to create `env_projet_7` automatically and install `requirements.txt`.

Report issues or ask for adjustments and I will update the README accordingly.

````

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
````

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
