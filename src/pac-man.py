import pygame
import sys
from pathlib import Path
from mazegenerator.Mazegenerator import MazeGenerator

def main() -> None:
    pygame.init()
    GAME_HIGHT = 512
    GAME_WIDTH = 512
    TILE_SIZE = GAME_WIDTH // 15
    PLAYER_X = 7 * TILE_SIZE
    PLAYER_Y = 7 * TILE_SIZE

    cell_images = {
        1: "/Users/elias/pacman/images/1.bmp",
        2: "/Users/elias/pacman/images/2.bmp",
        3: "/Users/elias/pacman/images/3.bmp",
        4: "/Users/elias/pacman/images/4.bmp",
        5: "/Users/elias/pacman/images/5.bmp",
        6: "/Users/elias/pacman/images/6.bmp",
        7: "/Users/elias/pacman/images/7.bmp",
        8: "/Users/elias/pacman/images/8.bmp",
        9: "/Users/elias/pacman/images/9.bmp",
        10: "/Users/elias/pacman/images/10.bmp",
        11: "/Users/elias/pacman/images/11.bmp",
        12: "/Users/elias/pacman/images/12.bmp",
        13: "/Users/elias/pacman/images/13.bmp",
        14: "/Users/elias/pacman/images/14.bmp",
        15: "/Users/elias/pacman/images/15.bmp",
    }

    keys = {
        pygame.K_w: 1, pygame.K_UP: 1,
          pygame.K_s: 2, pygame.K_DOWN: 2,
            pygame.K_d: 3, pygame.K_RIGHT: 3,
              pygame.K_a: 4, pygame.K_LEFT: 4
              }
    window = pygame.display.set_mode((GAME_WIDTH, GAME_HIGHT))

    loaded_images = {}
    for cell_value, path in cell_images.items():
        loaded_images[cell_value] = pygame.image.load(Path(path)).convert()

    clock = pygame.time.Clock()
    pygame.display.set_caption("pac-man")

    maze = MazeGenerator((15, 15), seed=42)
    maze_arr = maze.maze

    running = True
    solid_walls = []
    while running:
        OLD_X = PLAYER_X
        OLD_Y = PLAYER_Y
        for row_index, row in enumerate(maze_arr):
            for col_index, cell_value in enumerate(row):
                if cell_value > 0:
                    x_pixel = col_index * TILE_SIZE
                    y_pixel = row_index * TILE_SIZE
                    window.blit(loaded_images[cell_value], (x_pixel, y_pixel))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key in keys and keys[event.key] == 1:
                    OLD_Y = PLAYER_Y
                    PLAYER_Y -= 34
                if event.key in keys and keys[event.key] == 2:
                    OLD_Y = PLAYER_Y
                    PLAYER_Y += 34
                if event.key in keys and keys[event.key] == 3:
                    OLD_X = PLAYER_X
                    PLAYER_X += 34
                if event.key in keys and keys[event.key] == 4:
                    OLD_X = PLAYER_X
                    PLAYER_X -= 34
        player_rect = pygame.Rect(PLAYER_X, PLAYER_Y, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(window, (255, 255, 255), player_rect)
        collision_index = player_rect.collidelist(solid_walls)
        if collision_index != -1:
            PLAYER_X = OLD_X
            PLAYER_Y = OLD_Y
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    sys.exit(0)    







# GAME_HIGHT = 512
# GAME_WIDTH = 512
# m = MazeGenerator(size=(15, 15), seed=42)
# pygame.init()
# window = pygame.display.set_mode((GAME_WIDTH, GAME_HIGHT))
# clock = pygame.time.Clock()
# player = pygame.Rect(150, 150, 50, 50)
# is_true = True
# while is_true:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit(1)
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_UP] or keys[pygame.K_w]:
#         player.y -= 5
#     if keys[pygame.K_DOWN] or keys[pygame.K_s]:
#         player.y += 5
#     if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
#         player.x += 5
#     if keys[pygame.K_LEFT] or keys[pygame.K_a]:
#         player.x -= 5
    
#     window.fill((1, 1, 1))
#     pygame.draw.rect(window, (255, 255, 255), player)
#     pygame.display.update()
#     clock.tick(60)

if __name__ == "__main__":
    main()