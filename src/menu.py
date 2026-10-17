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


def menu():
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
    menu()















"""
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
