#!/bin/bash
# ============================================================
#  DUSK — Autostart Script
#  Ensures Spotify (raspotify) starts automatically on boot
#  and restarts if it crashes
# ============================================================

set -e

GREEN='\033[0;32m'
RESET='\033[0m'
log() { echo -e "${GREEN}[DUSK BOOT]${RESET} $1"; }

log "Configuring Dusk autostart on boot..."

# ── Enable raspotify on boot ──────────────────────────────
systemctl enable raspotify
log "raspotify enabled on boot"

# ── Create watchdog service ───────────────────────────────
# Restarts raspotify if it dies unexpectedly
cat > /etc/systemd/system/dusk-watchdog.service << 'SERVICE'
[Unit]
Description=Dusk Spotify Watchdog
After=network-online.target raspotify.service
Wants=network-online.target

[Service]
Type=simple
ExecStart=/bin/bash /usr/local/bin/dusk-watchdog.sh
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICE

# ── Watchdog script ───────────────────────────────────────
cat > /usr/local/bin/dusk-watchdog.sh << 'WATCHDOG'
#!/bin/bash
# Dusk watchdog — keeps raspotify alive
while true; do
    if ! systemctl is-active --quiet raspotify; then
        echo "[DUSK WATCHDOG] raspotify down — restarting..."
        systemctl start raspotify
    fi
    sleep 15
done
WATCHDOG

chmod +x /usr/local/bin/dusk-watchdog.sh

# ── Enable watchdog ───────────────────────────────────────
systemctl daemon-reload
systemctl enable dusk-watchdog.service
systemctl start dusk-watchdog.service

log "Watchdog service enabled"

# ── Disable unnecessary services for performance ──────────
log "Optimising for performance (disabling unused services)..."
systemctl disable bluetooth 2>/dev/null || true
systemctl disable triggerhappy 2>/dev/null || true
systemctl disable avahi-daemon 2>/dev/null || true

log "Autostart configuration complete."
log "Dusk will now start automatically on every boot."
