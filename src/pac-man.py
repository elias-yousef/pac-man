import pygame
import sys
from pathlib import Path
from mazegenerator.Mazegenerator import MazeGenerator


def neighbors(
        maze: list[list[int]], x: int, y: int,
        col_size: int, row_size: int
        ) -> list[int]:
    alowed = []
    if x > 0 and not maze[y][x] & 8:
        alowed.append(4)
    if x < row_size and not maze[y][x] & 2:
        alowed.append(3)
    if y > 0 and not maze[y][x] & 1:
        alowed.append(1)
    if y < col_size and not maze[y][x] & 4:
        alowed.append(2)
    return alowed


def main() -> None:
    pygame.init()
    col_size = 15
    row_size = 15
    TILE_SIZE = 512 // 15
    GAME_HIGHT = TILE_SIZE * col_size
    GAME_WIDTH = TILE_SIZE * col_size
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
    pacman = pygame.image.load((Path("/Users/elias/pacman/images/pacman1.bmp"))).convert()

    clock = pygame.time.Clock()
    pygame.display.set_caption("pac-man")

    maze = MazeGenerator((row_size, col_size), seed=42)
    maze_arr = maze.maze

    current_direction = None
    next_direction = None
    running = True
    while running:
        window.fill((0, 0, 0))
        for row_index, row in enumerate(maze_arr):
            for col_index, cell_value in enumerate(row):
                if cell_value > 0:
                    x_pixel = col_index * TILE_SIZE
                    y_pixel = row_index * TILE_SIZE
                    window.blit(loaded_images[cell_value], (x_pixel, y_pixel))
        current_col = PLAYER_X // TILE_SIZE
        current_row = PLAYER_Y // TILE_SIZE
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                next_direction = event.key
        alowed = neighbors(maze_arr, current_col, current_row, col_size, row_size)
        if next_direction in keys:
            if PLAYER_X % TILE_SIZE == 0 and PLAYER_Y % TILE_SIZE == 0:
                if keys[next_direction] in alowed:
                    current_direction = next_direction
                if current_direction in keys and keys[current_direction] not in alowed:
                        current_direction = None
        if current_direction in keys and keys[current_direction] == 1:
            PLAYER_Y -= 2
        elif current_direction in keys and keys[current_direction] == 2:
            PLAYER_Y += 2
        elif current_direction in keys and keys[current_direction] == 3:
            PLAYER_X += 2
        elif current_direction in keys and keys[current_direction] == 4:
            PLAYER_X -= 2
        window.blit(pacman, (x_pixel, y_pixel))
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    sys.exit(0)    


if __name__ == "__main__":
    main()