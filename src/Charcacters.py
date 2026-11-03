import pygame
from mazegenerator import MazeGenerator
from pathlib import Path
import random

class Ghosts:
    def __init__(
            self, ghost_num: int, x: int, y: int,
              TILE_SIZE: int, maze_arr, row_size: int, col_size: int
            ):
        self.start_col = x
        self.start_row = y
        self.col = x
        self.row = y
        self.col_size = col_size
        self.row_size = row_size
        self.maze_arr = maze_arr
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.TILE_SIZE = TILE_SIZE
        self.ghost = ghost_num
        self.current_direction = None
        self.chosen_path = None
        self.mode = "chasing"
        self.alowed = []

        self.script_dir = Path(__file__).resolve().parent.parent
        self.image = pygame.image.load(self.script_dir / "images" / f"ghost{ghost_num}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.TILE_SIZE, self.TILE_SIZE))

    def reset(self) -> None:
        """Reset ghost to initial spawn position."""
        self.col = self.start_col
        self.row = self.start_row
        self.pixel_x = self.start_col * self.TILE_SIZE
        self.pixel_y = self.start_row * self.TILE_SIZE

    def draw_ghost(self, window):
        window.blit(self.image, (self.pixel_x, self.pixel_y))

    def neighbors(self) -> None:
        self.alowed = []
        if self.col > 0 and not self.maze_arr[self.row][self.col] & 8:
            self.alowed.append(8)
        if self.col < self.row_size - 1 and not self.maze_arr[self.row][self.col] & 2:
            self.alowed.append(2)
        if self.row > 0 and not self.maze_arr[self.row][self.col] & 1:
            self.alowed.append(1)
        if self.row < self.col_size - 1 and not self.maze_arr[self.row][self.col] & 4:
            self.alowed.append(4)

    def direction(self, player_col: int, player_row: int):
        try_dir = {}
        dis_num = {0: 0, 1: 6, 2: 8, 3: 4}
        opposite_map = {1: 4, 4: 1, 2: 8, 8: 2}
        direction_map = {
            1: (0, -1),
            2: (1, 0),
            4: (0, 1),
            8: (-1, 0)
        }
        if self.pixel_x % self.TILE_SIZE == 0 and self.pixel_y % self.TILE_SIZE == 0:
            if not self.alowed:
                return
            opp = opposite_map.get(self.current_direction)
            valid_moves = [d for d in self.alowed if d != opp]
            candidates = valid_moves if valid_moves else self.alowed
            if self.distance > dis_num[self.ghost]:
                self.current_direction = random.choice(candidates)
            elif self.distance <= dis_num[self.ghost]:
                for allow in candidates:
                    d_col, d_row = direction_map[allow]
                    next_col = self.col + d_col
                    next_row = self.row + d_row
                    try_dir[allow] = abs(next_col - player_col) + abs(next_row - player_row)
                if try_dir:
                    self.current_direction = min(try_dir, key=try_dir.get)


    def update(self, player_col: int, player_row: int):
        direction_map = {1: (0, -1), 2: (1, 0), 4: (0, 1), 8: (-1, 0)}
        self.col = self.pixel_x // self.TILE_SIZE
        self.row = self.pixel_y // self.TILE_SIZE
        self.distance = abs(self.col - player_col) + abs(self.row - player_row)
        self.neighbors()
        self.direction(player_col, player_row)
        if self.mode == "chasing":
            c_col, c_row = direction_map[self.current_direction]
            self.pixel_x += c_col * 2
            self.pixel_y += c_row * 2
        elif self.mode == "edible":
            pass


class Pacman:
    def __init__(self, TILE_SIZE: int, lives: int, row_size: int, col_size: int):
        self.lives = lives
        self.next_direction = None
        self.current_direction = None
        self.col_size = col_size
        self.row_size = row_size
        self.start_col = row_size // 2
        self.start_row =  (col_size // 2) + 2
        self.TILE_SIZE = TILE_SIZE
        self.PLAYER_X = self.start_col * self.TILE_SIZE
        self.PLAYER_Y = self.start_row * self.TILE_SIZE
        self.current_col = self.start_col
        self.current_row = self.start_row
        self.alowed = []

        self.script_dir = Path(__file__).resolve().parent.parent
        self.abs_path_pacman = self.script_dir / "images" / f"pacman.png"
        self.pacman = pygame.image.load(str(self.abs_path_pacman))
        self.pacman = pygame.transform.scale(self.pacman, (self.TILE_SIZE, self.TILE_SIZE))

    def draw_pac(self, window):
        window.blit(self.pacman, (self.PLAYER_X, self.PLAYER_Y))

    def reset_position(self) -> None:
        """Reset player to starting point."""
        self.PLAYER_X = self.start_col * self.TILE_SIZE
        self.PLAYER_Y = self.start_row * self.TILE_SIZE
        self.current_direction = None

    def neighbors(self, maze_arr) -> None:
        self.alowed = []
        if self.current_col > 0 and not maze_arr[self.current_row][self.current_col] & 8:
            self.alowed.append(8)
        if self.current_col < self.row_size - 1 and not maze_arr[self.current_row][self.current_col] & 2:
            self.alowed.append(2)
        if self.current_row > 0 and not maze_arr[self.current_row][self.current_col] & 1:
            self.alowed.append(1)
        if self.current_row < self.col_size - 1 and not maze_arr[self.current_row][self.current_col] & 4:
            self.alowed.append(4)

    def update_physics(self) -> None:
        keys = {
            pygame.K_w: 1, pygame.K_UP: 1,
                pygame.K_s: 4, pygame.K_DOWN: 4,
                    pygame.K_d: 2, pygame.K_RIGHT: 2,
                        pygame.K_a: 8, pygame.K_LEFT: 8
              }
        if self.next_direction in keys:
            if self.PLAYER_X % self.TILE_SIZE == 0 and self.PLAYER_Y % self.TILE_SIZE == 0:
                if keys[self.next_direction] in self.alowed:
                    self.current_direction = self.next_direction
                if self.current_direction in keys and keys[self.current_direction] not in self.alowed:
                        self.current_direction = None
        if self.current_direction in keys and keys[self.current_direction] == 1:
            self.PLAYER_Y -= 2
        elif self.current_direction in keys and keys[self.current_direction] == 4:
            self.PLAYER_Y += 2
        elif self.current_direction in keys and keys[self.current_direction] == 2:
            self.PLAYER_X += 2
        elif self.current_direction in keys and keys[self.current_direction] == 8:
            self.PLAYER_X -= 2


class Game:
    def __init__(self, config: dict):
        self.config = config
        self.running = True
        self.lives = config["lives"]
        self.pacgum_points = config["points_per_pacgum"]
        self.seed = config.get("seed", 42)
        level_info = config["levels"]
        self.row_size = level_info["width"]
        self.col_size = level_info["height"]
        self.TILE_SIZE = 32
        self.GAME_WIDTH = self.TILE_SIZE * self.row_size
        self.GAME_HIGHT = self.TILE_SIZE * self.col_size
        self.window = pygame.display.set_mode((self.GAME_WIDTH, self.GAME_HIGHT))
        pygame.display.set_caption("Pac-Man")
        self.maze_arr = MazeGenerator((self.row_size, self.col_size), seed=self.seed).maze
        self.pacman = Pacman(self.TILE_SIZE, self.lives, self.row_size, self.col_size)
        self.ghosts = [
            Ghosts(0, 0, 0, self.TILE_SIZE, self.maze_arr, self.row_size, self.col_size),
            Ghosts(1, self.row_size - 1, 0, self.TILE_SIZE, self.maze_arr, self.row_size, self.col_size),
            Ghosts(2, 0, self.col_size - 1, self.TILE_SIZE, self.maze_arr, self.row_size, self.col_size),
            Ghosts(3, self.row_size - 1, self.col_size - 1, self.TILE_SIZE, self.maze_arr, self.row_size, self.col_size),
        ]

        self.load_maze_images()
        self.clock = pygame.time.Clock()

    def draw_maze(self) -> None: 
        for row_index, row in enumerate(self.maze_arr):
            for col_index, cell_value in enumerate(row):
                if cell_value > 0:
                    x_pixel = col_index * self.TILE_SIZE
                    y_pixel = row_index * self.TILE_SIZE
                    self.window.blit(self.loaded_images[cell_value], (x_pixel, y_pixel))

    def load_maze_images(self) -> None:
        self.loaded_images = {}
        script_dir = Path(__file__).resolve().parent.parent
        for i in range(1, 16):
            abs_path = script_dir / "images" / f"{i}.bmp"
            if abs_path.exists():
                img = pygame.image.load(str(abs_path)).convert()
                self.loaded_images[i] = pygame.transform.scale(img, (self.TILE_SIZE, self.TILE_SIZE))

    def reset_positions(self) -> None:
        """Reset player and ghost positions after a loss of life."""
        self.pacman.reset_position()
        for ghost in self.ghosts:
            ghost.reset()

    def run(self) -> None:
        while self.running:
            self.window.fill((0, 0, 0))
            self.draw_maze()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.pacman.next_direction = event.key
            self.pacman.current_col = self.pacman.PLAYER_X // self.TILE_SIZE
            self.pacman.current_row = self.pacman.PLAYER_Y // self.TILE_SIZE
            self.pacman.neighbors(self.maze_arr)
            self.pacman.update_physics()
            self.pacman.draw_pac(self.window)
            for ghost in self.ghosts:
                dx = self.pacman.PLAYER_X - ghost.pixel_x
                dy = self.pacman.PLAYER_Y - ghost.pixel_y
                distance = (dx ** 2 + dy ** 2) ** 0.5
                if distance < self.TILE_SIZE // 2:
                    self.pacman.lives -= 1
                    self.pacman.PLAYER_X = 7 * self.TILE_SIZE
                    self.pacman.PLAYER_Y = 7 * self.TILE_SIZE
                    # i need to reset the ghosts too here
                    if self.pacman.lives <= 0:
                        self.running = False
                    else:
                        self.reset_positions()
                ghost.draw_ghost(self.window)
                ghost.update(self.pacman.current_col, self.pacman.current_row)
            pygame.display.update()
            self.clock.tick(60)





