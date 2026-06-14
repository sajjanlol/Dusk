# Dusk — Hardware Setup Guide (v0)

## Components Required

| Component | Part | Source |
|---|---|---|
| Core | Raspberry Pi Zero 2 W | RoboElements / ThinkRobotics |
| Storage | MicroSD 16GB (SanDisk) | Amazon.in |
| Audio DAC | pHAT DAC (I2S) | Robu.in |
| Buttons | Tactile push buttons (10 pack) | Robu.in |
| Prototyping | Half-size breadboard + jumper wires | Robu.in |
| Power | Micro USB 5V 2.5A supply | Amazon.in |
| Setup | Mini HDMI adapter + SD card reader | Amazon.in |

**Total: ~Rs. 3,470**

---

## pHAT DAC Wiring

The pHAT DAC connects directly to the Pi Zero 2 W's 40-pin GPIO header.
It uses the I2S interface — no individual wiring needed, just stack it.

Add to `/boot/config.txt`:
```
dtoverlay=hifiberry-dac
dtparam=audio=off
```

---

## Pill Button Wiring

| Button Zone | GPIO Pin | Function |
|---|---|---|
| Pill LEFT | GPIO 17 | Previous track |
| Pill CENTER | GPIO 27 | Play / Pause |
| Pill RIGHT | GPIO 22 | Next track |
| Vol UP | GPIO 23 | Volume + |
| Vol DOWN | GPIO 24 | Volume - |

All buttons wired with one leg to GPIO pin, other leg to GND.
Internal pull-up resistors enabled in software (PUD_UP).

---

## Boot Config (`/boot/config.txt`)

```ini
# pHAT DAC
dtoverlay=hifiberry-dac
dtparam=audio=off

# HDMI (if using display)
hdmi_force_hotplug=1
hdmi_group=2
hdmi_mode=87
hdmi_cvt=320 240 60 6 0 0 0
```

---

## First Boot Checklist

- [ ] Flash Raspberry Pi OS Lite to MicroSD
- [ ] Enable SSH (`touch /boot/ssh`)
- [ ] Configure WiFi (`/boot/wpa_supplicant.conf`)
- [ ] Boot and SSH in
- [ ] Run `sudo ./scripts/install.sh`
- [ ] Edit `/etc/raspotify/conf` with Spotify credentials
- [ ] Reboot
- [ ] Open Spotify on phone → Connect → select "Dusk"
- [ ] Confirm music plays
