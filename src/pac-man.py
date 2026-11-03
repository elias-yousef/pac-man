import sys
from pathlib import Path
import pygame

from parser import ConfigError, parser
from Charcacters import Game, Ghosts, Pacman
from mazegenerator.Mazegenerator import MazeGenerator


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python3 pac-man.py <config_file.json>", file=sys.stderr)
        sys.exit(1)

    config_file = sys.argv[1]

    try:
        config = parser(config_file)
    except ConfigError as err:
        print(f"Configuration Error: {err}", file=sys.stderr)
        sys.exit(1)

    pygame.init()
    game = Game(config=config)
    game.run()
    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    main()