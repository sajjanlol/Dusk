"""
Dusk — Button Handler
GPIO input for the pill button and volume rocker.

The Pill (single unified front button):
  Left zone  -> Previous track
  Center     -> Play / Pause
  Right zone -> Next track

Volume Rocker (right edge):
  Top    -> Volume Up
  Bottom -> Volume Down
"""

import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dusk.buttons")

# GPIO Pin assignments (BCM numbering)
PIN_PILL_LEFT   = 17
PIN_PILL_CENTER = 27
PIN_PILL_RIGHT  = 22
PIN_VOL_UP      = 23
PIN_VOL_DOWN    = 24

DEBOUNCE_MS = 200
VOLUME_STEP = 5


class ButtonHandler:
    def __init__(self, spotify):
        self.spotify = spotify
        self._setup_gpio()
        logger.info("Button handler initialised")

    def _setup_gpio(self):
        try:
            import RPi.GPIO as GPIO
            self.GPIO = GPIO
            GPIO.setmode(GPIO.BCM)
            GPIO.setwarnings(False)
            pins = [PIN_PILL_LEFT, PIN_PILL_CENTER, PIN_PILL_RIGHT,
                    PIN_VOL_UP, PIN_VOL_DOWN]
            for pin in pins:
                GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.add_event_detect(PIN_PILL_LEFT,   GPIO.FALLING,
                                  callback=self._prev_track,  bouncetime=DEBOUNCE_MS)
            GPIO.add_event_detect(PIN_PILL_CENTER, GPIO.FALLING,
                                  callback=self._play_pause,  bouncetime=DEBOUNCE_MS)
            GPIO.add_event_detect(PIN_PILL_RIGHT,  GPIO.FALLING,
                                  callback=self._next_track,  bouncetime=DEBOUNCE_MS)
            GPIO.add_event_detect(PIN_VOL_UP,      GPIO.FALLING,
                                  callback=self._volume_up,   bouncetime=DEBOUNCE_MS)
            GPIO.add_event_detect(PIN_VOL_DOWN,    GPIO.FALLING,
                                  callback=self._volume_down, bouncetime=DEBOUNCE_MS)
        except ImportError:
            logger.warning("RPi.GPIO not available — running in simulation mode")

    def _prev_track(self, channel):
        logger.info("Pill LEFT -> Previous track")
        self.spotify.previous_track()

    def _play_pause(self, channel):
        logger.info("Pill CENTER -> Play/Pause")
        self.spotify.toggle_playback()

    def _next_track(self, channel):
        logger.info("Pill RIGHT -> Next track")
        self.spotify.next_track()

    def _volume_up(self, channel):
        logger.info(f"Vol UP +{VOLUME_STEP}")
        self.spotify.set_volume(delta=+VOLUME_STEP)

    def _volume_down(self, channel):
        logger.info(f"Vol DOWN -{VOLUME_STEP}")
        self.spotify.set_volume(delta=-VOLUME_STEP)

    def cleanup(self):
        try:
            self.GPIO.cleanup()
        except Exception:
            pass
        logger.info("GPIO cleaned up")
