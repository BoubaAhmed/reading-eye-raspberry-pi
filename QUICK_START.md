# Reading Eye — Raspberry Pi SSH Setup (Quick Reference)

## First Time Setup (15-30 minutes)

### 1. Connect to Raspberry Pi

```bash
ssh raspberryens@<RASPBERRY_PI_IP>
# or: ssh raspberryens@192.168.43.197
```

### 2. Create project folder and clone the repository

If you don't yet have the project on the Pi, create the project folder and clone into it:

```bash
nmkdir -p ~/Projet_7_Reading_eye
cd ~/Projet_7_Reading_eye
git clone https://github.com/BoubaAhmed/reading-eye-raspberry-pi.git .
```

If you already created the `env_projet_7` venv inside the folder, just `cd` into the folder and clone:

```bash
cd ~/Projet_7_Reading_eye
git clone https://github.com/BoubaAhmed/reading-eye-raspberry-pi.git .
```

> Tip: add `env_projet_7/` to `.gitignore` so the virtualenv is not committed.

### 3. System Setup (First User Only - Requires sudo)

```bash
sudo bash system_setup.sh
# Log out and back in if the script instructs to do so
exit
ssh raspberryens@<RASPBERRY_PI_IP>
```

### 4. Create / activate Python virtual environment

Create the venv (if not already created) and activate it:

```bash
# from inside ~/Projet_7_Reading_eye
python3 -m venv env_projet_7
source env_projet_7/bin/activate
```

### 5. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 6. Test It

```bash
bash run.sh --single --lang fra+eng
```

---

## Every Session - Activate Environment

```bash
nsource ~/Projet_7_Reading_eye/env_projet_7/bin/activate
cd ~/Projet_7_Reading_eye
```

---

## Common Commands

| Command                                            | What It Does           |
| -------------------------------------------------- | ---------------------- |
| `bash run.sh --single --lang fra+eng`              | Capture & read once    |
| `bash run.sh --loop --interval 5.0 --lang fra+eng` | Continuous reading     |
| `bash run.sh --single --lang ara`                  | Arabic single capture  |
| `tail -f logs/reading_eye.log`                     | View logs in real-time |
| `Ctrl+C`                                           | Stop running app       |

---

## Languages

Use any of these for `--lang`:

- `eng` (English)
- `fra` (French)
- `ara` (Arabic)
- `eng+fra` (English + French combined)
- `ara+eng` (Arabic + English combined)

---

## Troubleshooting

| Problem                      | Solution                                                |
| ---------------------------- | ------------------------------------------------------- |
| `Command not found: python3` | Update system: `sudo apt update && sudo apt upgrade`    |
| Camera not working           | `vcgencmd get_camera` and enable in `sudo raspi-config` |
| No audio                     | Install: `sudo apt install -y mpg123 alsa-utils`        |
| Permission denied on camera  | Reboot after `system_setup.sh`                          |
| Import errors                | Make sure environment is activated with `source`        |

---

## SSH from Windows

Use PowerShell or PuTTY:

```powershell
ssh raspberryens@<IP_ADDRESS>
```

Or use Visual Studio Code Remote SSH extension.

---

## Transfer Files via SCP

From your computer to Pi:

```bash
scp -r raspberry_code/ raspberryens@<IP_ADDRESS>:~/Projet_7_Reading_eye
```

From Pi to your computer:

```bash
scp raspberryens@<IP_ADDRESS>:~/Projet_7_Reading_eye/capture/image.png ./
```

---

## Next Steps

- Read full `README.md` for detailed documentation
- Edit `config/reading_eye_config.json` for custom settings
- Check `logs/reading_eye.log` for troubleshooting

---
