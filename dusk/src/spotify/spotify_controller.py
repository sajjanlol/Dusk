"""
Dusk — Spotify Controller
Controls playback via D-Bus MPRIS interface (raspotify/librespot).
Handles volume, session persistence across reboots.
"""

import subprocess
import logging
import os

logger = logging.getLogger("dusk.spotify")

VOLUME_FILE = "/tmp/dusk_volume"
RASPOTIFY_DBUS = "org.mpris.MediaPlayer2.raspotify"
MPRIS_PATH = "/org/mpris/MediaPlayer2"
MPRIS_PLAYER = "org.mpris.MediaPlayer2.Player"


class SpotifyController:
    def __init__(self):
        self._volume = self._load_volume()
        logger.info(f"SpotifyController ready. Volume: {self._volume}%")

    # Playback
    def toggle_playback(self):
        self._dbus("PlayPause")

    def next_track(self):
        self._dbus("Next")

    def previous_track(self):
        self._dbus("Previous")

    # Volume
    def set_volume(self, delta=0, absolute=None):
        if absolute is not None:
            self._volume = max(0, min(100, absolute))
        else:
            self._volume = max(0, min(100, self._volume + delta))
        self._apply_volume()
        self._save_volume()
        logger.info(f"Volume: {self._volume}%")

    def get_volume(self):
        return self._volume

    def _apply_volume(self):
        try:
            subprocess.run(["amixer", "sset", "PCM", f"{self._volume}%"],
                           capture_output=True, check=True)
        except Exception as e:
            logger.error(f"Volume error: {e}")

    def _save_volume(self):
        with open(VOLUME_FILE, "w") as f:
            f.write(str(self._volume))

    def _load_volume(self):
        try:
            with open(VOLUME_FILE) as f:
                return max(0, min(100, int(f.read().strip())))
        except Exception:
            return 60

    # Service
    def is_running(self):
        r = subprocess.run(["systemctl", "is-active", "raspotify"],
                           capture_output=True, text=True)
        return r.stdout.strip() == "active"

    def restart_service(self):
        subprocess.run(["sudo", "systemctl", "restart", "raspotify"])
        logger.info("raspotify restarted")

    # D-Bus
    def _dbus(self, method):
        try:
            subprocess.run([
                "dbus-send", "--print-reply",
                f"--dest={RASPOTIFY_DBUS}",
                MPRIS_PATH,
                f"{MPRIS_PLAYER}.{method}"
            ], capture_output=True, check=True)
        except subprocess.CalledProcessError:
            logger.warning(f"D-Bus {method} failed — is raspotify running?")
