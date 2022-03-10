from Scenes.RulesPageCommon import *
from guielements import *
from common import *


def PiecesScene(screen):
    Page_Title = font.render("Rooks", True, BLACK)
    Page_Text = ["Each piece is a member of a corp and can only be moved by the commander of the corp",
                 "The colors of the pieces symbolize which corp they belong to.",
                 "The bishops and the king are the commanders of the military. If a bishop is captured, then",
                 "a turn is lost for the side that lost the bishop."]
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