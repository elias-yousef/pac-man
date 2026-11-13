import pygame
import sys


'''
while running:
    # Handle events

    # Update game

    # Draw the maze and Pac-Man

    # Update the screen
'''


def pause(screen) -> str:

    title_font = pygame.font.SysFont("Corbel", 44, bold=True)
    text_font = pygame.font.SysFont("Corbel", 25)

    BG = (246, 243, 238)
    PURPLE = (153, 102, 204)
    WHITE = (255, 255, 255)
    clock = pygame.time.Clock()
    background = screen.copy()
    waiting = True

    while waiting:

        width, height = screen.get_size()
        start_y = height // 2 - 45

        resume = pygame.Rect(
            width // 2 - 75,
            start_y,
            150,
            42
        )

        mainmenu = pygame.Rect(
            width // 2 - 125,
            start_y + 57,
            250,
            42
        )


        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:#This means pressing Escape ends the Pause screen's loop.
                if event.key == pygame.K_ESCAPE:
                    return "resume"

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if resume.collidepoint(event.pos):
                    return "resume" #resume_screen()

                elif mainmenu.collidepoint(event.pos):
                    return "menu" #main_menu()
        screen.blit(background, (0, 0))


        #screen.fill(BG)#fix this cuz its colored the bg and never show the game screen behind it 

        overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        overlay.fill((246, 243, 238, 170))
        screen.blit(overlay, (0, 0))


        title = title_font.render("PAUSE", True, PURPLE)
        screen.blit(
                title,
                title.get_rect(center=(width // 2, 65))
        )

        mouse_pos = pygame.mouse.get_pos()

        if resume.collidepoint(mouse_pos):
            button_color = (126, 82, 176)
        else:
            button_color = PURPLE

        pygame.draw.rect(
            screen,
            button_color,
            resume,
            border_radius=14
        )

         
        if mainmenu.collidepoint(mouse_pos):
            button_color = (126, 82, 176)
        else:
            button_color = PURPLE

        pygame.draw.rect(
            screen,
            button_color,
            mainmenu,
            border_radius=14
        )

        resume_text = text_font.render("RESUME", True, WHITE)
        screen.blit(
            resume_text,
            resume_text.get_rect(center=resume.center)
        )
        menu_text = text_font.render("MAIN MENU", True, WHITE)
        screen.blit(
            menu_text,
            menu_text.get_rect(center=mainmenu.center)
        )


        pygame.display.flip()
        clock.tick(60)
