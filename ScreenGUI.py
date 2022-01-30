import common as cm
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
    font = pygame.freetype.SysFont("Arial", font_size)
    surface, _ = font.render(text=text, fgcolor=txt_rgb, bgcolor=bg_rgb)
    return surface


# class for non-interactable UI elements
class Element(Sprite):
    def __init__(self, img, pos):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.center = pos

    #scales image of element, factor is a tuple
    def scale(self, factor):
        return pygame.transform.scale(self.image, factor)

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# class for interactable elements that have text
class button(Sprite):
    def __init__(self, pos, text, font_size, txt_col, bg_col):
        self.selected = False

        unselected_img = create_text_surface(text, font_size, txt_col, bg_col)
        highlighted_img = create_text_surface(text, font_size * 1.3, txt_col, bg_col)

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

clock = pygame.time.Clock()
screen = pygame.display.set_mode((cm.WIDTH, cm.WIDTH))
pygame.display.set_caption('Medieval Fuzzy Logic Chess')
def start_menu():
    b_knight = Element("./Images/black_knight.png", (300, 400))
    b_knight.scale((cm.WIDTH / 2, cm.HEIGHT / 3))
    play_button = button(pos=(600, 300), font_size=50, txt_col=cm.BLACK, bg_col=cm.LIGHT_GRAY, text="Play")
    rules_button = button(pos=(600, 400), font_size=50, txt_col=cm.BLACK, bg_col=cm.BROWN, text="Rules")
    quit_button = button(pos=(600, 500), font_size=50, txt_col=cm.BLACK, bg_col=cm.RED, text="Quit Game")
    while True:

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if quit_button.selected:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if rules_button.selected:
                    rulespage()
        screen.fill(cm.WHITE)
        b_knight.draw(screen)
        play_button.moused_over(pygame.mouse.get_pos())
        play_button.draw(screen)
        rules_button.moused_over(pygame.mouse.get_pos())
        rules_button.draw(screen)
        quit_button.moused_over(pygame.mouse.get_pos())
        quit_button.draw(screen)

        pygame.display.update()
        clock.tick(cm.tickrate)

def rulespage():
    HeaderText = cm.font.render("RULES PAGE", True, cm.WHITE)
    Tab1Text = cm.font.render("Objectives", True, cm.WHITE)
    Tab2Text = cm.font.render("Rules", True, cm.WHITE)
    Tab3Text = cm.font.render("Pieces", True, cm.WHITE)
    while True:
        #follow mouse
        mouse = pygame.mouse.get_pos()
        #first color the screen and add headers.
        screen.fill(cm.blackish)
        screen.blit(HeaderText, (cm.WIDTH / 2 , 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if u click on objective tab, open objective tab
                if cm.ObjButtonLoc[0] <= mouse[0] <= cm.ObjButtonLoc[0] + cm.ObjButtonLoc[2] and \
                        cm.ObjButtonLoc[1] <= mouse[1] <= cm.ObjButtonLoc[1] + cm.ObjButtonLoc[3]:
                    ObjectiveTab()
                #if u click on RulesTab, open Rules Tab
                if cm.RuleButtonLoc[0] <= mouse[0] <= cm.RuleButtonLoc[0] + cm.RuleButtonLoc[2] and \
                        cm.RuleButtonLoc[1] <= mouse[1] <= cm.RuleButtonLoc[1] + cm.RuleButtonLoc[3]:
                    RulesTab()
                #If u click on Pieces Tab, Open Pieces Tab
                if cm.PieceButtonLoc[0] <= mouse[0] <= cm.PieceButtonLoc[0] + cm.PieceButtonLoc[2] and \
                        cm.PieceButtonLoc[1] <= mouse[1] <= cm.PieceButtonLoc[1] + cm.PieceButtonLoc[3]:
                    PiecesTab()
            #if u are hovering Objective Tab
        if cm.ObjButtonLoc[0] <= mouse[0] <= cm.ObjButtonLoc[0] + cm.ObjButtonLoc[2] and\
                cm.ObjButtonLoc[1] <= mouse[1] <= cm.ObjButtonLoc[1] + cm.ObjButtonLoc[3]:
            pygame.draw.rect(screen, cm.buttonhover, cm.ObjButtonLoc)
            pygame.draw.rect(screen, cm.buttoncolor, cm.RuleButtonLoc)
            pygame.draw.rect(screen, cm.buttoncolor, cm.PieceButtonLoc)
            # if u are hovering Rules Tab
        elif cm.RuleButtonLoc[0] <= mouse[0] <= cm.RuleButtonLoc[0] + cm.RuleButtonLoc[2] and \
                cm.RuleButtonLoc[1] <= mouse[1] <= cm.RuleButtonLoc[1] + cm.RuleButtonLoc[3]:
            pygame.draw.rect(screen, cm.buttoncolor, cm.ObjButtonLoc)
            pygame.draw.rect(screen, cm.buttonhover, cm.RuleButtonLoc)
            pygame.draw.rect(screen, cm.buttoncolor, cm.PieceButtonLoc)
            # if u are hovering Pieces Tab
        elif cm.PieceButtonLoc[0] <= mouse[0] <= cm.PieceButtonLoc[0] + cm.PieceButtonLoc[2] and \
                cm.PieceButtonLoc[1] <= mouse[1] <= cm.PieceButtonLoc[1] + cm.PieceButtonLoc[3]:
            pygame.draw.rect(screen, cm.buttoncolor, cm.ObjButtonLoc)
            pygame.draw.rect(screen, cm.buttoncolor, cm.RuleButtonLoc)
            pygame.draw.rect(screen, cm.buttonhover, cm.PieceButtonLoc)
            #if not hovering any, then just put buttons there.
        else:
                pygame.draw.rect(screen, cm.buttoncolor, cm.ObjButtonLoc)
                pygame.draw.rect(screen, cm.buttoncolor, cm.RuleButtonLoc)
                pygame.draw.rect(screen, cm.buttoncolor, cm.PieceButtonLoc)
        screen.blit(Tab1Text, (cm.WIDTH / 6, cm.HEIGHT/8))
        screen.blit(Tab2Text, (cm.WIDTH / 2, cm.HEIGHT/8))
        screen.blit(Tab3Text, (5 * cm.WIDTH / 6, cm.HEIGHT/8))


        pygame.display.update()
        clock.tick(cm.tickrate)

while True:
    start_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(cm.tickrate)


