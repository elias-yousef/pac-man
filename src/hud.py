from backgrounds import load_sprite
import pygame
from pathlib import Path
class HUD:
    def __init__(self, screen_w: int) -> None:
        self.height =60
        self.width = screen_w
        self.cuurent_score=0
        self.lives=3
        self.time=120
        self.level=1
        self.BG_COLOR = (54,15,90)#(76, 52, 100)#(112, 41, 99)#(190, 160, 220)
        self.TEXT_COLOR = (255, 242, 204)
        self.CARD_COLOR = (255, 250, 240)
        self.BORDER_COLOR = (112, 41, 99)#(76, 52, 100)


        pygame.font.init()
        #self.font= pygame.font.SysFont("monospace", 22, bold=True)#("Comic Sans MS", 24, bold=True)
        font_path = Path(__file__).resolve().parent.parent / "fonts" / "PressStart2P-Regular.ttf"
        if font_path.exists():
            self.font = pygame.font.Font(str(font_path), 12)
        else:
            self.font = pygame.font.SysFont("monospace", 16, bold=True)  # fallback
 
        image = Path(__file__).resolve().parent.parent / "images" / "bat.jpg"
        self.pic = load_sprite(image, (30, 30))
        image2 = Path(__file__).resolve().parent.parent / "images" / "kittens.jpg"
        self.kitten = load_sprite(image2, (30, 30))
 
    def draw_text(self, screen, text, x, y):
        text_surface = self.font.render(text, False, self.TEXT_COLOR)
        rect = text_surface.get_rect(midleft=(x, self.height // 2))
        screen.blit(text_surface, rect)

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
    def draw_timer(self, screen, seconds):
        screen.blit(self.kitten, (15, 15))
        self.draw_text(screen, f"TIME: {seconds}", 60, 17)
    
    def draw_lives(self, screen, lives):
        self.draw_text(screen, f"LIVES: {lives} ", 280, 17)
        #width = screen.get_width()

        #ghost_x = width - 190

        #screen.blit(self.ghost, (ghost_x, 18))
        #self.draw_text(screen, f"LIVES:{lives}", ghost_x + 22, 17)
    def draw_level(self, screen, level):
        #screen.blit(self.pic, (640, 15))
        #screen.blit(self.pic, (660, 15))
        #screen.blit(self.pic, (680, 15))
        screen.blit(self.kitten, (750, 15))

        self.draw_text(screen, f"LEVEL: {level}", 370, 15)
        

        #text = f"LEVEL: {level}"
        #text_surface = self.font.render(text, True, self.TEXT_COLOR)

        #x = screen.get_width() - text_surface.get_width() - 15
        #y = 17

        #screen.blit(text_surface, (x, y))
    
    def draw_score(self, screen, score):
        self.draw_text(screen, f"SCORE: {score}", 170, 17)
    
    def draw(self, screen, score, lives, level, remaining_time):
        self.draw_BG(screen)
        self.draw_timer(screen, remaining_time)
        self.draw_score(screen, score)
        self.draw_lives(screen, lives)
        self.draw_level(screen, level)

