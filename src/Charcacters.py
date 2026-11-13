import pygame
from mazegenerator import MazeGenerator
from pathlib import Path
from hud import HUD
from pause import pause
from menu import main_menu
from screens import game_over_screen, victory_screen
from highscore import HighscoreManager

class Game:
    def __init__(self):
        self.running = True
        self.TILE_SIZE = 512 // 15
        self.col_size = 15
        self.row_size = 15
        self.HUD_HEIGHT = 60
        self.GAME_HIGHT = self.TILE_SIZE * self.col_size
        self.GAME_WIDTH = self.TILE_SIZE  * self.row_size
        
        self.PLAYER_X = 7 * self.TILE_SIZE 
        self.PLAYER_Y = 7 * self.TILE_SIZE 
        
        self.current_col = self.PLAYER_X // self.TILE_SIZE
        self.current_row = self.PLAYER_Y // self.TILE_SIZE
        
        self.window = pygame.display.set_mode((self.GAME_WIDTH, self.GAME_HIGHT+ self.HUD_HEIGHT))
        self.maze_arr = MazeGenerator((self.row_size, self.col_size), seed=42).maze
        
        self.alowed = None
        self.load_maze_images()
        
        self.hud = HUD(self.GAME_WIDTH)
        # NEW game information 
        self.score = 0
        self.lives = 3
        self.highscores = HighscoreManager(
            str(Path(__file__).resolve().parent / "score.json")
        )

        self.highscores.load_scores()

        self.won = False
        self.level = 1
        self.remaining_time = 120

        # NEW timer tracking haha
        self.start_time = pygame.time.get_ticks()
        self.next_direction = None
        self.current_direction = None
        
        self.pacman = pygame.image.load((Path("/mnt/c/Users/leen9/leen42/pacman/lilyver/src/pacman.png"))).convert()
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
                    y_pixel = row_index * self.TILE_SIZE + self.HUD_HEIGHT
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
        1: "/mnt/c/Users/leen9/leen42/pacman/lilyver/src/images/1.png",
        2: "/mnt/c/Users/leen9/leen42/pacman/lilyver/src/images/2.png",
        3: "/mnt/c/Users/leen9/leen42/pacman/lilyver/src/images/3.png",
        4: "/mnt/c/Users/leen9/leen42/pacman/lilyver/src/images/4.png",
        5: "/mnt/c/Users/leen9/leen42/pacman/lilyver/src/images/5.png",
        6: "/mnt/c/Users/leen9/leen42/pacman/lilyver/src/images/6.png",
        7: "/mnt/c/Users/leen9/leen42/pacman/lilyver/src/images/7.png",
        8: "/mnt/c/Users/leen9/leen42/pacman/lilyver/src/images/8.png",
        9: "/mnt/c/Users/leen9/leen42/pacman/lilyver/src/images/9.png",
        10: "/mnt/c/Users/leen9/leen42/pacman/lilyver/src/images/10.png",
        11: "/mnt/c/Users/leen9/leen42/pacman/lilyver/src/images/11.png",
        12: "/mnt/c/Users/leen9/leen42/pacman/lilyver/src/images/12.png",
        13: "/mnt/c/Users/leen9/leen42/pacman/lilyver/src/images/13.png",
        14: "/mnt/c/Users/leen9/leen42/pacman/lilyver/src/images/14.png",
        15: "/mnt/c/Users/leen9/leen42/pacman/lilyver/src/images/15.png",
        }

        self.loaded_images = {}
        for cell_value, path in cell_images.items():
            self.loaded_images[cell_value] = pygame.image.load(Path(path)).convert()

    def draw_hud(self) -> None:
        elapsed_seconds = (
            pygame.time.get_ticks() - self.start_time
        ) // 1000

        self.remaining_time = max(0, 120 - elapsed_seconds)

        self.hud.draw(
            self.window,
            score=self.score,
            lives=self.lives,
            level=self.level,
            remaining_time=self.remaining_time
        )

    def draw_game(self) -> None:
        self.window.fill((0, 0, 0))
        self.draw_hud()
        self.draw_maze()

        self.window.blit(
            self.pacman,
            (
                self.PLAYER_X,
                self.PLAYER_Y + self.HUD_HEIGHT
            )
        )
    def run(self) -> None:
        while self.running:
            self.window.fill((0, 0, 0))
            self.draw_maze()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        # NEW: Draw the complete game before pausing
                        self.draw_game()
                        pygame.display.flip()

                        # NEW: Call your existing pause screen
                        action = pause(self.window)

                        if action == "menu":
                            main_menu()
                            self.running = False
                    else:
                        self.next_direction = event.key

            self.current_col = self.PLAYER_X // self.TILE_SIZE
            self.current_row = self.PLAYER_Y // self.TILE_SIZE
            self.neighbors()
            self.update_physics()
            self.draw_game()
            #self.window.blit(self.pacman, (self.PLAYER_X, self.PLAYER_Y + self.HUD_HEIGHT))
            pygame.display.flip()
            if self.lives <= 0 or self.remaining_time <= 0:

                action = game_over_screen(
                    self.window,
                    self.score,
                    self.highscores
                )

                self.running = False

                if action == "quit":
                    pygame.quit()
                    return

            return

        if self.won:

            action = victory_screen(
                self.window,
                self.score,
                self.highscores
            )

            self.running = False

            if action == "quit":
                pygame.quit()
                return

            return
        self.clock.tick(60)


class Pacman:
    def __init__(self):
        pass


class Gosts:
    def __init__(self):
        pass

