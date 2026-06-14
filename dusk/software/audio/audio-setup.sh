#!/bin/bash
# ============================================================
#  DUSK — Audio Setup Script
#  Configures pHAT DAC (I2S) on Raspberry Pi Zero 2 W
# ============================================================

set -e

GREEN='\033[0;32m'
RESET='\033[0m'
log() { echo -e "${GREEN}[DUSK AUDIO]${RESET} $1"; }

log "Configuring pHAT DAC (I2S audio)..."

# ── Check if running on Raspberry Pi ──────────────────────
if [ -f /boot/config.txt ]; then
    BOOT_CONFIG="/boot/config.txt"
elif [ -f /boot/firmware/config.txt ]; then
    BOOT_CONFIG="/boot/firmware/config.txt"
else
    log "WARNING: Not on Raspberry Pi — skipping hardware audio config"
    log "On VM, audio will use default system output"
    exit 0
fi

# ── Disable onboard audio (poor quality) ─────────────────
log "Disabling onboard audio..."
sed -i 's/dtparam=audio=on/dtparam=audio=off/' $BOOT_CONFIG 2>/dev/null || true

# ── Enable I2S for pHAT DAC ──────────────────────────────
log "Enabling I2S overlay for pHAT DAC..."
grep -qxF 'dtoverlay=hifiberry-dac' $BOOT_CONFIG || \
    echo 'dtoverlay=hifiberry-dac' >> $BOOT_CONFIG

# ── Set ALSA default card ─────────────────────────────────
log "Setting pHAT DAC as default ALSA device..."
cat > /etc/asound.conf << 'ALSA'
pcm.!default {
    type hw
    card 0
}
ctl.!default {
    type hw
    card 0
}
ALSA

# ── Set default volume ────────────────────────────────────
log "Setting initial volume to 85%..."
sleep 2
amixer set Master 85% 2>/dev/null || true

# ── Test audio config ─────────────────────────────────────
log "Audio setup complete."
log "Reboot required for I2S changes to take effect."
log "After reboot, test with: speaker-test -t sine -f 440"
