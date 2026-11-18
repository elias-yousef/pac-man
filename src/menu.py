import pygame
import sys
from pathlib import Path
from instruction import display_instructions
from display_highscore import display_highscores
from highscore import HighscoreManager
from backgrounds import Backgrounds
from Charcacters import Game

pygame.init()

WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode(
    (WIDTH, HEIGHT),
    pygame.RESIZABLE
)

pygame.display.set_caption("Pac-Man")

# Pixel font
font = pygame.font.SysFont("monospace", 22, bold=True)


class PixelButton:

    def __init__(self, text, rect, colors, font):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.colors = colors
        self.font = font

    def draw(self, surface):

        mouse = pygame.mouse.get_pos()
        hovered = self.rect.collidepoint(mouse)

        color = self.colors["hover"] if hovered else self.colors["normal"]

        # Pixel shadow
        shadow = self.rect.move(5, 5)
        pygame.draw.rect(
            surface,
            self.colors["shadow"],
            shadow
        )

        # Button body
        pygame.draw.rect(
            surface,
            color,
            self.rect
        )

        # Pixel border
        pygame.draw.rect(
            surface,
            self.colors["border"],
            self.rect,
            4
        )

        # Inner highlight
        inner = self.rect.inflate(-10, -10)

        pygame.draw.rect(
            surface,
            self.colors["highlight"],
            inner,
            2
        )

        # Text
        text_surface = self.font.render(
            self.text,
            False,
            self.colors["text"]
        )

        text_rect = text_surface.get_rect(
            center=self.rect.center
        )

        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):

        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


# Temporary palette - replace with your image colors later
BUTTON_COLORS = {
    "play": {
        "normal": (180, 120, 140),
        "hover": (220, 155, 175),
        "border": (75, 45, 60),
        "shadow": (45, 30, 40),
        "highlight": (235, 190, 200),
        "text": (255, 245, 230)
    },

    "score": {
        "normal": (145, 125, 175),
        "hover": (185, 160, 215),
        "border": (60, 45, 85),
        "shadow": (35, 25, 55),
        "highlight": (210, 195, 235),
        "text": (255, 245, 230)
    },

    "inst": {
        "normal": (115, 145, 175),
        "hover": (150, 185, 220),
        "border": (40, 65, 90),
        "shadow": (25, 40, 55),
        "highlight": (190, 215, 235),
        "text": (255, 245, 230)
    },

    "quit": {
        "normal": (125, 155, 125),
        "hover": (165, 195, 155),
        "border": (45, 75, 45),
        "shadow": (25, 45, 25),
        "highlight": (195, 220, 180),
        "text": (255, 245, 230)
    }
}


def menu(config):

    global screen, WIDTH, HEIGHT

    score_file = Path(__file__).resolve().parent / "score.json"
    config_file = Path(__file__).resolve().parent / "config.json"

    manager = HighscoreManager(str(score_file))

    clock = pygame.time.Clock()
    running = True

    backgrounds = Backgrounds(screen.get_size())

    while running:

        WIDTH, HEIGHT = screen.get_size()

        # Button dimensions and positions
        button_width = 300
        button_height = 55

        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        startgame = PixelButton(
            "START GAME",
            (center_x - 150, center_y - 110, button_width, button_height),
            BUTTON_COLORS["play"],
            font
        )

        hscore = PixelButton(
            "HIGH SCORES",
            (center_x - 150, center_y - 40, button_width, button_height),
            BUTTON_COLORS["score"],
            font
        )

        inst = PixelButton(
            "INSTRUCTIONS",
            (center_x - 150, center_y + 30, button_width, button_height),
            BUTTON_COLORS["inst"],
            font
        )

        ext = PixelButton(
            "EXIT",
            (center_x - 150, center_y + 100, button_width, button_height),
            BUTTON_COLORS["quit"],
            font
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                backgrounds = Backgrounds(screen.get_size())
                WIDTH, HEIGHT = screen.get_size()
                WIDTH, HEIGHT = event.size

                screen = pygame.display.set_mode(
                    (WIDTH, HEIGHT),
                    pygame.RESIZABLE
                )

                backgrounds = Backgrounds((WIDTH, HEIGHT))
            elif startgame.is_clicked(event):
                game = Game(config=config)
                result = game.run()

                screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                backgrounds = Backgrounds(screen.get_size())

                if result == "quit":
                    running = False
    
            elif hscore.is_clicked(event):

                manager.load_scores()
                scores = manager.get_scores()

                display_highscores(screen, scores)

            elif inst.is_clicked(event):

                display_instructions(screen)

            elif ext.is_clicked(event):

                running = False

        # Draw background
        backgrounds.draw(screen, "menu")

        # Draw buttons
        startgame.draw(screen)
        hscore.draw(screen)
        inst.draw(screen)
        ext.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    import json
    config_file = Path(__file__).resolve().parent / "config.json"
    with open(config_file) as f:
        config = json.load(f)
    menu(config)


"""
    import pygame
import sys
from pathlib import Path
from instruction import display_instructions
from display_highscore import display_highscores
from highscore import HighscoreManager
from backgrounds import backgrounds

pygame.init()

#Bg
BG = (246, 243, 238)

#buttons colors
PLAY = (255, 182, 193)
SCORE = (196, 164, 232)
INST = (176, 196, 222)
QUIT = (180, 220, 190)

#hovercolors
PLAY_HOVER = (255, 105, 180)
SCORE_HOVER = (153, 102, 204)
INST_HOVER = (100, 149, 237)
QUIT_HOVER = (100, 180, 130)

TEXT = (70, 50, 75)
WHITE = (255, 255, 255)


width = 800
height = 600

screen = pygame.display.set_mode(
    (width, height),
    pygame.RESIZABLE
)

pygame.display.set_caption("Pac-Man")
font = pygame.font.SysFont("Corbel", 26, bold=True)


def menu():
    # are we allowed to use global?????
    global screen, width, height

   
    score_file = Path(__file__).resolve().parent / "hs.json"
    manager = HighscoreManager(str(score_file))

    clock = pygame.time.Clock()
    running = True

    while running:

        width, height = screen.get_size()

        startgame = pygame.Rect(0, 0, 300, 50)
        hscore = pygame.Rect(0, 0, 300, 50)
        inst = pygame.Rect(0, 0, 300, 50)
        ext = pygame.Rect(0, 0, 300, 50)

        startgame.center = (width // 2, height // 2 - 105)
        hscore.center = (width // 2, height // 2 - 35)
        inst.center = (width // 2, height // 2 + 35)
        ext.center = (width // 2, height // 2 + 106)

        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                width, height = event.size

                screen = pygame.display.set_mode(
                    (width, height),
                    pygame.RESIZABLE
                )

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    # Start Game
                    if startgame.collidepoint(event.pos):
                        from pac_man import main as run_game
                        config_file = Path(__file__).resolve().parent / "config.json"
                        result = run_game(str(config_file))

                        if result == "quit":
                            running = False

                    
                    elif hscore.collidepoint(event.pos):
                        manager.load_scores()
                        scores = manager.get_scores()

                        display_highscores(screen, scores)

                    # Show Instructions
                    elif inst.collidepoint(event.pos):
                        display_instructions(screen)

                    
                    elif ext.collidepoint(event.pos):
                        running = False

        #here to draw the menu
        screen.fill(BG)

        pygame.draw.rect(
            screen,
            PLAY_HOVER if startgame.collidepoint(mouse) else PLAY,
            startgame
        )

        pygame.draw.rect(
            screen,
            SCORE_HOVER if hscore.collidepoint(mouse) else SCORE,
            hscore
        )

        pygame.draw.rect(
            screen,
            INST_HOVER if inst.collidepoint(mouse) else INST,
            inst
        )

        pygame.draw.rect(
            screen,
            QUIT_HOVER if ext.collidepoint(mouse) else QUIT,
            ext
        )

        #the button text
        s_text = font.render("START GAME", True, WHITE)
        h_text = font.render("SHOW HIGHSCORE", True, WHITE)
        in_text = font.render("INSTRUCTIONS", True, WHITE)
        ex_text = font.render("EXIT", True, WHITE)

        screen.blit(
            s_text,
            s_text.get_rect(center=startgame.center)
        )

        screen.blit(
            h_text,
            h_text.get_rect(center=hscore.center)
        )

        screen.blit(
            in_text,
            in_text.get_rect(center=inst.center)
        )

        screen.blit(
            ex_text,
            ex_text.get_rect(center=ext.center)
        )

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    menu()




"""
