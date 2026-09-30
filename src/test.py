import pygame
import sys

pygame.init()

# 1. Set initial dimensions and add the RESIZABLE flag
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Dynamic Resizable Window")

clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # 2. Listen for the window resize event
        elif event.type == pygame.VIDEORESIZE:
            # Update the width and height variables with the new dimensions
            WIDTH, HEIGHT = event.w, event.h
            # Apply the new size to the screen surface
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    # 3. Game Logic (Use WIDTH and HEIGHT relative coordinates)
    # Example: Keep a rectangle perfectly centered regardless of window size
    rect_width, rect_height = 100, 100
    rect_x = (WIDTH // 2) - (rect_width // 2)
    rect_y = (HEIGHT // 2) - (rect_height // 2)

    # 4. Drawing
    screen.fill((50, 50, 50)) 
    
    # Draw the centered rectangle
    pygame.draw.rect(screen, (0, 255, 128), (rect_x, rect_y, rect_width, rect_height))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
