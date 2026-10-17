#from pac-man import main
from instruction import display_instructions
#from highscore import HighscoreManager
import pygame
import sys
#import Charcacters
#game: "Charcacters"

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

def display_highscores(screen, highscores):
    title_font = pygame.font.SysFont("Corbel", 42, bold=True)
    text_font = pygame.font.SysFont("Corbel", 28)
    hint_font = pygame.font.SysFont("Corbel", 20)

    BG = (246, 243, 238)
    TITLE = (153, 102, 204)
    TEXT = (70, 50, 75)
    MUTED = (130, 120, 140)

    clock = pygame.time.Clock()
    scores = highscores.get_scores()
    waiting = True

    while waiting:
        width, height = screen.get_size()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type in (pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                waiting = False

        screen.fill(BG)

        title = title_font.render("HIGH SCORES", True, TITLE)
        screen.blit(
            title,
            title.get_rect(center=(width // 2, 70))
        )

        if not scores:
            message = text_font.render(
                "No scores yet. Start playing!",
                True,
                TEXT
            )
            screen.blit(
                message,
                message.get_rect(center=(width // 2, height // 2))
            )

        else:
            for index, entry in enumerate(scores):
                line = text_font.render(
                    f"{index + 1}.  {entry['name']}  -  "
                    f"{entry['score']}",
                    True,
                    TEXT
                )

                screen.blit(
                    line,
                    line.get_rect(
                        center=(width // 2, 140 + index * 38)
                    )
                )

        hint = hint_font.render(
            "Press any key or click to return",
            True,
            MUTED
        )
        screen.blit(
            hint,
            hint.get_rect(center=(width // 2, height - 30))
        )

        pygame.display.flip()
        clock.tick(40)

def menu():
    global screen, width, height
    #highscores = HighscoreManager("hs.json")
    #highscores.load_scores()

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
                    
                    #if hscore.collidepoint(event.pos):
                     #   display_highscores(screen, highscores)
                    if inst.collidepoint(event.pos):
                        display_instructions(screen)
                    
                    if ext.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

        pygame.display.update()


menu()
'''
import pygame
import sys
#import Charcacters
#game: "Charcacters"


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
WHITE = (255,255,255)
LIGHT = (170,170,170)
DARK = (100,100,100)
#BG = (60,25,60)
width = 200
height = 200
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("pac-man menu!")
font = pygame.font.SysFont("Corbel", 20)

def window():
    #pygame.init()
    #width = game.GAME_WIDTH
    #height = game.GAME_HEIGHT
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill((40, 40, 40))
        text = font.render("Game Started!", True, WHITE)
        screen.blit(text, (350, 350))

        pygame.display.flip()
def menu():
    while True:
        screen.fill(BG)
        mouse = pygame.mouse.get_pos()
        startgame = pygame.Rect(0, 0, 200, 40)
        hscore = pygame.Rect(0, 0, 200, 40)
        inst = pygame.Rect(0, 0, 200, 40)
        ext = pygame.Rect(0, 0, 200, 40)

        s_text = font.render("START GAME", True, WHITE)
        h_text = font.render("SHOW HIGHSCORE",True, WHITE)
        in_text = font.render("INSTRUCTIONS", True, WHITE)
        ex_text= font.render("EXIT", True, WHITE)

        pygame.draw.rect(screen, SCORE if startgame.collidepoint(mouse) else DARK, startgame)
        pygame.draw.rect(screen, SCORE if hscore.collidepoint(mouse) else DARK, hscore)

        pygame.draw.rect(screen, LIGHT if inst.collidepoint(mouse) else DARK, inst)
        pygame.draw.rect(screen, LIGHT if ext.collidepoint(mouse) else DARK, ext)

        pygame.draw.rect(screen, PLAY, startgame)
        pygame.draw.rect(screen, SCORE, hscore)
        pygame.draw.rect(screen, INST, inst)
        pygame.draw.rect(screen, QUIT, ext)
        startgame.center = (width // 2, height // 2 - 90)
        hscore.center = (width // 2, height // 2 - 30)
        inst.center = (width // 2, height // 2 + 30)
        ext.center = (width // 2, height // 2 + 90)
        screen.blit(s_text, s_text.get_rect(center=startgame.center))
        screen.blit(h_text, h_text.get_rect(center=hscore.center))
        screen.blit(in_text, in_text.get_rect(center=inst.center))
        screen.blit(ex_text, ex_text.get_rect(center=ext.center))

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:

                if startgame.collidepoint(mouse):
                    window()

                if ext.collidepoint(mouse):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
menu()



'''
