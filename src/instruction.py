import pygame
import sys
def display_instructions(screen):
    title_font = pygame.font.SysFont("Corbel", 44, bold=True)
    heading_font = pygame.font.SysFont("Corbel", 25, bold=True)
    text_font = pygame.font.SysFont("Corbel", 19)
    hint_font = pygame.font.SysFont("Corbel", 17)

    BG = (246, 243, 238)
    PURPLE = (153, 102, 204)
    DARK_PURPLE = (76, 54, 91)
    TEXT = (70, 50, 75)
    MUTED = (140, 127, 148)
    WHITE = (255, 255, 255)
    ROW_ALT = (240, 233, 247)

    clock = pygame.time.Clock()
    waiting = True

    while waiting:
        width, height = screen.get_size()

        back_button = pygame.Rect(
            width // 2 - 75,
            height - 60,
            150,
            40
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

     
        title = title_font.render("HOW TO PLAY", True, PURPLE)
        screen.blit(
            title,
            title.get_rect(center=(width // 2, 45))
        )

     
        pygame.draw.line(
            screen,
            PURPLE,
            (width // 2 - 90, 78),
            (width // 2 + 90, 78),
            3
        )

       
        panel_width = min(600, width - 40)
        panel_height = height - 155

        panel = pygame.Rect(
            (width - panel_width) // 2,
            95,
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

        x = panel.left + 25
        y = panel.top + 18
        line_gap = 25

       
        heading = heading_font.render("OBJECTIVE", True, PURPLE)
        screen.blit(heading, (x, y))
        y += 32

        objective = [
            "Navigate through the maze and collect all the dots.",
            "Avoid ghosts and try to survive!",
        ]

        for line in objective:
            text = text_font.render(line, True, TEXT)
            screen.blit(text, (x, y))
            y += line_gap


        y += 3
        pygame.draw.line(
            screen,
            ROW_ALT,
            (x, y),
            (panel.right - 25, y),
            2
        )
        y += 12
      
        heading = heading_font.render("CONTROLS", True, PURPLE)
        screen.blit(heading, (x, y))
        y += 35

        arrow_x = x + 12
        text_x = x + 45
        arrow_size = 8

        controls = [
            ("UP", "Move up", 0, -1),
            ("DOWN", "Move down", 0, 1),
            ("LEFT", "Move left", -1, 0),
            ("RIGHT", "Move right", 1, 0),
        ]

        for _, description, dx, dy in controls:
            center_x = arrow_x + arrow_size
            center_y = y + 9

           
            if dx == 0:
                pygame.draw.line(
                    screen, PURPLE,
                    (center_x, center_y - dy * 7),
                    (center_x, center_y + dy * 5),
                    3
                )
            else:
                pygame.draw.line(
                    screen, PURPLE,
                    (center_x - dx * 7, center_y),
                    (center_x + dx * 5, center_y),
                    3
                )

            if dy == -1:  
                points = [
                    (center_x, center_y - 8),
                    (center_x - 6, center_y - 1),
                    (center_x + 6, center_y - 1)
                ]
            elif dy == 1:
                points = [
                    (center_x, center_y + 8),
                    (center_x - 6, center_y + 1),
                    (center_x + 6, center_y + 1)
                ]
            elif dx == -1:
                points = [
                    (center_x - 8, center_y),
                    (center_x - 1, center_y - 6),
                    (center_x - 1, center_y + 6)
                ]
            else:
                points = [
                    (center_x + 8, center_y),
                    (center_x + 1, center_y - 6),
                    (center_x + 1, center_y + 6)
                ]

            pygame.draw.polygon(screen, PURPLE, points)

            text = text_font.render(description, True, TEXT)
            screen.blit(text, (text_x, y))
            y += 25

        esc_text = text_font.render(
            "ESC  -  Return to the main menu",
            True,
            TEXT
        )
        screen.blit(esc_text, (x, y))
        y += 25

               heading = heading_font.render("GAME RULES", True, PURPLE)
        screen.blit(heading, (x, y))
        y += 32

        rules = [
            "Collect dots to earn points.",
            "Avoid ghosts; touching them can cost you a life.",
            "Power pellets let you eat ghosts temporarily.",
            "Collect all required dots to win the level.",
            "The game ends when you lose all your lives.",
        ]

        for line in rules:
            text = text_font.render(line, True, TEXT)
            screen.blit(text, (x, y))
            y += line_gap

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

        back_text = text_font.render("BACK", True, WHITE)
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
            hint.get_rect(center=(width // 2, height - 10))
        )

        pygame.display.flip()
        clock.tick(40)
