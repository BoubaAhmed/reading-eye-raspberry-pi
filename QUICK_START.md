# Reading Eye - Raspberry Pi SSH Setup (Quick Reference)

## First Time Setup (15-30 minutes)

### 1. Connect to Raspberry Pi

```bash
ssh pi@raspberrypi.local
# or: ssh pi@<IP_ADDRESS>
```

### 2. Navigate to Project

```bash
cd ~/reading_eye
```

### 3. System Setup (First User Only - Requires sudo)

```bash
sudo bash system_setup.sh
# Log out and back in
exit
ssh pi@raspberrypi.local
```

### 4. Python Environment Setup

```bash
cd ~/reading_eye
bash setup.sh
```

### 5. Test It

```bash
bash run.sh --single --lang fra+eng
```

---

## Every Session - Activate Environment

```bash
source ~/env_projet_7/bin/activate
cd ~/reading_eye
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

Use PuTTY or Windows PowerShell:

```powershell
ssh pi@<IP_ADDRESS>
```

Or use Visual Studio Code Remote SSH extension.

---

## Transfer Files via SCP

From your computer to Pi:

```bash
scp -r raspberry_code/ pi@<IP_ADDRESS>:~/reading_eye
```

From Pi to your computer:

```bash
scp pi@<IP_ADDRESS>:~/reading_eye/capture/image.png ./
```

---

## Next Steps

- Read full `README.md` for detailed documentation
- Edit `config/reading_eye_config.json` for custom settings
- Check `logs/reading_eye.log` for troubleshooting

---
