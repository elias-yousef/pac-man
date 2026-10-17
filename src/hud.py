import pygame
from pathlib import Path
"""
an example of how i could use the HUD inisde the game to represent the data bar or whatever its name :)
   

   while running:
    window.fill((0, 0, 0))

    draw_maze(window, maze_arr, TILE_SIZE, loaded_images)

    # Handle events
    # Update game state

    window.blit(pacman, (PLAYER_X, PLAYER_Y))

    draw_hud(
        window,
        score,
        lives,
        level,
        remaining_time
    )

    pygame.display.update()
    clock.tick(60)
"""
   
BG_COLOR = (255, 242, 204)
TEXT_COLOR = (76, 52, 100)
CARD_COLOR = (255, 250, 240)
BORDER_COLOR = (190, 160, 220)
class HUD:
    def __init__(self, screen_w: int) -> None:
        self.height =60
        self.width = screen_w
        self.cuurent_score=0
        self.lives=3
        self.time=120
        self.level=1
        self.BG_COLOR = (190, 160, 220)
        self.TEXT_COLOR = (255, 242, 204)
        self.CARD_COLOR = (255, 250, 240)
        self.BORDER_COLOR = (76, 52, 100)


        pygame.font.init()
        self.font= pygame.font.SysFont("arial", 17, bold=True)#("Comic Sans MS", 24, bold=True)
        image_path = Path(__file__).resolve().parent / "pacman.png"

        self.ghost = pygame.image.load(image_path).convert_alpha()
        self.ghost = pygame.transform.scale(self.ghost, (16, 16))


    def draw_BG(self, screen):
        width = screen.get_width()
        pygame.draw.rect(
            screen,
            self.BG_COLOR,
            (0, 0, width, self.height)
        )
        pygame.draw.rect(
            screen,
            self.BORDER_COLOR,
            (0, 0, width, self.height),
            4
        )
    def draw_text(self, screen, text, x, y):
        text_surface = self.font.render(text, True, self.TEXT_COLOR)
        screen.blit(text_surface, (x, y))
    
    def draw_timer(self, screen, seconds):
        self.draw_text(screen, f"TIME: {seconds}", 15, 17)
    
    def draw_lives(self, screen, lives):
        screen.blit(self.ghost, (320, 18))
        self.draw_text(screen, f"LIVES: {lives} ", 260, 17)
        #width = screen.get_width()

        #ghost_x = width - 190

        #screen.blit(self.ghost, (ghost_x, 18))
        #self.draw_text(screen, f"LIVES:{lives}", ghost_x + 22, 17)
    def draw_level(self, screen, level):
        self.draw_text(screen, f"LEVEL: {level}", 390, 17)
        #text = f"LEVEL: {level}"
        #text_surface = self.font.render(text, True, self.TEXT_COLOR)

        #x = screen.get_width() - text_surface.get_width() - 15
        #y = 17

        #screen.blit(text_surface, (x, y))
    
    def draw_score(self, screen, score):
        self.draw_text(screen, f"SCORE: {score}", 110, 17)
    
    def draw(self, screen, score, lives, level, remaining_time):
        self.draw_BG(screen)
        self.draw_timer(screen, remaining_time)
        self.draw_score(screen, score)
        self.draw_lives(screen, lives)
        self.draw_level(screen, level)
'''
    class HUD:
    def __init__(self) -> None:
        self.height = 60

        self.BG_COLOR = (190, 160, 220)
        self.TEXT_COLOR = (76, 52, 100)
        self.CARD_COLOR = (255, 250, 240)
        self.BORDER_COLOR = (255, 242, 204)

        pygame.font.init()
        self.font = pygame.font.SysFont("arial", 17, bold=True)

        image_path = Path(__file__).resolve().parent / "pacman.png"
        self.ghost = pygame.image.load(image_path).convert_alpha()
        self.ghost = pygame.transform.scale(self.ghost, (16, 16))

    def render(self, text):
        return self.font.render(text, True, self.TEXT_COLOR)

    def draw_BG(self, screen):
        width = screen.get_width()
        bar = pygame.Rect(0, 0, width, self.height)
        pygame.draw.rect(screen, self.BG_COLOR, bar)
        pygame.draw.rect(screen, self.BORDER_COLOR, bar, 4)

    def draw(self, screen, seconds, score, lives, level):
        width = screen.get_width()

        self.draw_BG(screen)

        time_surf = self.render(f"TIME: {seconds}")
        level_surf = self.render(f"LEVEL: {level}")
        score_surf = self.render(f"SCORE: {score}")
        lives_surf = self.render(f"{lives}-LIVES!")
        text_y = (self.height - self.font.get_height()) // 2
        ghost_y = (self.height - self.ghost.get_height()) // 2

       
        screen.blit(time_surf, (15, text_y))

      
        screen.blit(level_surf, (width - level_surf.get_width() - 15, text_y))

        gap = 40
        icon_gap = 4
        ghost_w = self.ghost.get_width()

        total_w = (
            score_surf.get_width() + gap
            + ghost_w + icon_gap
            + lives_surf.get_width()
        )
        x = (width - total_w) // 2

        screen.blit(score_surf, (x, text_y))
        x += score_surf.get_width() + gap

        screen.blit(self.ghost, (x, ghost_y))
        x += ghost_w + icon_gap

        screen.blit(lives_surf, (x, text_y))
'''
