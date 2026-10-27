import pygame
import sys
from pathlib import Path
from mazegenerator.Mazegenerator import MazeGenerator
from Charcacters import Game, Ghosts, Pacman

def main() -> None:
    pygame.init()
    game = Game()
    game.run()
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()