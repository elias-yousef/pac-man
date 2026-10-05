import pygame

class GAME:
    def __init__(
            self, TILE_SIZE, col_size, row_size, window
            ):
        self.TILE_SIZE = TILE_SIZE
        self.col_size = col_size
        self.row_size = row_size
        self.GAME_HIGHT = TILE_SIZE * col_size
        self.GAME_WIDTH = TILE_SIZE * row_size
        self.PLAYER_X = 7 * TILE_SIZE
        self.PLAYER_Y = 7 * TILE_SIZE
        self.window = pygame.display.set_mode((self.GAME_WIDTH, self.GAME_HIGHT))

class PACMAN:
    def __init__(self):
        pass


class GOSTS:
    def __init__(self):
        pass

