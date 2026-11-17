import pygame
import sys
from backgrounds import Backgrounds


def display_highscores(screen, scores):

    # Fonts
    title_font = pygame.font.SysFont("monospace", 34, bold=True)
    text_font = pygame.font.SysFont("monospace", 17)
    score_font = pygame.font.SysFont("monospace", 17, bold=True)
    hint_font = pygame.font.SysFont("monospace", 12)
    rank_font = pygame.font.SysFont("monospace", 18, bold=True)

    # Temporary theme colors
    PURPLE = (153, 102, 204)
    DARK_PURPLE = (76, 54, 91)
    TEXT = (70, 50, 75)
    WHITE = (255, 255, 255)
    SHADOW = (45, 30, 55)
    HIGHLIGHT = (220, 195, 240)

    GOLD = (240, 195, 70)
    SILVER = (185, 195, 210)
    BRONZE = (195, 130, 85)

    clock = pygame.time.Clock()
    waiting = True

    backgrounds = Backgrounds(screen.get_size())

    while waiting:

        width, height = screen.get_size()

        # Back button
        back_button = pygame.Rect(
            width // 2 - 85,
            height - 65,
            170,
            42
        )

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if back_button.collidepoint(event.pos):
                        waiting = False

        # Background
        backgrounds.draw(screen, "highscores")

        # Main panel
        panel_width = min(520, width - 40)
        panel_height = min(450, height - 160)

        panel = pygame.Rect(
            (width - panel_width) // 2,
            105,
            panel_width,
            panel_height
        )

        # Pixel shadow
        pygame.draw.rect(
            screen,
            SHADOW,
            panel.move(7, 7)
        )

        # Panel body
        pygame.draw.rect(
            screen,
            DARK_PURPLE,
            panel
        )

        # Pixel border
        pygame.draw.rect(
            screen,
            HIGHLIGHT,
            panel,
            3
        )

        inner_panel = panel.inflate(-10, -10)

        pygame.draw.rect(
            screen,
            PURPLE,
            inner_panel,
            2
        )

        # Title
        title = title_font.render(
            "HIGH SCORES",
            False,
            WHITE
        )

        screen.blit(
            title,
            title.get_rect(
                center=(width // 2, 55)
            )
        )

        # Column headings
        heading_y = panel.top + 22

        rank_heading = hint_font.render(
            "RANK",
            False,
            HIGHLIGHT
        )

        name_heading = hint_font.render(
            "PLAYER",
            False,
            HIGHLIGHT
        )

        score_heading = hint_font.render(
            "SCORE",
            False,
            HIGHLIGHT
        )

        screen.blit(
            rank_heading,
            (panel.left + 22, heading_y)
        )

        screen.blit(
            name_heading,
            (panel.left + 100, heading_y)
        )

        screen.blit(
            score_heading,
            score_heading.get_rect(
                midright=(panel.right - 22, heading_y + 8)
            )
        )

        # No scores
        if not scores:

            message = text_font.render(
                "NO SCORES YET!",
                False,
                WHITE
            )

            screen.blit(
                message,
                message.get_rect(center=panel.center)
            )

            sub_message = hint_font.render(
                "START PLAYING TO ENTER THE RANKING",
                False,
                HIGHLIGHT
            )

            screen.blit(
                sub_message,
                sub_message.get_rect(
                    center=(panel.centerx, panel.centery + 30)
                )
            )

        else:

            row_height = 37
            row_gap = 7

            start_y = panel.top + 55

            available_height = panel.bottom - 15 - start_y

            max_rows = max(
                0,
                (available_height + row_gap) // (row_height + row_gap)
            )

            for index, entry in enumerate(scores[:max_rows]):

                y = start_y + index * (row_height + row_gap)

                row = pygame.Rect(
                    panel.left + 15,
                    y,
                    panel.width - 30,
                    row_height
                )

                # Row background
                row_color = (
                    PURPLE if index % 2 == 0
                    else DARK_PURPLE
                )

                pygame.draw.rect(
                    screen,
                    row_color,
                    row
                )

                pygame.draw.rect(
                    screen,
                    HIGHLIGHT,
                    row,
                    1
                )

                # Rank colors
                if index == 0:
                    rank_color = GOLD
                elif index == 1:
                    rank_color = SILVER
                elif index == 2:
                    rank_color = BRONZE
                else:
                    rank_color = WHITE

                # Rank
                rank_text = rank_font.render(
                    f"{index + 1:02}",
                    False,
                    rank_color
                )

                screen.blit(
                    rank_text,
                    rank_text.get_rect(
                        midleft=(row.left + 12, row.centery)
                    )
                )

                # Player name
                name_surface = text_font.render(
                    str(entry["name"]),
                    False,
                    WHITE
                )

                screen.blit(
                    name_surface,
                    name_surface.get_rect(
                        midleft=(row.left + 75, row.centery)
                    )
                )

                # Score badge
                score_text = score_font.render(
                    f'{entry["score"]:,}',
                    False,
                    GOLD if index == 0 else WHITE
                )

                badge_width = score_text.get_width() + 16

                badge = pygame.Rect(
                    row.right - badge_width - 8,
                    row.top + 5,
                    badge_width,
                    row.height - 10
                )

                pygame.draw.rect(
                    screen,
                    DARK_PURPLE,
                    badge
                )

                pygame.draw.rect(
                    screen,
                    HIGHLIGHT,
                    badge,
                    1
                )

                screen.blit(
                    score_text,
                    score_text.get_rect(
                        center=badge.center
                    )
                )

        # Back button
        mouse = pygame.mouse.get_pos()

        hovered = back_button.collidepoint(mouse)

        button_color = (
            (190, 145, 220) if hovered
            else PURPLE
        )

        # Shadow
        pygame.draw.rect(
            screen,
            SHADOW,
            back_button.move(4, 4)
        )

        # Body
        pygame.draw.rect(
            screen,
            button_color,
            back_button
        )

        # Border
        pygame.draw.rect(
            screen,
            HIGHLIGHT,
            back_button,
            3
        )

        back_text = text_font.render(
            "BACK",
            False,
            WHITE
        )

        screen.blit(
            back_text,
            back_text.get_rect(
                center=back_button.center
            )
        )

        # Hint
        hint = hint_font.render(
            "PRESS ESC OR CLICK BACK TO RETURN",
            False,
            WHITE
        )

        screen.blit(
            hint,
            hint.get_rect(
                center=(width // 2, height - 12)
            )
        )

        pygame.display.flip()
        clock.tick(60)
"""import json
import pygame
import sys

def display_highscores(screen, scores):
    title_font = pygame.font.SysFont("Corbel", 44, bold=True)
    text_font = pygame.font.SysFont("Corbel", 25)
    score_font = pygame.font.SysFont("Corbel", 24, bold=True)
    hint_font = pygame.font.SysFont("Corbel", 18)
    rank_font = pygame.font.SysFont("Corbel", 22, bold=True)

    BG = (246, 243, 238)
    PURPLE = (153, 102, 204)
    DARK_PURPLE = (76, 54, 91)
    TEXT = (70, 50, 75)
    MUTED = (140, 127, 148)
    WHITE = (255, 255, 255)
    ROW_BG = (255, 252, 248)
    ROW_ALT = (240, 233, 247)
    GOLD = (218, 165, 50)
    SILVER = (150, 160, 175)
    BRONZE = (190, 120, 75)

    clock = pygame.time.Clock()
    waiting = True

    while waiting:
        width, height = screen.get_size()

        back_button = pygame.Rect(
            width // 2 - 75,
            height - 65,
            150,
            42
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    waiting = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if back_button.collidepoint(event.pos):
                    waiting = False

        screen.fill(BG)


        title = title_font.render("HIGH SCORES", True, PURPLE)
        screen.blit(
            title,
            title.get_rect(center=(width // 2, 65))
        )

       
        pygame.draw.line(
            screen,
            PURPLE,
            (width // 2 - 90, 100),
            (width // 2 + 90, 100),
            3
        )

       
        panel_width = min(480, width - 40)
        panel_height = min(440, height - 160)

        panel = pygame.Rect(
            (width - panel_width) // 2,
            120,
            panel_width,
            panel_height
        )

        pygame.draw.rect(
            screen,
            (225, 216, 236),
            panel.move(0, 5),
            border_radius=20
        )

        pygame.draw.rect(
            screen,
            WHITE,
            panel,
            border_radius=20
        )

        pygame.draw.rect(
            screen,
            (224, 211, 239),
            panel,
            width=2,
            border_radius=20
        )

       
        heading_y = panel.top + 22

        rank_heading = hint_font.render("RANK", True, MUTED)
        screen.blit(
            rank_heading,
            (panel.left + 24, heading_y)
        )

        score_heading = hint_font.render("SCORE", True, MUTED)
        screen.blit(
            score_heading,
            score_heading.get_rect(
                midright=(panel.right - 22, heading_y + 10)
            )
        )

        if not scores:
            message = text_font.render(
                "No scores yet. Start playing!",
                True,
                TEXT
            )

            screen.blit(
                message,
                message.get_rect(center=panel.center)
            )

        else:
            row_height = 35
            row_gap = 5
            start_y = panel.top + 55
            available_height = panel.bottom - 20 - start_y

            max_rows = max(
                0,
                (available_height + row_gap) // (row_height + row_gap)
            )

            for index, entry in enumerate(scores[:max_rows]):
                y = start_y + index * (row_height + row_gap)

                row = pygame.Rect(
                    panel.left + 15,
                    y,
                    panel.width - 30,
                    row_height
                )

                row_color = ROW_BG if index % 2 == 0 else ROW_ALT

                pygame.draw.rect(
                    screen,
                    row_color,
                    row,
                    border_radius=10
                )

              
                if index == 0:
                    rank_color = GOLD
                elif index == 1:
                    rank_color = SILVER
                elif index == 2:
                    rank_color = BRONZE
                else:
                    rank_color = MUTED

                rank_text = rank_font.render(
                    f"{index + 1:02}",
                    True,
                    rank_color
                )

                screen.blit(
                    rank_text,
                    rank_text.get_rect(
                        midleft=(row.left + 12, row.centery)
                    )
                )

             
                name_surface = text_font.render(
                    str(entry["name"]),
                    True,
                    TEXT
                )

                screen.blit(
                    name_surface,
                    name_surface.get_rect(
                        midleft=(row.left + 65, row.centery)
                    )
                )

              
                score_text = score_font.render(
                    f'{entry["score"]:,}',
                    True,
                    DARK_PURPLE
                )

                badge_width = score_text.get_width() + 20

                badge = pygame.Rect(
                    row.right - badge_width - 8,
                    row.top + 4,
                    badge_width,
                    row.height - 8
                )

                pygame.draw.rect(
                    screen,
                    (230, 220, 243),
                    badge,
                    border_radius=8
                )

                screen.blit(
                    score_text,
                    score_text.get_rect(center=badge.center)
                )

       
        mouse_pos = pygame.mouse.get_pos()

        if back_button.collidepoint(mouse_pos):
            button_color = (126, 82, 176)
        else:
            button_color = PURPLE

        pygame.draw.rect(
            screen,
            button_color,
            back_button,
            border_radius=14
        )

        back_text = text_font.render(
            "BACK",
            True,
            WHITE
        )

        screen.blit(
            back_text,
            back_text.get_rect(center=back_button.center)
        )

     
        hint = hint_font.render(
            "Press ESC or click BACK to return",
            True,
            MUTED
        )

        screen.blit(
            hint,
            hint.get_rect(center=(width // 2, height - 12))
        )

        pygame.display.flip()
        clock.tick(40)
"""
