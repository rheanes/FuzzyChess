from pydoc import text
import pygame
import pygame.freetype
from pygame.locals import *
from pygame.sprite import Sprite
from pygame.rect import Rect
import sys

pygame.init()
DISP_WIDTH = 800
DISP_HEIGHT = 800

WHITE = (255, 255, 255)
BLACK = (0, 0 ,0)
RED = (255, 0 ,0)
BROWN = (222, 184, 135)
LIGHT_GRAY = (211, 211, 211)



def create_text_surface(text, font_size, txt_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Arial", font_size)
    surface, _ = font.render(text=text, fgcolor = txt_rgb, bgcolor = bg_rgb)
    return surface
#class for non-interactable UI elements
class Element(Sprite):
    def __init__(self, img, pos):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.center = pos
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

#class for interactable elements that have text
class button(Sprite):
    def __init__(self, pos, text, font_size, txt_col, bg_col):
        self.mouse_over = False

        unselected_img = create_text_surface(text, font_size, txt_col, bg_col)
        highlighted_img = create_text_surface(text, font_size * 1.3, txt_col, bg_col)

        self.images = [unselected_img, highlighted_img]
        self.rects = [unselected_img.get_rect(center=pos), highlighted_img.get_rect(center=pos)]

        super().__init__()
    
    
    @property
    def img(self):
        return self.images[1] if self.mouse_over else self.images[0]
    @property
    def rect(self):
        return self.rects[1] if self.mouse_over else self.rects[0]
        
    #selects different button images depending if the mouse is hovered over it
    def moused_over(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.mouse_over = True
        else:
            self.mouse_over = False
    
    def draw(self, surface):
        surface.blit(self.img, self.rect)


def main():
    display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
    pygame.display.set_caption("Start Screen")
    FPS = 30
    Frames = pygame.time.Clock()
    b_knight = Element("./Images/black_knight.png", (300,400))
    pygame.transform.scale(b_knight.image, (400, 100))
    play_button = button(pos=(600,300), font_size = 50, txt_col=BLACK, bg_col=LIGHT_GRAY, text = "Play")
    rules_button = button(pos=(600,400), font_size= 50, txt_col= BLACK, bg_col= BROWN, text ="Rules")
    quit_button = button(pos=(600, 500), font_size= 50, txt_col=BLACK, bg_col=RED, text="Quit Game")

    while True:
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        display.fill(WHITE)
        b_knight.draw(display)
        play_button.update(pygame.mouse.get_pos())
        play_button.draw(display)
        rules_button.update(pygame.mouse.get_pos())
        rules_button.draw(display)
        quit_button.update(pygame.mouse.get_pos())
        quit_button.draw(display)

        pygame.display.update()
        Frames.tick(FPS)



if __name__ == "__main__":
    main()




