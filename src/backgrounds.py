import pygame
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "images"

def load_sprite(path, size, tolerance=40):
    image = pygame.image.load(str(path)).convert_alpha()
    image = pygame.transform.scale(image, size)
    bg = image.get_at((0, 0))
    for x in range(size[0]):
        for y in range(size[1]):
            r, g, b, a = image.get_at((x, y))
            if (abs(r - bg.r) <= tolerance
                    and abs(g - bg.g) <= tolerance
                    and abs(b - bg.b) <= tolerance):
                image.set_at((x, y), (0, 0, 0, 0))
    return image

class Backgrounds:

    def __init__(self, screen_size):
        self.images = {}
        self.screen_size = screen_size

        screens = {
            "menu": "menus.jpg",
            "instructions": "inst.jpg",
            "highscores": "hs.jpg",
            "victory": "vict.jpg",
            "game_over": "gameover.jpg"
        }

        for name, filename in screens.items():
            image = pygame.image.load(
                ASSETS / filename
            ).convert()

            self.images[name] = pygame.transform.scale(
                image, screen_size
            )

    def draw(self, screen, name):
        image = self.images[name]

        screen_size = screen.get_size()

        scaled_image = image
        screen.blit(self.images[name], (0, 0))
