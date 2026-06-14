#!/bin/bash
# Dusk — Install Script
# Run on Raspberry Pi OS Lite after fresh flash.
# Usage: sudo ./scripts/install.sh

set -e

echo ""
echo "=================================="
echo "  DUSK — Installation"
echo "=================================="
echo ""

# 1. Update system
echo "[1/7] Updating system..."
apt-get update -qq && apt-get upgrade -y -qq

# 2. Install dependencies
echo "[2/7] Installing dependencies..."
apt-get install -y -qq \
    python3 python3-pip python3-pygame \
    curl git alsa-utils \
    dbus python3-dbus \
    fonts-dejavu-core

# 3. Install raspotify (Spotify Connect)
echo "[3/7] Installing raspotify..."
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh

# 4. Configure pHAT DAC
echo "[4/7] Configuring pHAT DAC..."
if ! grep -q "dtoverlay=hifiberry-dac" /boot/config.txt; then
    echo "dtoverlay=hifiberry-dac" >> /boot/config.txt
    echo "Added hifiberry-dac overlay"
fi
if ! grep -q "dtparam=audio=off" /boot/config.txt; then
    echo "dtparam=audio=off" >> /boot/config.txt
    echo "Disabled onboard audio"
fi

# 5. Write ALSA config
echo "[5/7] Configuring ALSA..."
cat > /etc/asound.conf << 'ASOUND'
pcm.!default {
    type hw
    card sndrpihifiberry
}
ctl.!default {
    type hw
    card sndrpihifiberry
}
ASOUND

# 6. Install Python deps
echo "[6/7] Installing Python packages..."
pip3 install RPi.GPIO pygame requests --break-system-packages -q

# 7. Install systemd service
echo "[7/7] Installing dusk.service..."
cp /home/pi/dusk/scripts/dusk.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable dusk.service

echo ""
echo "=================================="
echo "  Installation complete!"
echo ""
echo "  Next step: configure Spotify"
echo "  nano /etc/raspotify/conf"
echo ""
echo "  Then reboot:"
echo "  sudo reboot"
echo "=================================="
