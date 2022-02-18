import pygame.draw_py
from Scenes.RulesPageCommon import *
from guielements import *
from common import *

def RulesPageScene(screen):
    Page_Title = font.render("Game Rules", True, BLACK)
    Page_Text = ["Much like normal chess, the goal of fuzzy logic ",
                     "chess is to capture the enemy's king. However, ",
                     "there are no checks or checkmates and capturing",
                     "the king is like capturing any other piece."]
    while True:
        mouse_down = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True
        drawscreen(screen, Page_Title, Page_Text)
        for tab in tabs:
            ui_action = tab.moused_over(pygame.mouse.get_pos(),mouse_down)
            if ui_action is not None:
                return ui_action
            tab.draw(screen)
        pygame.display.flip()


