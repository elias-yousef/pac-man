import pygame
import sys


def display_instructions(screen: pygame.Surface) -> None:
    """Display the instructions screen until a key or mouse button is pressed."""

    # Fonts
    font_title = pygame.font.SysFont("georgia", 48, bold=True)
    font_text = pygame.font.SysFont("corbel", 25)
    font_hint = pygame.font.SysFont("corbel", 22, italic=True)
    font_section = pygame.font.SysFont("corbel", 28, bold=True)

    BG = (28, 24, 45)              # Dark purple background
    WHITE = (248, 244, 255)        # Soft white
    PINK = (255, 170, 200)         # Pastel pink
    LAVENDER = (205, 180, 255)     # Lavender
    BLUE = (170, 210, 255)         # Powder blue
    YELLOW = (255, 225, 150)       # Soft yellow
    MUTED = (175, 165, 195)        # Muted lavender
    LINE = (75, 65, 100)           # Divider color

    instructions = [
        ("➤", "Arrow Keys", "Move Pac-Man"),
        ("●", "Pacgums", "Eat all pacgums to complete each level"),
        ("★", "Complete all levels", "Win the game"),
        ("✦", "Super pacgums", "Make ghosts edible"),
        ("✧", "Edible ghosts", "Eat them for bonus points"),
        ("!", "Danger", "Avoid non-edible ghosts or lose a life"),
        ("⌨", "Escape", "Pause the game"),
    ]

    cheat_instructions = [
        ("C", "Toggle Cheat Mode"),
        ("∞", "Endless lives and no timer"),
        ("N", "Skip to the next level"),
    ]

    clock = pygame.time.Clock()
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

        decorations = [
            (45, 45, PINK),
            (width - 45, 55, LAVENDER),
            (75, height - 55, BLUE),
            (width - 65, height - 65, YELLOW),
        ]

        for x, y, color in decorations:
            star = font_text.render("✦", True, color)
            screen.blit(star, star.get_rect(center=(x, y)))

        title = font_title.render("HOW TO PLAY", True, PINK)
        title_rect = title.get_rect(center=(width // 2, 55))
        screen.blit(title, title_rect)

        subtitle = font_hint.render(
            "✧  A little guide to your Pac-Man adventure  ✧",
            True,
            MUTED,
        )
        screen.blit(
            subtitle,
            subtitle.get_rect(center=(width // 2, 100)),
        )

        pygame.draw.line(
            screen, LINE,
            (width // 2 - 250, 130),
            (width // 2 + 250, 130),
            2,
        )

        y = 155

        for symbol, heading, description in instructions:
            icon_color = YELLOW if symbol in ("★", "✦") else LAVENDER

            icon = font_text.render(symbol, True, icon_color)
            screen.blit(icon, (width // 2 - 250, y))

            heading_text = font_text.render(heading, True, PINK)
            screen.blit(heading_text, (width // 2 - 215, y))

            # Render the description separately when there is room.
            description_text = font_text.render(
                description, True, WHITE
            )
            screen.blit(
                description_text,
                (width // 2 - 215, y + 27),
            )

            y += 68

        # Cheat mode section
        section_y = y + 2

        pygame.draw.line(
            screen, LINE,
            (width // 2 - 250, section_y),
            (width // 2 + 250, section_y),
            2,
        )

        section_y += 28

        cheat_title = font_section.render(
            "✦  CHEAT MODE  ✦", True, YELLOW
        )
        screen.blit(
            cheat_title,
            cheat_title.get_rect(
                center=(width // 2, section_y)
            ),
        )

        section_y += 35

        for key, description in cheat_instructions:
            key_text = font_text.render(
                f"[ {key} ]", True, LAVENDER
            )
            description_text = font_text.render(
                description, True, WHITE
            )

            screen.blit(
                key_text,
                (width // 2 - 220, section_y),
            )
            screen.blit(
                description_text,
                (width // 2 - 130, section_y),
            )

            section_y += 32

        # Return hint at the bottom
        hint = font_hint.render(
            "♡  Press any key to return to the menu  ♡",
            True,
            MUTED,
        )

        screen.blit(
            hint,
            hint.get_rect(
                center=(width // 2, height - 25)
            ),
        )

        pygame.display.update()
        clock.tick(40)

