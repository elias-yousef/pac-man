import pygame
from hud import HUD

pygame.init()

WIDTH = 510
HEIGHT = 570

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("HUD Test")

hud = HUD(WIDTH)
clock = pygame.time.Clock()

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 30, 30))

    hud.draw_BG(screen)
    hud.draw_timer(screen, 90)
    hud.draw_score(screen, 1200)

    hud.draw_lives(screen, 7)
    hud.draw_level(screen, 1)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
