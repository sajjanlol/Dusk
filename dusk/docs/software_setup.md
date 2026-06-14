# Dusk — Software Setup Guide

## Prerequisites

- Raspberry Pi Zero 2 W with Raspberry Pi OS Lite (64-bit)
- Spotify Premium account
- WiFi network

---

## Step 1 — Flash the OS

Download Raspberry Pi OS Lite (64-bit) from raspberrypi.com/software

Flash to MicroSD using Raspberry Pi Imager.

Before ejecting, create two files on the boot partition:

```bash
# Enable SSH
touch /boot/ssh

# Configure WiFi
cat > /boot/wpa_supplicant.conf << EOF
country=IN
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
    ssid="YourWiFiName"
    psk="YourWiFiPassword"
}
EOF
```

---

## Step 2 — Run Install Script

```bash
git clone https://github.com/yourusername/dusk.git
cd dusk
sudo chmod +x scripts/install.sh
sudo ./scripts/install.sh
```

---

## Step 3 — Configure Spotify

```bash
sudo nano /etc/raspotify/conf
```

Set:
```
LIBRESPOT_NAME="Dusk"
LIBRESPOT_BITRATE="320"
LIBRESPOT_USERNAME="your@email.com"
LIBRESPOT_PASSWORD="yourpassword"
```

---

## Step 4 — Reboot and Test

```bash
sudo reboot
```

After reboot:
1. Open Spotify on your phone or laptop
2. Play any song
3. Tap the Connect button (speaker icon)
4. Select **"Dusk"** from the device list
5. Music should stream through your headphones

---

## Step 5 — Verify Button Handler

```bash
cd dusk
python3 src/system/boot.py
```

Press each button zone and confirm logs show correct actions.

---

## Troubleshooting

| Issue | Fix |
|---|---|
| "Dusk" not appearing in Spotify | `sudo systemctl status raspotify` |
| Auth failed | Check credentials in `/etc/raspotify/conf` |
| No audio | `aplay -l` — verify pHAT DAC detected |
| Buttons not responding | `gpio readall` — check pin connections |
| Service won't start | `sudo journalctl -u dusk -f` |
