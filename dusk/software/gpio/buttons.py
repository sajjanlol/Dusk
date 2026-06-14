#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════╗
║  DUSK — Physical Button Controller                   ║
║  Controls Spotify playback via GPIO buttons          ║
║                                                      ║
║  The Pill:                                           ║
║    Left end  → Previous track  (GPIO 17)             ║
║    Center    → Play / Pause    (GPIO 27)             ║
║    Right end → Next track      (GPIO 22)             ║
║  Volume:                                             ║
║    Vol+      → Volume up       (GPIO 23)             ║
║    Vol-      → Volume down     (GPIO 24)             ║
╚══════════════════════════════════════════════════════╝
"""

import subprocess
import time
import logging
import sys
import os

# ── Setup logging ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format='[DUSK] %(asctime)s %(levelname)s: %(message)s',
    datefmt='%H:%M:%S'
)
log = logging.getLogger('dusk')

# ── Try to import GPIO ────────────────────────────────────
try:
    from gpiozero import Button
    from signal import pause
    GPIO_AVAILABLE = True
    log.info("GPIO available — running on hardware")
except (ImportError, Exception):
    GPIO_AVAILABLE = False
    log.warning("GPIO not available — running in simulation mode")

# ── GPIO Pin assignments ──────────────────────────────────
PIN_PREV    = 17   # Pill — left end
PIN_PLAY    = 27   # Pill — center
PIN_NEXT    = 22   # Pill — right end
PIN_VOL_UP  = 23   # Volume rocker — top
PIN_VOL_DN  = 24   # Volume rocker — bottom

# ── Debounce time (seconds) ───────────────────────────────
DEBOUNCE    = 0.3

# ── Volume step ──────────────────────────────────────────
VOLUME_STEP = 5     # percent per press
current_volume = 80  # track volume internally

# ── Spotify control via playerctl / librespot ─────────────
def run_cmd(cmd):
    """Run a shell command silently."""
    try:
        result = subprocess.run(
            cmd, shell=True,
            capture_output=True, text=True, timeout=3
        )
        return result.returncode == 0
    except Exception as e:
        log.error(f"Command failed: {cmd} — {e}")
        return False

def spotify_prev():
    log.info("← Previous track")
    run_cmd("playerctl previous 2>/dev/null || "
            "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.raspotify "
            "/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Previous")

def spotify_play_pause():
    log.info("⏸ Play / Pause")
    run_cmd("playerctl play-pause 2>/dev/null || "
            "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.raspotify "
            "/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.PlayPause")

def spotify_next():
    log.info("→ Next track")
    run_cmd("playerctl next 2>/dev/null || "
            "dbus-send --print-reply --dest=org.mpris.MediaPlayer2.raspotify "
            "/org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next")

def volume_up():
    global current_volume
    current_volume = min(100, current_volume + VOLUME_STEP)
    log.info(f"🔊 Volume up → {current_volume}%")
    run_cmd(f"amixer set Master {VOLUME_STEP}%+ 2>/dev/null || "
            f"pactl set-sink-volume @DEFAULT_SINK@ +{VOLUME_STEP}% 2>/dev/null")

def volume_down():
    global current_volume
    current_volume = max(0, current_volume - VOLUME_STEP)
    log.info(f"🔉 Volume down → {current_volume}%")
    run_cmd(f"amixer set Master {VOLUME_STEP}%- 2>/dev/null || "
            f"pactl set-sink-volume @DEFAULT_SINK@ -{VOLUME_STEP}% 2>/dev/null")

# ── Simulation mode (for VM testing) ─────────────────────
class SimButton:
    """Simulated button for VM testing without real GPIO."""
    def __init__(self, pin, hold_time=None, bounce_time=None):
        self.pin = pin
        self.when_pressed = None
        self.when_held = None

def run_simulation():
    """Interactive keyboard simulation for VM testing."""
    log.info("Running in SIMULATION MODE")
    log.info("Keyboard controls:")
    log.info("  [a] = Previous    [s] = Play/Pause    [d] = Next")
    log.info("  [w] = Volume Up   [x] = Volume Down   [q] = Quit")
    log.info("")

    import tty, termios

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)

    try:
        tty.setraw(fd)
        while True:
            ch = sys.stdin.read(1)
            if ch == 'q':
                log.info("Exiting simulation.")
                break
            elif ch == 'a':
                spotify_prev()
            elif ch == 's':
                spotify_play_pause()
            elif ch == 'd':
                spotify_next()
            elif ch == 'w':
                volume_up()
            elif ch == 'x':
                volume_down()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

# ── Hardware mode ─────────────────────────────────────────
def run_hardware():
    """Real GPIO button handling on Pi hardware."""
    log.info("Initialising GPIO buttons...")

    btn_prev   = Button(PIN_PREV,   bounce_time=DEBOUNCE)
    btn_play   = Button(PIN_PLAY,   bounce_time=DEBOUNCE)
    btn_next   = Button(PIN_NEXT,   bounce_time=DEBOUNCE)
    btn_vol_up = Button(PIN_VOL_UP, bounce_time=DEBOUNCE)
    btn_vol_dn = Button(PIN_VOL_DN, bounce_time=DEBOUNCE)

    btn_prev.when_pressed   = spotify_prev
    btn_play.when_pressed   = spotify_play_pause
    btn_next.when_pressed   = spotify_next
    btn_vol_up.when_pressed = volume_up
    btn_vol_dn.when_pressed = volume_down

    log.info("Buttons active — Dusk is ready.")
    log.info(f"  GPIO {PIN_PREV}  → Previous")
    log.info(f"  GPIO {PIN_PLAY}  → Play/Pause")
    log.info(f"  GPIO {PIN_NEXT}  → Next")
    log.info(f"  GPIO {PIN_VOL_UP} → Volume Up")
    log.info(f"  GPIO {PIN_VOL_DN} → Volume Down")

    pause()  # Wait forever, handling button events

# ── Entry point ───────────────────────────────────────────
if __name__ == "__main__":
    log.info("Starting Dusk button controller...")

    if GPIO_AVAILABLE:
        run_hardware()
    else:
        # Check if simulation flag passed
        if "--sim" in sys.argv or not sys.stdin.isatty():
            run_simulation()
        else:
            log.info("Pass --sim flag to run keyboard simulation")
            log.info("Example: python3 buttons.py --sim")
