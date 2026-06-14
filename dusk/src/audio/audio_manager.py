"""
Dusk — Audio Manager
Configures pHAT DAC (I2S / HifiBerry), ALSA output, Bluetooth.
"""

import subprocess
import logging

logger = logging.getLogger("dusk.audio")

ALSA_CARD = "sndrpihifiberry"


class AudioManager:
    def __init__(self):
        self._verify_dac()

    def _verify_dac(self):
        r = subprocess.run(["aplay", "-l"], capture_output=True, text=True)
        if "hifiberry" in r.stdout.lower():
            logger.info("pHAT DAC detected")
        else:
            logger.warning("pHAT DAC not detected. Check /boot/config.txt — dtoverlay=hifiberry-dac")

    def set_output_headphone(self):
        subprocess.run(["amixer", "-c", "0", "cset", "numid=3", "1"],
                       capture_output=True)
        logger.info("Output: headphone jack")

    def set_output_bluetooth(self):
        logger.info("Output: Bluetooth (via PulseAudio)")

    def write_alsa_config(self):
        conf = f"""
pcm.!default {{
    type hw
    card {ALSA_CARD}
}}
ctl.!default {{
    type hw
    card {ALSA_CARD}
}}
"""
        with open("/etc/asound.conf", "w") as f:
            f.write(conf)
        logger.info("ALSA config written")
