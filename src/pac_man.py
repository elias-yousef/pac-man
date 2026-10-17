import pygame
import sys
from pathlib import Path
from mazegenerator.Mazegenerator import MazeGenerator
from Charcacters import GAME
from hud import HUD

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


def load_maze_images() -> dict:
    cell_images = {
        1: "/mnt/c/Users/leen9/leen42/pacman/lilyver/images/1.bmp",
        2: "/mnt/c/Users/leen9/leen42/pacman/lilyver/images/2.bmp",
        3: "/mnt/c/Users/leen9/leen42/pacman/lilyver/images/3.bmp",
        4: "/mnt/c/Users/leen9/leen42/pacman/lilyver/images/4.bmp",
        5: "/mnt/c/Users/leen9/leen42/pacman/lilyver/images/5.bmp",
        6: "/mnt/c/Users/leen9/leen42/pacman/lilyver/images/6.bmp",
        7: "/mnt/c/Users/leen9/leen42/pacman/lilyver/images/7.bmp",
        8: "/mnt/c/Users/leen9/leen42/pacman/lilyver/images/8.bmp",
        9: "/mnt/c/Users/leen9/leen42/pacman/lilyver/images/9.bmp",
        10: "/mnt/c/Users/leen9/leen42/pacman/lilyver/images/10.bmp",
        11: "/mnt/c/Users/leen9/leen42/pacman/lilyver/images/11.bmp",
        12: "/mnt/c/Users/leen9/leen42/pacman/lilyver/images/12.bmp",
        13: "/mnt/c/Users/leen9/leen42/pacman/lilyver/images/13.bmp",
        14: "/mnt/c/Users/leen9/leen42/pacman/lilyver/images/14.bmp",
        15: "/mnt/c/Users/leen9/leen42/pacman/lilyver/images/15.bmp",
    }
    loaded_images = {}
    for cell_value, path in cell_images.items():
        loaded_images[cell_value] = pygame.image.load(Path(path)).convert()
    return loaded_images

'''
def draw_maze(
        window: Surface, maze_list: list[int],
          TILE_SIZE: int, loaded_images: dict
        ) -> None:
    for row_index, row in enumerate(maze_list):
        for col_index, cell_value in enumerate(row):
            if cell_value > 0:
                x_pixel = col_index * TILE_SIZE
                y_pixel = row_index * TILE_SIZE + HUD_HEIGHT
                window.blit(loaded_images[cell_value], (x_pixel, y_pixel))
'''
def draw_maze(
    window,
    maze_list,
    TILE_SIZE,
    loaded_images,
    y_offset=0
    ):
    for row_index, row in enumerate(maze_list):
        for col_index, cell_value in enumerate(row):
            if cell_value > 0:
                x_pixel = col_index * TILE_SIZE
                y_pixel = row_index * TILE_SIZE + y_offset

                window.blit(
                    loaded_images[cell_value],
                    (x_pixel, y_pixel)
                )
def update_physics(
        TILE_SIZE: int, PLAYER_X: int, PLAYER_Y: int,
          alowed: list[int], next_direction: int | None, current_direction: int | None
        ) -> tuple[int, int, int | None]:
    keys = {
        pygame.K_w: 1, pygame.K_UP: 1,
          pygame.K_s: 2, pygame.K_DOWN: 2,
            pygame.K_d: 3, pygame.K_RIGHT: 3,
              pygame.K_a: 4, pygame.K_LEFT: 4
              }
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
    return PLAYER_X, PLAYER_Y, current_direction


def main() -> str:
    pygame.init()
    TILE_SIZE = 512 // 15
    col_size = 15
    row_size = 15
    HUD_HEIGHT = 60
    GAME_HIGHT = TILE_SIZE * col_size
    GAME_WIDTH = TILE_SIZE * row_size
    PLAYER_X = 7 * TILE_SIZE
    PLAYER_Y = 7 * TILE_SIZE
    
    window = pygame.display.set_mode(
        (GAME_WIDTH, GAME_HIGHT + HUD_HEIGHT)
    )

    game = GAME(TILE_SIZE, col_size, row_size, window)

    #window = pygame.display.set_mode((GAME_WIDTH, GAME_HIGHT))

    hud = HUD(GAME_WIDTH)
    loaded_images = load_maze_images()
    pacman = pygame.image.load((Path("/mnt/c/Users/leen9/leen42/pacman/lilyver/images/pacman1.bmp"))).convert()
    pacman = pygame.transform.scale(pacman, (TILE_SIZE, TILE_SIZE))
    clock = pygame.time.Clock()
    pygame.display.set_caption("pac-man")
    maze = MazeGenerator((row_size, col_size))
    maze_arr = maze.maze
    current_direction = None
    next_direction = None
    running = True

    while running:
        
        window.fill((0, 0, 0))
        
        #draw_maze(window, maze_arr, TILE_SIZE, loaded_images, y_offset=HUD_HEIGHT)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    next_direction = event.key
        
        current_col = PLAYER_X // TILE_SIZE
        current_row = PLAYER_Y // TILE_SIZE
        
        alowed = neighbors(maze_arr, current_col, current_row, col_size, row_size, )
        
        PLAYER_X, PLAYER_Y, current_direction = update_physics(TILE_SIZE, PLAYER_X, PLAYER_Y, alowed, next_direction, current_direction)
        draw_maze( window, maze_arr, TILE_SIZE, loaded_images, y_offset=HUD_HEIGHT )    
        window.blit(pacman, (PLAYER_X, PLAYER_Y + HUD_HEIGHT))
        hud.draw( window, score=0, lives=3, level=1, remaining_time=120)
        pygame.display.update()
        
        clock.tick(60)
    return "menu"


if __name__ == "__main__":
    result = main()
    pygame.quit()
'''
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()
'''
