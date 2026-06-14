#!/bin/bash
# ============================================================
#  DUSK — Full Setup Script
#  Raspberry Pi Zero 2 W / Ubuntu Server 22.04
#  Run with: sudo ./install.sh
# ============================================================

set -e

GREEN='\033[0;32m'
DIM='\033[2m'
RESET='\033[0m'
BOLD='\033[1m'

log()  { echo -e "${GREEN}[DUSK]${RESET} $1"; }
info() { echo -e "${DIM}       $1${RESET}"; }
done_() { echo -e "${GREEN}[✓]${RESET} $1"; }

echo ""
echo -e "${BOLD}  ██████╗ ██╗   ██╗███████╗██╗  ██╗${RESET}"
echo -e "${BOLD}  ██╔══██╗██║   ██║██╔════╝██║ ██╔╝${RESET}"
echo -e "${BOLD}  ██║  ██║██║   ██║███████╗█████╔╝ ${RESET}"
echo -e "${BOLD}  ██║  ██║██║   ██║╚════██║██╔═██╗ ${RESET}"
echo -e "${BOLD}  ██████╔╝╚██████╔╝███████║██║  ██╗${RESET}"
echo -e "${BOLD}  ╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═╝${RESET}"
echo ""
echo -e "  ${DIM}Standalone Spotify Device — Setup v0${RESET}"
echo ""

# ── STEP 1: System update ────────────────────────────────────
log "Updating system packages..."
apt-get update -qq && apt-get upgrade -y -qq
done_ "System updated"

# ── STEP 2: Install dependencies ─────────────────────────────
log "Installing dependencies..."
apt-get install -y -qq \
    curl \
    wget \
    git \
    python3 \
    python3-pip \
    alsa-utils \
    libasound2-dev \
    libssl-dev \
    avahi-daemon \
    systemd
done_ "Dependencies installed"

# ── STEP 3: Install raspotify ─────────────────────────────────
log "Installing raspotify (Spotify Connect daemon)..."
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
done_ "raspotify installed"

# ── STEP 4: Configure raspotify ──────────────────────────────
log "Writing raspotify configuration..."
cat > /etc/raspotify/conf << 'CONF'
# ── Dusk Device Configuration ──────────────────────────────
# Device name shown in Spotify Connect
LIBRESPOT_NAME="Dusk"

# Audio quality — 320kbps for best quality
LIBRESPOT_BITRATE="320"

# Device type shown in Spotify app
LIBRESPOT_DEVICE_TYPE="speaker"

# Spotify credentials (set these to your account)
# LIBRESPOT_USERNAME="your_spotify_email"
# LIBRESPOT_PASSWORD="your_spotify_password"

# Initial volume (0-100)
LIBRESPOT_INITIAL_VOLUME="80"

# Normalise volume across tracks
LIBRESPOT_ENABLE_VOLUME_NORMALISATION=""

# Cache for faster track loading
LIBRESPOT_CACHE="/tmp/dusk-cache"
CONF

done_ "raspotify configured"

# ── STEP 5: Install Python GPIO dependencies ──────────────────
log "Installing Python GPIO libraries..."
pip3 install -q gpiozero RPi.GPIO spotipy requests 2>/dev/null || \
pip3 install -q --break-system-packages gpiozero RPi.GPIO spotipy requests 2>/dev/null || true
done_ "Python libraries installed"

# ── STEP 6: Copy Dusk button controller ──────────────────────
log "Installing Dusk button controller..."
if [ -f "software/gpio/buttons.py" ]; then
    cp software/gpio/buttons.py /usr/local/bin/dusk-buttons.py
    chmod +x /usr/local/bin/dusk-buttons.py
fi
done_ "Button controller installed"

# ── STEP 7: Setup systemd services ───────────────────────────
log "Configuring systemd services..."

# Enable raspotify to start on boot
systemctl enable raspotify
systemctl start raspotify

# Create button controller service
cat > /etc/systemd/system/dusk-buttons.service << 'SERVICE'
[Unit]
Description=Dusk Physical Button Controller
After=raspotify.service
Wants=raspotify.service

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/dusk-buttons.py
Restart=always
RestartSec=3
User=root

[Install]
WantedBy=multi-user.target
SERVICE

systemctl daemon-reload

if [ -f "/usr/local/bin/dusk-buttons.py" ]; then
    systemctl enable dusk-buttons.service
fi

done_ "Systemd services configured"

# ── STEP 8: Audio configuration ───────────────────────────────
log "Configuring audio output..."
if [ -f "software/audio/audio-setup.sh" ]; then
    bash software/audio/audio-setup.sh
fi
done_ "Audio configured"

# ── DONE ─────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo -e "${GREEN}  Dusk setup complete.${RESET}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
echo ""
echo "  Next steps:"
echo "  1. Add your Spotify credentials:"
echo "     sudo nano /etc/raspotify/conf"
echo ""
echo "  2. Restart the service:"
echo "     sudo systemctl restart raspotify"
echo ""
echo "  3. Open Spotify on any device"
echo "     Connect → select 'Dusk' → Play"
echo ""
echo -e "  ${DIM}Requires Spotify Premium${RESET}"
echo ""
