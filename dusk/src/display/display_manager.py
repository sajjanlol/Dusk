"""
Dusk — Display Manager
Drives the 2.8" IPS touchscreen.
Shows album art, track name, artist, progress bar, volume indicator.
Uses pygame for rendering on framebuffer.
"""

import logging
import time

logger = logging.getLogger("dusk.display")

# Screen resolution for 2.8" IPS
SCREEN_W = 320
SCREEN_H = 240

# Spotify green
COLOR_GREEN  = (29, 185, 84)
COLOR_BG     = (10, 10, 10)
COLOR_WHITE  = (255, 255, 255)
COLOR_MUTED  = (100, 100, 100)
COLOR_PILL   = (30, 30, 25)


class DisplayManager:
    def __init__(self):
        try:
            import pygame
            self.pygame = pygame
            os = __import__("os")
            os.environ["SDL_FBDEV"] = "/dev/fb0"
            os.environ["SDL_VIDEODRIVER"] = "fbcon"
            pygame.init()
            self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
            pygame.display.set_caption("Dusk")
            pygame.mouse.set_visible(False)
            self.font_large  = pygame.font.SysFont("sans", 18, bold=True)
            self.font_medium = pygame.font.SysFont("sans", 14)
            self.font_small  = pygame.font.SysFont("sans", 11)
            logger.info(f"Display ready: {SCREEN_W}x{SCREEN_H}")
        except ImportError:
            logger.warning("pygame not available — display disabled")
            self.pygame = None

    def render(self, track_name="", artist="", progress=0.0,
               volume=60, album_art=None):
        if not self.pygame:
            return

        pygame = self.pygame
        screen = self.screen
        screen.fill(COLOR_BG)

        # Album art (placeholder square if no art)
        art_size = 140
        art_x, art_y = (SCREEN_W - art_size) // 2, 12
        if album_art:
            art = pygame.transform.scale(album_art, (art_size, art_size))
            screen.blit(art, (art_x, art_y))
        else:
            pygame.draw.rect(screen, (20, 30, 20),
                             (art_x, art_y, art_size, art_size), border_radius=6)
            note = self.font_large.render("♪", True, COLOR_GREEN)
            screen.blit(note, (art_x + art_size//2 - 10, art_y + art_size//2 - 12))

        # Track name
        name_surf = self.font_large.render(
            track_name[:28] if len(track_name) > 28 else track_name,
            True, COLOR_WHITE)
        screen.blit(name_surf, ((SCREEN_W - name_surf.get_width()) // 2, 162))

        # Artist
        artist_surf = self.font_medium.render(artist, True, COLOR_MUTED)
        screen.blit(artist_surf, ((SCREEN_W - artist_surf.get_width()) // 2, 182))

        # Progress bar
        bar_x, bar_y, bar_w, bar_h = 20, 202, SCREEN_W - 40, 3
        pygame.draw.rect(screen, (40, 40, 40), (bar_x, bar_y, bar_w, bar_h),
                         border_radius=2)
        pygame.draw.rect(screen, COLOR_GREEN,
                         (bar_x, bar_y, int(bar_w * progress), bar_h),
                         border_radius=2)

        # Volume dot
        vol_x = int(20 + (SCREEN_W - 60) * volume / 100)
        pygame.draw.circle(screen, COLOR_MUTED, (SCREEN_W - 30, 207), 3)
        vol_surf = self.font_small.render(f"{volume}%", True, COLOR_MUTED)
        screen.blit(vol_surf, (SCREEN_W - 40, 212))

        pygame.display.flip()

    def show_startup(self):
        if not self.pygame:
            return
        self.screen.fill(COLOR_BG)
        title = self.font_large.render("DUSK", True, COLOR_GREEN)
        sub   = self.font_small.render("connecting to spotify...", True, COLOR_MUTED)
        self.screen.blit(title, ((SCREEN_W - title.get_width()) // 2, 100))
        self.screen.blit(sub,   ((SCREEN_W - sub.get_width())   // 2, 130))
        self.pygame.display.flip()

    def cleanup(self):
        if self.pygame:
            self.pygame.quit()
