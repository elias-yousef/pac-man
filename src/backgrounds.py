import pygame
from pathlib import Path

ASSETS = Path(__file__).resolve().parent.parent / "images"

class Backgrounds:

    def __init__(self, screen_size):
        self.images = {}
        self.screen_size = screen_size

        screens = {
            "menu": "menu.jpg",
            "instructions": "instruction.jpg",
            "highscores": "highscore.jpg",
            "pause": "pause.jpg",
            "victory": "victory.jpg",
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
