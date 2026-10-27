import pygame
from mazegenerator import MazeGenerator
from pathlib import Path
import random

class Ghosts:
    def __init__(
            self, ghost_num: int, x: int, y: int,
              TILE_SIZE: int, maze_arr, row_size: int, col_size: int
            ):
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
        self.mode = "chasing"
        self.script_dir = Path(__file__).resolve().parent.parent
        self.image = pygame.image.load(self.script_dir / "images" / f"ghost{ghost_num}.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.TILE_SIZE, self.TILE_SIZE))

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

    def update(self, player_col: int, player_row: int):
        self.col = self.pixel_x // self.TILE_SIZE
        self.row = self.pixel_y // self.TILE_SIZE
        if self.pixel_x % self.TILE_SIZE == 0 and self.pixel_y % self.TILE_SIZE == 0:
            self.neighbors()
            if self.current_direction == 1 and len(self.alowed) > 1:
                self.alowed.remove(4)
            elif self.current_direction == 8 and len(self.alowed) > 1:
                self.alowed.remove(2)
            if self.current_direction == 2 and len(self.alowed) > 1:
                self.alowed.remove(8)
            elif self.current_direction == 4 and len(self.alowed) > 1:
                self.alowed.remove(1)
            self.current_direction = random.choice(self.alowed)
        if self.mode == "chasing":
            if self.current_direction == 1:
                self.pixel_y -= 2
            elif self.current_direction == 2:
                self.pixel_x += 2
            elif self.current_direction == 4:
                self.pixel_y += 2
            elif self.current_direction == 8:
                self.pixel_x -= 2
        elif self.mode == "edible":
                pass


class Pacman:
    def __init__(self, TILE_SIZE: int):
        self.next_direction = None
        self.current_direction = None
        self.col_size = 15
        self.row_size = 15
        self.TILE_SIZE = TILE_SIZE
        self.PLAYER_X = 7 * self.TILE_SIZE
        self.PLAYER_Y = 7 * self.TILE_SIZE 
        self.current_col = self.PLAYER_X // self.TILE_SIZE
        self.current_row = self.PLAYER_Y // self.TILE_SIZE
        self.script_dir = Path(__file__).resolve().parent.parent
        self.abs_path_pacman = self.script_dir / "images" / f"pacman.bmp"
        self.pacman = pygame.image.load(self.abs_path_pacman).convert()
        self.pacman = pygame.transform.scale(self.pacman, (self.TILE_SIZE, self.TILE_SIZE))

    def draw_pac(self, window):
        window.blit(self.pacman, (self.PLAYER_X, self.PLAYER_Y))

    def neighbors(self, maze_arr) -> None:
        self.alowed = []
        if self.current_col > 0 and not maze_arr[self.current_row][self.current_col] & 8:
            self.alowed.append(4)
        if self.current_col < self.row_size - 1 and not maze_arr[self.current_row][self.current_col] & 2:
            self.alowed.append(3)
        if self.current_row > 0 and not maze_arr[self.current_row][self.current_col] & 1:
            self.alowed.append(1)
        if self.current_row < self.col_size - 1 and not maze_arr[self.current_row][self.current_col] & 4:
            self.alowed.append(2)

    def update_physics(self) -> None:
        keys = {
            pygame.K_w: 1, pygame.K_UP: 1,
                pygame.K_s: 2, pygame.K_DOWN: 2,
                    pygame.K_d: 3, pygame.K_RIGHT: 3,
                        pygame.K_a: 4, pygame.K_LEFT: 4
              }
        if self.next_direction in keys:
            if self.PLAYER_X % self.TILE_SIZE == 0 and self.PLAYER_Y % self.TILE_SIZE == 0:
                if keys[self.next_direction] in self.alowed:
                    self.current_direction = self.next_direction
                if self.current_direction in keys and keys[self.current_direction] not in self.alowed:
                        self.current_direction = None
        if self.current_direction in keys and keys[self.current_direction] == 1:
            self.PLAYER_Y -= 2
        elif self.current_direction in keys and keys[self.current_direction] == 2:
            self.PLAYER_Y += 2
        elif self.current_direction in keys and keys[self.current_direction] == 3:
            self.PLAYER_X += 2
        elif self.current_direction in keys and keys[self.current_direction] == 4:
            self.PLAYER_X -= 2


class Game:
    def __init__(self):
        self.running = True
        self.TILE_SIZE = 512 // 15
        self.col_size = 15
        self.row_size = 15
        self.GAME_HIGHT = self.TILE_SIZE * self.col_size
        self.GAME_WIDTH = self.TILE_SIZE  * self.row_size
        self.window = pygame.display.set_mode((self.GAME_WIDTH, self.GAME_HIGHT))
        self.maze_arr = MazeGenerator((self.row_size, self.col_size), seed=42).maze
        self.pacman = Pacman(self.TILE_SIZE)
        self.ghosts = [
            Ghosts(0, 0, 0, self.TILE_SIZE, self.maze_arr, self.row_size, self.col_size),
            Ghosts(1, self.col_size - 1, 0, self.TILE_SIZE, self.maze_arr, self.row_size, self.col_size),
            Ghosts(2, 0, self.row_size - 1, self.TILE_SIZE, self.maze_arr, self.row_size, self.col_size),
            Ghosts(3, self.col_size - 1, self.row_size - 1, self.TILE_SIZE, self.maze_arr, self.row_size, self.col_size)
              ]
        self.alowed = None
        self.load_maze_images()
        self.next_direction = None
        self.current_direction = None
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
            self.loaded_images[i] = pygame.image.load(abs_path).convert()

    def run(self) -> None:
        while self.running:
            self.window.fill((0, 0, 0))
            self.draw_maze()
            for ghost in self.ghosts:
                ghost.draw_ghost(self.window)
                ghost.update(self.pacman.current_col, self.pacman.current_row)
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
            pygame.display.update()
            self.clock.tick(60)





