from mazegenerator import MazeGenerator
import pygame
import sys
import math


def draw_maze():
    maze_size_x = 15
    maze_size_y = 15
    Maze = MazeGenerator(size=(maze_size_x, maze_size_y), seed=42)
    GAME_HIGHT = 512
    GAME_WIDTH= 512
    window = pygame.display.set_mode((GAME_WIDTH, GAME_HIGHT), pygame.RESIZABLE)
    pygame.display.set_caption('image')

    image_1 = pygame.image.load("images/1.png").convert()
    image_2 = pygame.image.load("images/2.png").convert()
    image_3 = pygame.image.load("images/3.png").convert()
    image_4 = pygame.image.load("images/4.png").convert()
    image_5 = pygame.image.load("images/5.png").convert()
    image_6 = pygame.image.load("images/6.png").convert()
    image_7 = pygame.image.load("images/7.png").convert()
    image_8 = pygame.image.load("images/8.png").convert()
    image_9 = pygame.image.load("images/9.png").convert()
    image_10 = pygame.image.load("images/10.png").convert()
    image_11 = pygame.image.load("images/11.png").convert()
    image_12 = pygame.image.load("images/12.png").convert()
    image_13 = pygame.image.load("images/13.png").convert()
    image_14 = pygame.image.load("images/14.png").convert()
    image_15 = pygame.image.load("images/15.png").convert()

    x_axis = 0
    y_axis = 0
    clock = pygame.time.Clock()
    arr = Maze.maze
    for row in arr:
        for element in row:
            if math.isclose(x_axis, GAME_WIDTH, abs_tol=5):
                print("==")
                x_axis = 0
            if element == 1:
                window.blit(image_1, (x_axis, y_axis))
            elif element == 2:
                window.blit(image_2, (x_axis, y_axis))
            elif element == 3:
                window.blit(image_3, (x_axis, y_axis))
            elif element == 4:
                window.blit(image_4, (x_axis, y_axis))
            elif element == 5:
                window.blit(image_5, (x_axis, y_axis))
            elif element == 6:
                window.blit(image_6, (x_axis, y_axis))
            elif element == 7:
                window.blit(image_7, (x_axis, y_axis))
            elif element == 8:
                window.blit(image_8, (x_axis, y_axis))
            elif element == 9:
                window.blit(image_9, (x_axis, y_axis))
            elif element == 10:
                window.blit(image_10, (x_axis, y_axis))
            elif element == 11:
                window.blit(image_11, (x_axis, y_axis))
            elif element == 12:
                window.blit(image_12, (x_axis, y_axis))
            elif element == 13:
                window.blit(image_13, (x_axis, y_axis))
            elif element == 14:
                window.blit(image_14, (x_axis, y_axis))
            elif element == 15:
                window.blit(image_15, (x_axis, y_axis))
            x_axis += GAME_WIDTH // maze_size_x
            print(f"x:{x_axis}")
            pygame.display.update()
            clock.tick(60)
        y_axis += GAME_HIGHT // maze_size_y
        print(f"y{y_axis}")

    

draw_maze()