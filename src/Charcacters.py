import random
from pathlib import Path
from screen import game_over_screen, victory_screen
import pygame
from backgrounds import load_sprite
from highscore import HighscoreManager
from hud import HUD
from mazegenerator import MazeGenerator
from pause import pause

BASE_DIR = Path(__file__).resolve().parent.parent / "images"

# Direction bits (same bits the maze uses for its walls)
NORTH, EAST, SOUTH, WEST = 1, 2, 4, 8
DIRECTION_VECTORS = {
    NORTH: (0, -1),
    EAST: (1, 0),
    SOUTH: (0, 1),
    WEST: (-1, 0),
}
OPPOSITE = {NORTH: SOUTH, SOUTH: NORTH, EAST: WEST, WEST: EAST}
KEY_TO_DIRECTION = {
    pygame.K_w: NORTH, pygame.K_UP: NORTH,
    pygame.K_s: SOUTH, pygame.K_DOWN: SOUTH,
    pygame.K_d: EAST, pygame.K_RIGHT: EAST,
    pygame.K_a: WEST, pygame.K_LEFT: WEST,
}
SPEED = 2  # pixels per frame (must divide TILE_SIZE)


def open_directions(maze_arr, col, row, row_size, col_size) -> list[int]:
    """Return the directions you can leave tile (col, row) through."""
    cell = maze_arr[row][col]
    allowed = []
    if row > 0 and not cell & NORTH:
        allowed.append(NORTH)
    if col < row_size - 1 and not cell & EAST:
        allowed.append(EAST)
    if row < col_size - 1 and not cell & SOUTH:
        allowed.append(SOUTH)
    if col > 0 and not cell & WEST:
        allowed.append(WEST)
    return allowed


class Ghosts:
    def __init__(self, ghost_num: int, x: int, y: int, TILE_SIZE: int,
                 maze_arr, row_size: int, col_size: int) -> None:
        self.start_col = x
        self.start_row = y
        self.col = x
        self.row = y
        self.col_size = col_size
        self.row_size = row_size
        self.maze_arr = maze_arr
        self.TILE_SIZE = TILE_SIZE
        self.pixel_x = x * TILE_SIZE
        self.pixel_y = y * TILE_SIZE
        self.ghost = ghost_num
        self.current_direction = None
        self.mode = "chasing"
        self.allowed = []
        self.distance = 0
        self.image = load_sprite(
        BASE_DIR / f"ghost{ghost_num + 1:02d}.png",
        (TILE_SIZE, TILE_SIZE),
        )
        #image = pygame.image.load(
         #   str(BASE_DIR / f"ghost{ghost_num + 1:02d}.png")
        #).convert_alpha()
       # self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

    def reset(self) -> None:
        self.col = self.start_col
        self.row = self.start_row
        self.pixel_x = self.start_col * self.TILE_SIZE
        self.pixel_y = self.start_row * self.TILE_SIZE
        self.current_direction = None

    def draw_ghost(self, surface) -> None:
        surface.blit(self.image, (self.pixel_x, self.pixel_y))

    def choose_direction(self, player_col: int, player_row: int) -> None:
        """Pick a direction. Only called when exactly on a tile."""
        chase_range = {0: 0, 1: 6, 2: 8, 3: 4}[self.ghost]
        if not self.allowed:
            return

        opposite = OPPOSITE.get(self.current_direction)
        candidates = [d for d in self.allowed if d != opposite] or self.allowed

        if self.distance > chase_range:
            self.current_direction = random.choice(candidates)
        else:
            best = {}
            for d in candidates:
                dc, dr = DIRECTION_VECTORS[d]
                best[d] = (abs(self.col + dc - player_col)
                           + abs(self.row + dr - player_row))
            self.current_direction = min(best, key=best.get)

    def update(self, player_col: int, player_row: int) -> None:
        self.col = self.pixel_x // self.TILE_SIZE
        self.row = self.pixel_y // self.TILE_SIZE
        self.distance = abs(self.col - player_col) + abs(self.row - player_row)

        aligned = (self.pixel_x % self.TILE_SIZE == 0
                   and self.pixel_y % self.TILE_SIZE == 0)
        if aligned:
            self.allowed = open_directions(
                self.maze_arr, self.col, self.row,
                self.row_size, self.col_size)
            self.choose_direction(player_col, player_row)

        if self.mode == "chasing" and self.current_direction is not None:
            dc, dr = DIRECTION_VECTORS[self.current_direction]
            self.pixel_x += dc * SPEED
            self.pixel_y += dr * SPEED


class Pacman:
    def __init__(self, TILE_SIZE: int, lives: int,
                 row_size: int, col_size: int) -> None:
        self.lives = lives
        self.TILE_SIZE = TILE_SIZE
        self.row_size = row_size
        self.col_size = col_size
        self.start_col = row_size // 2
        self.start_row = (col_size // 2) + 2
        self.PLAYER_X = self.start_col * TILE_SIZE
        self.PLAYER_Y = self.start_row * TILE_SIZE
        self.current_col = self.start_col
        self.current_row = self.start_row
        self.next_direction = None      # remembered key press
        self.current_direction = None   # NORTH/EAST/SOUTH/WEST or None
        self.allowed = []
        self.image = load_sprite(
            BASE_DIR / "pacman.png",
            (TILE_SIZE, TILE_SIZE),
        )
        #image = pygame.image.load(str(BASE_DIR / "pacman.png")).convert_alpha()
        #self.image = pygame.transform.scale(image, (TILE_SIZE, TILE_SIZE))

    def draw_pac(self, surface) -> None:
        surface.blit(self.image, (self.PLAYER_X, self.PLAYER_Y))

    def reset_position(self) -> None:
        self.PLAYER_X = self.start_col * self.TILE_SIZE
        self.PLAYER_Y = self.start_row * self.TILE_SIZE
        self.current_direction = None
        self.next_direction = None

    def update_physics(self, maze_arr) -> None:
        self.current_col = self.PLAYER_X // self.TILE_SIZE
        self.current_row = self.PLAYER_Y // self.TILE_SIZE

        aligned = (self.PLAYER_X % self.TILE_SIZE == 0
                   and self.PLAYER_Y % self.TILE_SIZE == 0)
        if aligned:
            self.allowed = open_directions(
                maze_arr, self.current_col, self.current_row,
                self.row_size, self.col_size)
            wanted = KEY_TO_DIRECTION.get(self.next_direction)
            if wanted in self.allowed:
                self.current_direction = wanted
            elif self.current_direction not in self.allowed:
                self.current_direction = None

        if self.current_direction is not None:
            dc, dr = DIRECTION_VECTORS[self.current_direction]
            self.PLAYER_X += dc * SPEED
            self.PLAYER_Y += dr * SPEED


class Game:
    HUD_HEIGHT = 60

    def __init__(self, config: dict) -> None:
        self.config = config
        self.running = True
        self.lives = config["lives"]
        self.pacgum_points = config["points_per_pacgum"]
        self.level_max_time = config["level_max_time"]
        self.seed = config["seed"]
        self.pacgum = 40
        self.super_gums = 4
        self.score = 0
        self.level = 1
        self.max_level = 10
        self.remaining_time = self.level_max_time
        self.won = False
        self.row_size = config["levels"]["width"]
        self.col_size = config["levels"]["height"]
        self.TILE_SIZE = 40
        self.GAME_WIDTH = self.TILE_SIZE * self.row_size
        self.GAME_HEIGHT = self.TILE_SIZE * self.col_size

        # window = HUD strip on top + board below
        self.window = pygame.display.set_mode(
            (self.GAME_WIDTH, self.GAME_HEIGHT + self.HUD_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        # everything in the maze is drawn on this surface in maze coordinates
        self.board = pygame.Surface((self.GAME_WIDTH, self.GAME_HEIGHT))

        self.maze_arr = MazeGenerator(
            (self.row_size, self.col_size), seed=self.seed).maze
        self.pacman = Pacman(
            self.TILE_SIZE, self.lives, self.row_size, self.col_size)
        self.ghosts = self.make_ghosts()

        self.hud = HUD(self.GAME_WIDTH)
        self.highscores = HighscoreManager(
            str(Path(__file__).resolve().parent / "score.json"))
        self.highscores.load_scores()

        self.load_maze_images()
        self.supergum_image = load_sprite(BASE_DIR / "pacgums.png", (32, 32))
        #strawberry = pygame.image.load(
         #   str(BASE_DIR / "pacgum.png")).convert_alpha()
        #self.supergum_image = pygame.transform.scale(strawberry, (30, 30))

        self.clock = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

    # ---------- setup helpers ----------
    def make_ghosts(self) -> list:
        args = (self.TILE_SIZE, self.maze_arr, self.row_size, self.col_size)
        last_col, last_row = self.row_size - 1, self.col_size - 1
        return [
            Ghosts(0, 0, 0, *args),
            Ghosts(1, last_col, 0, *args),
            Ghosts(2, 0, last_row, *args),
            Ghosts(3, last_col, last_row, *args),
        ]

    def load_maze_images(self) -> None:
        self.loaded_images = {}
        for i in range(1, 16):
            path = BASE_DIR / f"{i}.png"
            if not path.exists():
                raise FileNotFoundError(f"Maze image not found: {path}")
            img = pygame.image.load(str(path)).convert()
            self.loaded_images[i] = pygame.transform.scale(
                img, (self.TILE_SIZE, self.TILE_SIZE))

    def generate_maze(self) -> None:
        self.seed = random.random()
        self.maze_arr = MazeGenerator(
            (self.row_size, self.col_size),
            perfect=False, seed=self.seed).maze
        for ghost in self.ghosts:
            ghost.maze_arr = self.maze_arr
        self.reset_positions()

    def reset_positions(self) -> None:
        self.pacman.reset_position()
        for ghost in self.ghosts:
            ghost.reset()

    # ---------- game logic ----------
    def check_level_completion(self) -> None:
        if self.pacgum == 0 and self.super_gums == 0:
            if self.level < self.max_level:
                self.level += 1
                self.generate_maze()
            else:
                self.won = True

    def check_ghost_collisions(self) -> None:
        for ghost in self.ghosts:
            dx = self.pacman.PLAYER_X - ghost.pixel_x
            dy = self.pacman.PLAYER_Y - ghost.pixel_y
            if (dx ** 2 + dy ** 2) ** 0.5 < self.TILE_SIZE // 2:
                self.pacman.lives -= 1
                self.reset_positions()
                return

    def update(self) -> None:
        elapsed = (pygame.time.get_ticks() - self.start_time) // 1000
        self.remaining_time = max(0, self.level_max_time - elapsed)

        self.check_level_completion()
        self.pacman.update_physics(self.maze_arr)
        for ghost in self.ghosts:
            ghost.update(self.pacman.current_col, self.pacman.current_row)
        self.check_ghost_collisions()

    # ---------- drawing ----------
    def draw_maze(self) -> None:
        for row_index, row in enumerate(self.maze_arr):
            for col_index, cell_value in enumerate(row):
                if cell_value > 0:
                    self.board.blit(
                        self.loaded_images[cell_value],
                        (col_index * self.TILE_SIZE,
                         row_index * self.TILE_SIZE))

    def draw_gums(self) -> None:
        w, h = self.GAME_WIDTH, self.GAME_HEIGHT
        for pos in [(6, 6), (w - 38, 6), (6, h - 38), (w - 38, h - 38)]:
            self.board.blit(self.supergum_image, pos)

    def draw_game(self) -> None:
        self.window.fill((0, 0, 0))
        self.board.fill((0, 0, 0))
        self.draw_maze()
        self.draw_gums()
        self.pacman.draw_pac(self.board)
        for ghost in self.ghosts:
            ghost.draw_ghost(self.board)

        self.window.blit(self.board, (0, self.HUD_HEIGHT))
        self.hud.draw(
            self.window,
            score=self.score,
            lives=self.pacman.lives,
            level=self.level,
            remaining_time=self.remaining_time,
        )

    # ---------- main loop ----------
    def run(self) -> str:
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.draw_game()
                        pygame.display.flip()
                        paused_at = pygame.time.get_ticks()
                        action = pause(self.window)
                        # don't let paused time count against the player
                        self.start_time += pygame.time.get_ticks() - paused_at
                        if action == "menu":
                            return "menu"
                    else:
                        self.pacman.next_direction = event.key

            self.update()
            self.draw_game()
            pygame.display.flip()
            if self.pacman.lives <= 0 or self.remaining_time <= 0:
                return game_over_screen(self.window, self.score, self.highscores)

            if self.won:
                return victory_screen(self.window, self.score, self.highscores)
            self.clock.tick(60)


