# Raspberry Pi One-Time Admin Setup Checklist

Complete this checklist once per Raspberry Pi for the entire class.

## Pre-Deployment (on your computer)

- [ ] Download `raspberry_code/` folder
- [ ] Review documentation in README.md
- [ ] Test locally if possible

## Initial Raspberry Pi Setup

### 1. Basic OS Setup

- [ ] Flash Raspberry Pi OS (Bookworm or Bullseye)
- [ ] Boot and connect to network
- [ ] Find IP: `ping raspberrypi.local` or check router
- [ ] SSH in: `ssh pi@raspberrypi.local`
- [ ] Update password: `passwd`
- [ ] Update OS:
  ```bash
  sudo apt update && sudo apt upgrade -y
  sudo reboot
  ```

### 2. Hardware Setup

- [ ] Connect Pi Camera 3 Module (Camera connector, not USB-C)
- [ ] Power on Pi
- [ ] Test camera: `libcamera-hello -v`

### 3. System Dependencies (Run on Pi)

```bash
cd ~
# Copy raspberry_code folder here or git clone
sudo bash raspberry_code/system_setup.sh
sudo reboot
```

Verify after reboot:

- [ ] `tesseract --version` (should show v5+)
- [ ] `tesseract --list-langs` (should show eng, fra, ara)
- [ ] `libcamera-hello -v` works
- [ ] `python3 --version` (3.13.5+)

### 4. Python Virtual Environment (Create Once)

```bash
ssh pi@raspberrypi.local
cd ~
python3 -m venv env_projet_7
source env_projet_7/bin/activate
pip install --upgrade pip
pip install -r raspberry_code/requirements.txt
deactivate
```

Verify:

- [ ] `ls -la ~/env_projet_7/bin/activate` exists
- [ ] `source ~/env_projet_7/bin/activate` works

### 5. Initial Test

```bash
cd ~/raspberry_code
bash setup.sh
bash run.sh --single --lang fra+eng
```

- [ ] Capture successful
- [ ] OCR detected text (if text in image)
- [ ] Audio played (if TTS enabled)
- [ ] No errors in logs

### 6. Documentation

- [ ] Copy/upload QUICK_START.md to shared location
- [ ] Copy SETUP_INSTRUCTIONS.md to shared location
- [ ] Post IP address and credentials in secure location

---

## For Each Student Group

Provide them with:

- [ ] Raspberry Pi IP address
- [ ] SSH credentials (username/password or SSH key)
- [ ] QUICK_START.md
- [ ] Link to full SETUP_INSTRUCTIONS.md
- [ ] Pi is in their SSH access group

### Pre-class Verification (Optional)

For each group before first session:

```bash
ssh pi@raspberrypi.local

# Test their virtual environment
source ~/env_projet_7/bin/activate

# Test camera
cd ~/raspberry_code
bash run.sh --single --lang fra+eng

# Test different languages
bash run.sh --single --lang ara
bash run.sh --single --lang eng
```

---

## Ongoing Maintenance

### Weekly

- [ ] Check disk space: `df -h` (should have >2GB free)
- [ ] Clear old logs: `rm logs/reading_eye_*.log` older than 1 week
- [ ] Monitor CPU temp: `vcgencmd measure_temp` (should be <60°C)

### Monthly

- [ ] Check for Pi OS updates: `sudo apt update && sudo apt upgrade`
- [ ] Test all cameras still working
- [ ] Verify all language packs installed: `tesseract --list-langs`
- [ ] Check for sufficient disk space

### End of Semester

- [ ] Backup any student work
- [ ] Archive logs and captures
- [ ] Clean `/tmp` directory: `sudo rm -rf /tmp/*`
- [ ] Optional: Fresh reinstall of system

---

## Troubleshooting Quick Reference

| Issue                       | Quick Fix                                                                             |
| --------------------------- | ------------------------------------------------------------------------------------- |
| Camera error on first run   | `sudo raspi-config` → Camera → Enable → Reboot                                        |
| Students can't SSH in       | Check IP, firewall, check `/etc/ssh/sshd_config`                                      |
| Tesseract missing languages | `sudo apt install -y tesseract-ocr-ara tesseract-ocr-fra`                             |
| Disk full                   | Remove old logs: `rm logs/*.log`                                                      |
| Python import errors        | `source ~/env_projet_7/bin/activate` and reinstall: `pip install -r requirements.txt` |
| Permissions on camera       | `sudo usermod -aG video $USER` and reboot                                             |

---

## Useful Commands for Admin

```bash
# Connect to Pi
ssh pi@raspberrypi.local

# Check disk usage
du -sh ~/.

# Clear disk space
rm -rf capture/*.png  # Clear old captures
rm logs/*.log         # Clear old logs

# Restart Pi
sudo reboot

# Check Pi info
cat /proc/device-tree/model
cat /proc/cpuinfo | grep Processor

# Update all language packs
sudo apt install -y tesseract-ocr-{eng,fra,ara,deu,spa,ita}

# Test audio
speaker-test -t sine -f 1000 -l 1  # Ctrl+C to stop

# Monitor system
top
watch -n 1 vcgencmd measure_temp

# Check SSH logs
sudo journalctl -u ssh -f
```

---

## Security Considerations

- [ ] Change default password from 'raspberry'
- [ ] Use SSH keys instead of passwords (see SETUP_INSTRUCTIONS.md)
- [ ] Disable root login: Edit `/etc/ssh/sshd_config`
- [ ] Set up firewall: `sudo apt install ufw`
- [ ] Enable automatic updates: `sudo apt install unattended-upgrades`

---

## Backup and Recovery

### Backup Before Semester

```bash
# On your computer
mkdir ~/raspberry_pi_backup_$(date +%Y%m%d)
cd ~/raspberry_pi_backup_$(date +%Y%m%d)

# Backup entire home directory
rsync -avz -e ssh pi@raspberrypi.local:~/ ./

# This preserves everything needed for recovery
```

### Restore from Backup

```bash
rsync -avz -e ssh ./home_backup/ pi@raspberrypi.local:~/
```

---

## Documentation for Students

Print or share these files with students:

1. **QUICK_START.md** - Basic quick reference (1 page)
2. **SETUP_INSTRUCTIONS.md** - Detailed setup guide (5 pages)
3. **README.md** - Full documentation with troubleshooting

---

## Notes

- **OS Version**: Test with Bookworm (latest) - Bullseye should also work
- **Python Version**: Requires 3.13.5+ (pre-installed on recent OS)
- **Storage**: Need at least 2GB free for logs and captures
- **Network**: Ensure stable WiFi or use Ethernet for better reliability

---

Last Updated: 2025-01-08
