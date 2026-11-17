

import pygame
from pathlib import Path
"""
an example of how i could use the HUD inisde the game to represent the data bar or whatever its name :)
   

   while running:
    window.fill((0, 0, 0))

    draw_maze(window, maze_arr, TILE_SIZE, loaded_images)

    # Handle events
    # Update game state

    window.blit(pacman, (PLAYER_X, PLAYER_Y))

    draw_hud(
        window,
        score,
        lives,
        level,
        remaining_time
    )

    pygame.display.update()
    clock.tick(60)
"""
   
BG_COLOR = (255, 242, 204)
TEXT_COLOR = (76, 52, 100)
CARD_COLOR = (255, 250, 240)
BORDER_COLOR = (190, 160, 220)
class HUD:
    def __init__(self, screen_w: int) -> None:
        self.height =60
        self.width = screen_w
        self.cuurent_score=0
        self.lives=3
        self.time=120
        self.level=1
        self.BG_COLOR = (190, 160, 220)
        self.TEXT_COLOR = (255, 242, 204)
        self.CARD_COLOR = (255, 250, 240)
        self.BORDER_COLOR = (76, 52, 100)


        pygame.font.init()
        self.font= pygame.font.SysFont("arial", 17, bold=True)#("Comic Sans MS", 24, bold=True)
        image_path = Path(__file__).resolve().parent / "pacman.png"

        self.ghost = pygame.image.load(image_path).convert_alpha()
        self.ghost = pygame.transform.scale(self.ghost, (16, 16))


    def draw_BG(self, screen):
        width = screen.get_width()
        pygame.draw.rect(
            screen,
            self.BG_COLOR,
            (0, 0, width, self.height)
        )
        pygame.draw.rect(
            screen,
            self.BORDER_COLOR,
            (0, 0, width, self.height),
            4
        )
    def draw_text(self, screen, text, x, y):
        text_surface = self.font.render(text, True, self.TEXT_COLOR)
        screen.blit(text_surface, (x, y))
    
    def draw_timer(self, screen, seconds):
        self.draw_text(screen, f"TIME: {seconds}", 15, 17)
    
    def draw_lives(self, screen, lives):
        screen.blit(self.ghost, (320, 18))
        self.draw_text(screen, f"LIVES: {lives} ", 260, 17)
        #width = screen.get_width()

        #ghost_x = width - 190

        #screen.blit(self.ghost, (ghost_x, 18))
        #self.draw_text(screen, f"LIVES:{lives}", ghost_x + 22, 17)
    def draw_level(self, screen, level):
        self.draw_text(screen, f"LEVEL: {level}", 390, 17)
        #text = f"LEVEL: {level}"
        #text_surface = self.font.render(text, True, self.TEXT_COLOR)

        #x = screen.get_width() - text_surface.get_width() - 15
        #y = 17

        #screen.blit(text_surface, (x, y))
    
    def draw_score(self, screen, score):
        self.draw_text(screen, f"SCORE: {score}", 110, 17)
    
    def draw(self, screen, score, lives, level, remaining_time):
        self.draw_BG(screen)
        self.draw_timer(screen, remaining_time)
        self.draw_score(screen, score)
        self.draw_lives(screen, lives)
        self.draw_level(screen, level)

"""
import pygame
import sys
from pathlib import Path

from instruction import display_instructions
from display_highscore import display_highscores
from highscore import HighscoreManager


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


def hud():
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

                        result = run_game()

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
    hud()















from pac_man import main
from instruction import display_instructions
import pygame
import sys
from display_highscore import display_highscores
pygame.init()

# Background
#BG = (255, 240, 245)       # Soft pink
BG = (246, 243, 238)

# Buttons
PLAY = (255, 182, 193)     # Light pink
SCORE = (196, 164, 232)    # Lavender
INST = (176, 196, 222)     # Powder blue
QUIT = (180, 220, 190)     # Pastel green

# Hover colors
PLAY_HOVER = (255, 105, 180)
SCORE_HOVER = (153, 102, 204)
INST_HOVER = (100, 149, 237)
QUIT_HOVER = (100, 180, 130)

# Text
TEXT = (70, 50, 75)
WHITE = (255, 255, 255)
LIGHT = (170, 170, 170)
DARK = (100, 100, 100)

width = 800
height = 600

screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("pac-man menu!")
font = pygame.font.SysFont("Corbel", 26, bold=True)


def window():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((40, 40, 40))

        text = font.render("Game Started!", True, WHITE)
        screen.blit(text, text.get_rect(center=(width // 2, height // 2)))

        pygame.display.flip()

def load_test_scores(filename="score.json"):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

def menu():
    global screen, width, height
    
    #the real strucutre for receiving data from manager
    #highscores = HighscoreManager("hs.json")
    #manager = HighscoreManager("hs.json")
    #scores = manager.get_scores()
    
    #for testing only, taking data from an existed file i make to test the screen lol
    scores= load_test_scores()
    
    
    while True:
        screen.fill(BG)
        mouse = pygame.mouse.get_pos()

        # Create buttons
        startgame = pygame.Rect(0, 0, 300, 50)
        hscore = pygame.Rect(0, 0, 300, 50)
        inst = pygame.Rect(0, 0, 300, 50)
        ext = pygame.Rect(0, 0, 300, 50)

        # Center buttons
        startgame.center = (width // 2, height // 2 - 105)
        hscore.center = (width // 2, height // 2 - 35)
        inst.center = (width // 2, height // 2 + 35)
        ext.center = (width // 2, height // 2 + 106)

        # Button text
        s_text = font.render("START GAME", True, WHITE)
        h_text = font.render("SHOW HIGHSCORE", True, WHITE)
        in_text = font.render("INSTRUCTIONS", True, WHITE)
        ex_text = font.render("EXIT", True, WHITE)

        # Draw buttons with hover colors
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

        # Center text inside buttons
        screen.blit(s_text, s_text.get_rect(center=startgame.center))
        screen.blit(h_text, h_text.get_rect(center=hscore.center))
        screen.blit(in_text, in_text.get_rect(center=inst.center))
        screen.blit(ex_text, ex_text.get_rect(center=ext.center))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.VIDEORESIZE:
                width, height = event.size
                screen = pygame.display.set_mode(
                    (width, height), pygame.RESIZABLE
                )

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:

                    #if startgame.collidepoint(event.pos):
                   #     main()
                    
                    if hscore.collidepoint(event.pos):
                        display_highscores(screen, scores)
                    if inst.collidepoint(event.pos):
                        display_instructions(screen)
                    
                    if ext.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()


menu()
"""
