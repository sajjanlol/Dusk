# 🌆 Dusk

> A standalone, minimalist Spotify-only streaming device — built for digital detox.

---

## What is Dusk?

Dusk is a dedicated music device that does exactly one thing: **plays your Spotify.**

No notifications. No social media. No phone required.

Think of it as a modern iPod — but streaming-native, built for the age of digital detox. It connects to WiFi independently, streams your Spotify playlists, and is controlled entirely through physical buttons. Your phone can stay in another room.

---

## Who is it for?

**The intentional adult listener**
Gym sessions, deep work, morning routines, commutes — all without picking up a screen that wants your attention.

**High school students**
Schools ban phones, not music devices. Dusk has no calls, no messages, no social media, no browser. Categorically not a phone. Teachers cannot object.

**Parents**
Your child gets music. You get peace of mind. Works on Spotify Family Plan — ₹179/month for up to 6 accounts.

---

## The Design

| Spec | Detail |
|---|---|
| Dimensions | 65mm × 110mm × 11mm |
| Display | 2.8" IPS Touchscreen |
| Controls | **The Pill** — single unified front button |
| Volume | Side rocker (right edge) |
| Audio out | 3.5mm headphone jack + Bluetooth |
| Charging | USB-C |
| Connectivity | WiFi + Bluetooth (eSIM in v2) |
| Finish | Matte soft-touch polycarbonate |
| Logo | Laser-etched, flush with surface |

### The Pill

The signature design element. One seamless elongated pill-shaped button at the bottom of the front face.

- **Press left end** → Previous track
- **Press center** → Play / Pause
- **Press right end** → Next track

No labels. No icons. Just muscle memory.

---

## Colorways

| Name | Finish | Status |
|---|---|---|
| Dusk Chalk | Warm off-white matte | Launch |
| Dusk Obsidian | Deep matte black | Drop 02 |
| Dusk Midnight | Deep navy, limited run | Drop 03 |
| Dusk Ember | Dark oxblood | Collectors |

---

## Roadmap

| Version | Focus |
|---|---|
| **v0** | Pi Zero prototype — validate Spotify standalone + button feel |
| **v1** | Consumer enclosure, pill button, touchscreen, Chalk launch |
| **v2** | Built-in eSIM (fully standalone outdoors), speaker, wireless charging |
| **v3** | Custom PCB, proper manufacturing |
| **v4** | VC fundraising, Spotify licensing, premium brand scaling |

---

## Software Stack

| Version | OS | Spotify Method |
|---|---|---|
| v0 / v1 | Raspberry Pi OS Lite | raspotify / librespot |
| v2 | Linux (custom build) | raspotify / librespot + eSIM |
| v3 / v4 | AOSP (custom Android) | Official Spotify APK sideloaded |

> **Note:** Dusk requires Spotify Premium (or Spotify Family Plan).

---

## Hardware (v0 Prototype)

| Component | Part |
|---|---|
| Core | Raspberry Pi Zero 2 W |
| Storage | MicroSD 16GB |
| Audio | pHAT DAC (I2S) |
| Controls | GPIO tactile buttons |
| Power | USB-C power bank / supply |

---

## Repository Structure

```
dusk/
├── src/
│   ├── spotify/        # Spotify auth, session management
│   ├── buttons/        # GPIO button handler + pill button logic
│   ├── audio/          # Audio output, DAC config, volume control
│   ├── display/        # Screen UI — album art, track info
│   └── system/         # Boot config, WiFi setup, kiosk mode
├── config/             # Device config files
├── scripts/            # Install + setup scripts
├── docs/               # Full documentation
└── assets/             # Images, renders, design files
```

---

## Quick Start (v0 Setup)

```bash
# Clone the repo
git clone https://github.com/yourusername/dusk.git
cd dusk

# Run the install script (on Raspberry Pi OS Lite)
chmod +x scripts/install.sh
sudo ./scripts/install.sh

# Configure your Spotify credentials
nano config/dusk.conf

# Start Dusk
sudo systemctl start dusk
```

---

## Market Context

| | Mighty Audio (closest competitor) | Dusk |
|---|---|---|
| Screen | No | Yes |
| Live streaming | Offline only | Yes |
| Phone needed | Always (to sync) | Never |
| Design | Utilitarian clip | Premium limited edition |
| India market | Very limited | Built for India |

---

## License

MIT License — see LICENSE

---

## Built in India

Dusk is designed and built in Chennai, India.
Currently in prototype stage.

*Requires Spotify Premium · Not affiliated with Spotify AB*
