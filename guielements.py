import common as cm
import sys
import pygame

from pydoc import text
from basechessgame import playgame
import pygame
import pygame.freetype
from pygame.locals import *
from pygame.sprite import Sprite
from pygame.rect import Rect
import sys

pygame.init()


def create_text_surface(text, font_size, txt_rgb, bg_rgb):
    font = pygame.freetype.SysFont("Arial", font_size)
    surface, _ = font.render(text=text, fgcolor=txt_rgb, bgcolor=bg_rgb)
    return surface

#turns text into list of seperate strings for multiline elements
def create_multiline_text(text, font, x, y):
    pos_x = x
    pos_y = y
    pos = pos_x, pos_y
    out = []
    for t in text:
        out.append(font.render(t, True, cm.BLACK))
    return out, pos


# class for non-interactable UI elements
class Element(Sprite):
    def __init__(self, img, pos):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    #scales image of element, factor is a tuple
    def scale(self, x_factor, y_factor):
        pygame.transform.scale(self.image, (x_factor,y_factor))

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# class for interactable elements that have text
class button(Sprite):
    def __init__(self, pos, text, font_size, txt_col, bg_col, bg_hover):
        self.selected = False

        unselected_img = create_text_surface(text, font_size, txt_col, bg_col)
        highlighted_img = create_text_surface(text, font_size * 1.3, txt_col, bg_hover)

        self.images = [unselected_img, highlighted_img]
        self.rects = [unselected_img.get_rect(center=pos), highlighted_img.get_rect(center=pos)]

        super().__init__()

    @property
    def img(self):
        return self.images[1] if self.selected else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.selected else self.rects[0]

    # selects different button images depending if the mouse is hovered over it
    def moused_over(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.selected = True
        else:
            self.selected = False

    def draw(self, surface):
        surface.blit(self.img, self.rect)