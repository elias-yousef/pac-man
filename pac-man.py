import pygame
import sys
import time
from mazegenerator import MazeGenerator


GAME_HIGHT = 512
GAME_WIDTH = 512
m = MazeGenerator(size=(15, 15), seed=42)
pygame.init()
window = pygame.display.set_mode((GAME_WIDTH, GAME_HIGHT))
clock = pygame.time.Clock()
player = pygame.Rect(150, 150, 50, 50)
is_true = True
while is_true:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(1)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] or keys[pygame.K_w]:
        player.y -= 5
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player.y += 5
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player.x += 5
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player.x -= 5
    
    window.fill((1, 1, 1))
    pygame.draw.rect(window, (255, 255, 255), player)
    pygame.display.update()
    clock.tick(60)
    time.sleep(99)
    is_true == False


if __name__ == "__main__":
    pass