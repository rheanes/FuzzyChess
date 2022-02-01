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

#turns text into list of seperate strings for multiline elements
def create_multiline_text(text, font):
    pos_x = cm.WIDTH * 0.1
    pos_y = cm.HEIGHT * 0.35
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
        return pygame.transform.scale(self.image, (x_factor,y_factor))

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
    b_knight.scale(400, 400)
    
    play_button = button(pos=(600, 300), font_size=50, txt_col=cm.BLACK, bg_col=cm.LIGHT_GRAY, text="Play")
    rules_button = button(pos=(600, 400), font_size=50, txt_col=cm.BLACK, bg_col=cm.BROWN, text="Rules")
    quit_button = button(pos=(600, 500), font_size=50, txt_col=cm.BLACK, bg_col=cm.RED, text="Quit Game")
    yeet = [play_button, rules_button, quit_button]
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

        for yee in yeet:
            yee.moused_over(pygame.mouse.get_pos())
            yee.draw(screen)

        pygame.display.update()
        clock.tick(cm.tickrate)

def rulespage():
    Home_Button = button(pos=(cm.WIDTH / 2, 0.2 * cm.HEIGHT), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                         text="Return to Homescreen")
    Obj_Tab = button(pos=(cm.WIDTH/6, cm.HEIGHT/8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                     text="Objectives")
    Rule_Tab = button(pos=(cm.WIDTH/2, cm.HEIGHT/8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                      text="Rules")
    Pieces_Tab = button(pos=(5*cm.WIDTH/6, cm.HEIGHT/8), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                        text="Pieces")
    tabs = [Home_Button, Obj_Tab, Rule_Tab, Pieces_Tab]
    ObjectiveTab(tabs)



def ObjectiveTab(tabs):
    HeaderText = cm.font.render("Objectives", True, cm.BLACK)
    ObjectiveText = ["Much like normal chess, the goal of fuzzy logic ",
                     "chess is to capture the enemy's king. However, ",
                     "there are no checks or checkmates and capturing",
                     "the king is like capturing any other piece."]
    text_label, text_pos = create_multiline_text(ObjectiveText, cm.font)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    start_menu()
                if tabs[1].selected:
                    ObjectiveTab(tabs)
                if tabs[2].selected:
                    RulesTab(tabs)
                if tabs[3].selected:
                    PiecesTab(tabs)
        screen.fill(cm.WHITE)
        screen.blit(HeaderText, (cm.WIDTH * 0.40, cm.HEIGHT / 4))
        #loops through text list and blits each line to the screen
        for line in range(len(text_label)):
            screen.blit(text_label[line], (text_pos[0], text_pos[1] + (line * 30)+ (5 * line)))
        for tab in tabs:
            tab.draw(screen)
            tab.moused_over(pygame.mouse.get_pos())
        pygame.display.flip()

def RulesTab(tabs):
    HeaderText = cm.font.render("RULES PAGE", True, cm.BLACK)
    RulesText = cm.font.render("This is the text for the rules", True, cm.BLACK)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    start_menu()
                if tabs[1].selected:
                    ObjectiveTab(tabs)
                if tabs[2].selected:
                    RulesTab(tabs)
                if tabs[3].selected:
                    PiecesTab(tabs)
            screen.fill(cm.WHITE)
            screen.blit(HeaderText, (cm.WIDTH / 2, 0))
            screen.blit(RulesText, (cm.WIDTH / 2, cm.HEIGHT / 2))
            for tab in tabs:
                tab.draw(screen)
                tab.moused_over(pygame.mouse.get_pos())
            pygame.display.flip()
def PiecesTab(tabs):
    positions = [(cm.WIDTH / 6, cm.HEIGHT / 2), (cm.WIDTH / 2, cm.HEIGHT / 2),
                 (5 * cm.WIDTH / 6, cm.HEIGHT / 2), (cm.WIDTH / 6, 7 * cm.HEIGHT / 8),
                 (cm.WIDTH / 2, 7 * cm.HEIGHT / 8), (5 * cm.WIDTH / 6, 7 * cm.HEIGHT / 8)]
    HeaderText = cm.font.render("RULES PAGE", True, cm.BLACK)
    Pawn_Button = button(pos=(positions[0]), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                         text="Pawn")
    Rook_Button = button(pos=(positions[1]), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                         text="Rook")
    Knight_Button = button(pos=(positions[2]), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                           text="Knight")
    Queen_Button = button(pos=(positions[3]), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                          text="Queen")
    Bishop_Button = button(pos=(positions[4]), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                           text="Bishop")
    King_Button = button(pos=(positions[5]), font_size=50, txt_col=cm.BLACK,
                         bg_col=cm.buttoncolor,
                         text="King")
    buttons = [Pawn_Button, Rook_Button, Knight_Button, Queen_Button, Bishop_Button, King_Button]
    #images and text for pieces
    pawn = Element("./Images/blue_pawn.png", (positions[0][0] , positions[0][1]-20))
    rook = Element("./Images/blue_rook.png", (positions[1][0] , positions[1][1]-20))
    knight = Element("./Images/blue_knight.png", (positions[2][0] , positions[2][1]-20))
    queen = Element("./Images/blue_queen.png", (positions[3][0] , positions[3][1]-20))
    bishop = Element("./Images/blue_bishop.png", (positions[4][0] , positions[4][1]-20))
    king = Element("./Images/blue_king.png", (positions[5][0] , positions[5][1]-20))
    images = [pawn, rook, knight, queen, bishop, king]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    start_menu()
                if tabs[1].selected:
                    ObjectiveTab(tabs)
                if tabs[2].selected:
                    RulesTab(tabs)
                if tabs[3].selected:
                    PiecesTab(tabs)
                if buttons[0].selected:
                    pawnPage(tabs)
                if buttons[1].selected:
                    rookPage(tabs)
                if buttons[2].selected:
                    knightPage(tabs)
                if buttons[3].selected:
                    queenPage(tabs)
                if buttons[4].selected:
                    bishopPage(tabs)
                if buttons[5].selected:
                    kingPage(tabs)
            screen.fill(cm.WHITE)
            screen.blit(HeaderText, (cm.WIDTH / 2, 0))
            for tab in tabs:
                tab.draw(screen)
                tab.moused_over(pygame.mouse.get_pos())
            for img in images:
                img.draw(screen)
            for b in buttons:
                b.draw(screen)
                b.moused_over(pygame.mouse.get_pos())

            pygame.display.flip()

def pawnPage(tabs):
    HeaderText = cm.font.render("RULES PAGE", True, cm.BLACK)
    PieceDes = cm.font.render("Description of the piece Here.", True, cm.BLACK)
    positions = [(cm.WIDTH/6, 3/8*cm.HEIGHT), (cm.WIDTH/3, 3/8*cm.HEIGHT), (cm.WIDTH/2, 3/8*cm.HEIGHT),
                 (2/3*cm.WIDTH, 3/8*cm.HEIGHT), (5/6*cm.WIDTH, 3/8*cm.HEIGHT), (cm.WIDTH, 3/8*cm.HEIGHT)]
    img1 = Element("./Images/blue_pawn.png", (positions[0][0] , positions[0][1]))
    img2 = Element("./Images/purple_pawn.png", (positions[1][0], positions[1][1]))
    img3 = Element("./Images/green_pawn.png", (positions[2][0], positions[2][1]))
    img4 = Element("./Images/red_pawn.png", (positions[3][0], positions[3][1]))
    img5 = Element("./Images/orange_pawn.png", (positions[4][0], positions[4][1]))
    img6 = Element("./Images/yellow_pawn.png", (positions[5][0], positions[5][1]))
    imgs = [img1, img2, img3, img4, img5, img6]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    start_menu()
                if tabs[1].selected:
                    ObjectiveTab(tabs)
                if tabs[2].selected:
                    RulesTab(tabs)
                if tabs[3].selected:
                    PiecesTab(tabs)
        screen.fill(cm.WHITE)
        screen.blit(HeaderText, (cm.WIDTH / 2, 0))
        for tab in tabs:
            tab.draw(screen)
            tab.moused_over(pygame.mouse.get_pos())
        for img in imgs:
            img.draw(screen)
        screen.blit(PieceDes, (cm.WIDTH / 4, 5 / 8 * cm.HEIGHT))
        pygame.display.flip()

def rookPage(tabs):
    HeaderText = cm.font.render("RULES PAGE", True, cm.BLACK)
    PieceDes = cm.font.render("Description of the piece Here.", True, cm.BLACK)
    positions = [(cm.WIDTH / 6, 3 / 8 * cm.HEIGHT), (cm.WIDTH / 3, 3 / 8 * cm.HEIGHT),
                 (cm.WIDTH / 2, 3 / 8 * cm.HEIGHT),
                 (2 / 3 * cm.WIDTH, 3 / 8 * cm.HEIGHT), (5 / 6 * cm.WIDTH, 3 / 8 * cm.HEIGHT),
                 (cm.WIDTH, 3 / 8 * cm.HEIGHT)]
    img1 = Element("./Images/blue_rook.png", (positions[0][0], positions[0][1]))
    img2 = Element("./Images/purple_rook.png", (positions[1][0], positions[1][1]))
    img3 = Element("./Images/green_rook.png", (positions[2][0], positions[2][1]))
    img4 = Element("./Images/red_rook.png", (positions[3][0], positions[3][1]))
    img5 = Element("./Images/orange_rook.png", (positions[4][0], positions[4][1]))
    img6 = Element("./Images/yellow_rook.png", (positions[5][0], positions[5][1]))
    imgs = [img1, img2, img3, img4, img5, img6]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    start_menu()
                if tabs[1].selected:
                    ObjectiveTab(tabs)
                if tabs[2].selected:
                    RulesTab(tabs)
                if tabs[3].selected:
                    PiecesTab(tabs)
        screen.fill(cm.WHITE)
        screen.blit(HeaderText, (cm.WIDTH / 2, 0))
        for tab in tabs:
            tab.draw(screen)
            tab.moused_over(pygame.mouse.get_pos())
        for img in imgs:
            img.draw(screen)
        screen.blit(PieceDes, (cm.WIDTH / 4, 5 / 8 * cm.HEIGHT))
        pygame.display.flip()

def knightPage(tabs):
    HeaderText = cm.font.render("RULES PAGE", True, cm.BLACK)
    PieceDes = cm.font.render("Description of the piece Here.", True, cm.BLACK)
    positions = [(cm.WIDTH / 6, 3 / 8 * cm.HEIGHT), (cm.WIDTH / 3, 3 / 8 * cm.HEIGHT),
                 (cm.WIDTH / 2, 3 / 8 * cm.HEIGHT),
                 (2 / 3 * cm.WIDTH, 3 / 8 * cm.HEIGHT), (5 / 6 * cm.WIDTH, 3 / 8 * cm.HEIGHT),
                 (cm.WIDTH, 3 / 8 * cm.HEIGHT)]
    img1 = Element("./Images/blue_knight.png", (positions[0][0], positions[0][1]))
    img2 = Element("./Images/purple_knight.png", (positions[1][0], positions[1][1]))
    img3 = Element("./Images/green_knight.png", (positions[2][0], positions[2][1]))
    img4 = Element("./Images/red_knight.png", (positions[3][0], positions[3][1]))
    img5 = Element("./Images/orange_knight.png", (positions[4][0], positions[4][1]))
    img6 = Element("./Images/yellow_knight.png", (positions[5][0], positions[5][1]))
    imgs = [img1, img2, img3, img4, img5, img6]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    start_menu()
                if tabs[1].selected:
                    ObjectiveTab(tabs)
                if tabs[2].selected:
                    RulesTab(tabs)
                if tabs[3].selected:
                    PiecesTab(tabs)
        screen.fill(cm.WHITE)
        screen.blit(HeaderText, (cm.WIDTH / 2, 0))
        for tab in tabs:
            tab.draw(screen)
            tab.moused_over(pygame.mouse.get_pos())
        for img in imgs:
            img.draw(screen)
        screen.blit(PieceDes, (cm.WIDTH / 4, 5 / 8 * cm.HEIGHT))
        pygame.display.flip()

def queenPage(tabs):
    HeaderText = cm.font.render("RULES PAGE", True, cm.BLACK)
    PieceDes = cm.font.render("Description of the piece Here.", True, cm.BLACK)
    positions = [(cm.WIDTH/4, 3 / 8 * cm.HEIGHT), (cm.WIDTH * 3/4, 3 / 8 * cm.HEIGHT)]
    img1 = Element("./Images/blue_queen.png", (positions[0][0], positions[0][1]))
    img2 = Element("./Images/red_queen.png", (positions[1][0], positions[1][1]))
    imgs = [img1, img2]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    start_menu()
                if tabs[1].selected:
                    ObjectiveTab(tabs)
                if tabs[2].selected:
                    RulesTab(tabs)
                if tabs[3].selected:
                    PiecesTab(tabs)
        screen.fill(cm.WHITE)
        screen.blit(HeaderText, (cm.WIDTH / 2, 0))
        for tab in tabs:
            tab.draw(screen)
            tab.moused_over(pygame.mouse.get_pos())
        for img in imgs:
            img.draw(screen)
        screen.blit(PieceDes, (cm.WIDTH / 4, 5 / 8 * cm.HEIGHT))
        pygame.display.flip()

def bishopPage(tabs):
    HeaderText = cm.font.render("RULES PAGE", True, cm.BLACK)
    PieceDes = cm.font.render("Description of the piece Here.", True, cm.BLACK)
    positions = [(cm.WIDTH / 3, 3 / 8 * cm.HEIGHT), (cm.WIDTH / 2, 3 / 8 * cm.HEIGHT),
                 (cm.WIDTH * 2/3, 3 / 8 * cm.HEIGHT), (5/6 * cm.WIDTH, 3 / 8 * cm.HEIGHT)]
    img1 = Element("./Images/green_bishop.png", (positions[0][0], positions[0][1]))
    img2 = Element("./Images/purple_bishop.png", (positions[1][0], positions[1][1]))
    img3 = Element("./Images/orange_bishop.png", (positions[2][0], positions[2][1]))
    img4 = Element("./Images/yellow_bishop.png", (positions[3][0], positions[3][1]))
    imgs = [img1, img2, img3, img4]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    start_menu()
                if tabs[1].selected:
                    ObjectiveTab(tabs)
                if tabs[2].selected:
                    RulesTab(tabs)
                if tabs[3].selected:
                    PiecesTab(tabs)
        screen.fill(cm.WHITE)
        screen.blit(HeaderText, (cm.WIDTH / 2, 0))
        for tab in tabs:
            tab.draw(screen)
            tab.moused_over(pygame.mouse.get_pos())
        for img in imgs:
            img.draw(screen)
        screen.blit(PieceDes, (cm.WIDTH / 4, 5 / 8 * cm.HEIGHT))
        pygame.display.flip()

def kingPage(tabs):
    HeaderText = cm.font.render("RULES PAGE", True, cm.BLACK)
    PieceDes = cm.font.render("Description of the piece Here.", True, cm.BLACK)
    positions = [(cm.WIDTH / 4, 3 / 8 * cm.HEIGHT), (cm.WIDTH * 3 / 4, 3 / 8 * cm.HEIGHT)]
    img1 = Element("./Images/blue_king.png", (positions[0][0], positions[0][1]))
    img2 = Element("./Images/red_king.png", (positions[1][0], positions[1][1]))
    imgs = [img1, img2]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if tabs[0].selected:
                    start_menu()
                if tabs[1].selected:
                    ObjectiveTab(tabs)
                if tabs[2].selected:
                    RulesTab(tabs)
                if tabs[3].selected:
                    PiecesTab(tabs)
        screen.fill(cm.WHITE)
        screen.blit(HeaderText, (cm.WIDTH / 2, 0))
        for tab in tabs:
            tab.draw(screen)
            tab.moused_over(pygame.mouse.get_pos())
        for img in imgs:
            img.draw(screen)
        screen.blit(PieceDes, (cm.WIDTH / 4, 5/8*cm.HEIGHT))
        pygame.display.flip()


while True:
    start_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(cm.tickrate)


