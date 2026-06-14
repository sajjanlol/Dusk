"""
Dusk — Boot Manager
Entry point. Called by dusk.service on startup.
Initialises audio, Spotify, and button handler in sequence.
"""

import time
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from spotify.spotify_controller import SpotifyController
from buttons.button_handler import ButtonHandler
from audio.audio_manager import AudioManager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("/var/log/dusk.log")
    ]
)
logger = logging.getLogger("dusk.boot")


def main():
    logger.info("=" * 40)
    logger.info("  DUSK — Booting")
    logger.info("=" * 40)

    # 1. Audio subsystem
    logger.info("[1/3] Audio...")
    audio = AudioManager()
    audio.set_output_headphone()
    time.sleep(1)

    # 2. Spotify
    logger.info("[2/3] Spotify...")
    spotify = SpotifyController()
    if not spotify.is_running():
        logger.warning("raspotify not running — restarting...")
        spotify.restart_service()
        time.sleep(3)

    if spotify.is_running():
        logger.info("Spotify: READY")
    else:
        logger.error("Spotify failed — check /etc/raspotify/conf credentials")

    # 3. Buttons
    logger.info("[3/3] Buttons...")
    buttons = ButtonHandler(spotify)

    logger.info("Dusk ready. Listening for input.")

    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        logger.info("Shutting down...")
        buttons.cleanup()
        logger.info("Done.")


if __name__ == "__main__":
    main()
