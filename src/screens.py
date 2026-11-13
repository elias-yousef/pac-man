import pygame
from highscore import HighscoreManager


BG = (246, 243, 238)
PURPLE = (153, 102, 204)
DARK_PURPLE = (76, 54, 91)
PINK = (255, 182, 193)
WHITE = (255, 255, 255)
TEXT = (70, 50, 75)
MUTED = (140, 127, 148)
RED = (210, 80, 100)
GREEN = (100, 160, 120)


def end_screen(screen, final_score, manager, victory=False):

    title_font = pygame.font.SysFont("Corbel", 54, bold=True)
    score_font = pygame.font.SysFont("Corbel", 32, bold=True)
    text_font = pygame.font.SysFont("Corbel", 25)
    small_font = pygame.font.SysFont("Corbel", 18)

    clock = pygame.time.Clock()

    player_name = ""
    message = ""
    saved = False

    while True:
        width, height = screen.get_size()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                return "quit"

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    return "menu"

                if not saved:

                    if event.key == pygame.K_BACKSPACE:
                        player_name = player_name[:-1]

                    elif event.key == pygame.K_RETURN:

                        if player_name.strip():
                            manager.add_score(
                                player_name.strip(),
                                final_score
                            )
                            saved = True
                            message = "Score saved successfully!"

                        else:
                            message = "Please enter your name."

                    elif event.unicode.isalnum() or event.unicode == " ":
                        if len(player_name) < 10:
                            player_name += event.unicode

        screen.fill(BG)

        if victory:
            title = title_font.render(
                "VICTORY!",
                True,
                GREEN
            )
            subtitle = "Congratulations! You completed the game!"
        else:
            title = title_font.render(
                "GAME OVER",
                True,
                RED
            )
            subtitle = "Better luck next time!"

        screen.blit(
            title,
            title.get_rect(center=(width // 2, height // 2 - 140))
        )

        subtitle_surface = text_font.render(
            subtitle,
            True,
            DARK_PURPLE
        )

        screen.blit(
            subtitle_surface,
            subtitle_surface.get_rect(
                center=(width // 2, height // 2 - 80)
            )
        )

        score_surface = score_font.render(
            f"FINAL SCORE: {final_score}",
            True,
            PURPLE
        )

        screen.blit(
            score_surface,
            score_surface.get_rect(
                center=(width // 2, height // 2 - 25)
            )
        )

        name_label = text_font.render(
            "Enter your name:",
            True,
            TEXT
        )

        screen.blit(
            name_label,
            name_label.get_rect(
                center=(width // 2, height // 2 + 35)
            )
        )

        input_box = pygame.Rect(
            width // 2 - 140,
            height // 2 + 65,
            280,
            45
        )

        pygame.draw.rect(
            screen,
            WHITE,
            input_box,
            border_radius=8
        )

        pygame.draw.rect(
            screen,
            PURPLE,
            input_box,
            2,
            border_radius=8
        )

        name_surface = text_font.render(
            player_name,
            True,
            TEXT
        )

        screen.blit(
            name_surface,
            name_surface.get_rect(center=input_box.center)
        )

        if not saved:
            hint = small_font.render(
                "Press ENTER to save your score",
                True,
                MUTED
            )
        else:
            hint = small_font.render(
                "Press ESC to return to the menu",
                True,
                MUTED
            )

        screen.blit(
            hint,
            hint.get_rect(center=(width // 2, height // 2 + 135))
        )

        if message:
            message_surface = small_font.render(
                message,
                True,
                GREEN if saved else RED
            )

            screen.blit(
                message_surface,
                message_surface.get_rect(
                    center=(width // 2, height // 2 + 175)
                )
            )

        pygame.display.flip()
        clock.tick(60)


def game_over_screen(screen, final_score, manager):
    return end_screen(screen, final_score, manager, victory=False)


def victory_screen(screen, final_score, manager):
    return end_screen(screen, final_score, manager, victory=True)
