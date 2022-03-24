from common import *
from enum import Enum
import sys
import pygame

from pydoc import text
import pygame
import pygame.freetype
from pygame.locals import *
from pygame.sprite import Sprite
from pygame.rect import Rect
import sys

pygame.init()

def create_text_surface(text, font_size, txt_rgb, bg_rgb):
    font = pygame.freetype.SysFont(fonttype, font_size)
    surface, _ = font.render(text=text, fgcolor=txt_rgb, bgcolor=bg_rgb)
    return surface

#turns text into list of seperate strings for multiline elements
def create_multiline_text(text, font, x, y):
    pos_x = x
    pos_y = y
    pos = pos_x, pos_y
    out = []
    for t in text:
        out.append(rulesfont.render(t, True, BLACK))
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
    def __init__(self, pos, text, font_size, txt_col, bg_col, bg_hover, action=None):
        self.action = action
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
    def moused_over(self, mouse_pos, mouse_down):
        if self.rect.collidepoint(mouse_pos):
            self.selected = True
            if mouse_down:
                return self.action
        else:
            self.selected = False

    def draw(self, surface):
        surface.blit(self.img, self.rect)


class GameState(Enum):
    Quit = -1
    Home = 0
    Play = 1
    Escape = 2
    Load1 = 4
    Load2 = 5
    Load3 = 6
    Save1 = 7
    Save2 = 8
    Save3 = 9
    Delegate = 11
    EndTurn = 12
    Win = 13
    Loss = 14
    Rules = 20
    HowTo = 21
    Pieces = 22
    Pawn = 31
    Rook = 32
    Knight = 33
    Queen = 34
    Bishop = 35
    King = 36





# ActionCount Text
class Action_Counttxt(Sprite):
    def __init__(self, pos, text, font_size, txt_col, bg_col, bg_hover, action=None):
        self.action = action
        # self.selected = False
        unselected_img = create_text_surface(text, font_size, txt_col, bg_col)
        # highlighted_img = create_text_surface(text, font_size * 1.3, txt_col, bg_hover)

        self.images = unselected_img
        self.rects = unselected_img.get_rect(center=pos)
        super().__init__()

    @property
    def img(self):
        return self.images

    @property
    def rect(self):
        return self.rects

    def moused_over(self, mouse_pos, mouse_down):
        if self.rect.collidepoint(mouse_pos):
            self.selected = False
            # if mouse_down:
            # return self.action

    #  else:
    #  self.selected = False

    def draw(self, surface):
        surface.blit(self.img, self.rect)


# Current Turn Text
class WhosTurn(Sprite):
    def __init__(self, pos, text, font_size, txt_col, bg_col, bg_hover, action=None):
        self.action = action
        # self.selected = False
        unselected_img = create_text_surface(text, font_size, txt_col, bg_col)
        # highlighted_img = create_text_surface(text, font_size * 1.3, txt_col, bg_hover)

        self.images = unselected_img
        self.rects = unselected_img.get_rect(center=pos)
        super().__init__()

    @property
    def img(self):
        return self.images

    @property
    def rect(self):
        return self.rects

    def moused_over(self, mouse_pos, mouse_down):
        if self.rect.collidepoint(mouse_pos):
            self.selected = False
            # if mouse_down:
            # return self.action

    #  else:
    #  self.selected = False

    def draw(self, surface):
        surface.blit(self.img, self.rect)

    #BonePile
class BoneP(Sprite):
    def __init__(self, pos, text, font_size, txt_col, bg_col, bg_hover, action=None):
        self.action = action
        self.selected = False
        # self.remain_selected = False
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
    def moused_over(self, mouse_pos, mouse_down):
        if self.rect.collidepoint(mouse_pos):
            self.selected = False


    def draw(self, surface):
        surface.blit(self.img, self.rect)