import pygame
from mazegenerator import MazeGenerator
from pathlib import Path

class Game:
    def __init__(self):
        self.running = True
        self.TILE_SIZE = 512 // 15
        self.col_size = 15
        self.row_size = 15
        self.GAME_HIGHT = self.TILE_SIZE * self.col_size
        self.GAME_WIDTH = self.TILE_SIZE  * self.row_size
        self.PLAYER_X = 7 * self.TILE_SIZE 
        self.PLAYER_Y = 7 * self.TILE_SIZE 
        self.current_col = self.PLAYER_X // self.TILE_SIZE
        self.current_row = self.PLAYER_Y // self.TILE_SIZE
        self.window = pygame.display.set_mode((self.GAME_WIDTH, self.GAME_HIGHT))
        self.maze_arr = MazeGenerator((self.row_size, self.col_size), seed=42).maze
        self.alowed = None
        self.load_maze_images()
        self.next_direction = None
        self.current_direction = None
        self.pacman = pygame.image.load((Path("/Users/elias/pacman/images/pacman1.bmp"))).convert()
        self.pacman = pygame.transform.scale(self.pacman, (self.TILE_SIZE, self.TILE_SIZE))
        self.clock = pygame.time.Clock()

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

    def draw_maze(self) -> None: 
        for row_index, row in enumerate(self.maze_arr):
            for col_index, cell_value in enumerate(row):
                if cell_value > 0:
                    x_pixel = col_index * self.TILE_SIZE
                    y_pixel = row_index * self.TILE_SIZE
                    self.window.blit(self.loaded_images[cell_value], (x_pixel, y_pixel))

    def neighbors(self) -> None:
        self.alowed = []
        if self.current_col > 0 and not self.maze_arr[self.current_row][self.current_col] & 8:
            self.alowed.append(4)
        if self.current_col < self.row_size - 1 and not self.maze_arr[self.current_row][self.current_col] & 2:
            self.alowed.append(3)
        if self.current_row > 0 and not self.maze_arr[self.current_row][self.current_col] & 1:
            self.alowed.append(1)
        if self.current_row < self.col_size - 1 and not self.maze_arr[self.current_row][self.current_col] & 4:
            self.alowed.append(2)

    def load_maze_images(self) -> None:
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
        self.loaded_images = {}
        for cell_value, path in cell_images.items():
            self.loaded_images[cell_value] = pygame.image.load(Path(path)).convert()

    def run(self) -> None:
        while self.running:
            self.window.fill((0, 0, 0))
            self.draw_maze()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.next_direction = event.key
            self.current_col = self.PLAYER_X // self.TILE_SIZE
            self.current_row = self.PLAYER_Y // self.TILE_SIZE
            self.neighbors()
            self.update_physics()
            self.window.blit(self.pacman, (self.PLAYER_X, self.PLAYER_Y))
            pygame.display.update()
            self.clock.tick(60)


class Pacman:
    def __init__(self):
        pass


class Gosts:
    def __init__(self):
        pass

