# Dusk — VM Testing Guide

Test the Spotify stack before buying hardware.

## Setup

1. Download VirtualBox — virtualbox.org
2. Download Ubuntu Server 22.04 (.iso) — ubuntu.com/download/server
3. Create VM: Linux, Debian 64-bit, 1024MB RAM, 8GB disk
4. Mount the .iso: Settings → Storage → Empty CD → blue disk icon → select .iso
5. Start VM and complete Ubuntu setup

## Install raspotify

```bash
sudo apt-get update && sudo apt-get upgrade -y
sudo apt-get install -y curl
curl -sL https://dtcooper.github.io/raspotify/install.sh | sh
```

## Configure

```bash
sudo nano /etc/raspotify/conf
```

Add:
```
LIBRESPOT_NAME="Dusk"
LIBRESPOT_BITRATE="320"
LIBRESPOT_USERNAME="your@email.com"
LIBRESPOT_PASSWORD="yourpassword"
```

## Test

```bash
sudo systemctl start raspotify
sudo systemctl status raspotify
```

Open Spotify on your phone → Connect → select "Dusk" → press play.

If it appears and plays: **concept validated.**

Note: Audio won't play through VM speakers (expected).
You are validating Spotify Connect, not audio output.
