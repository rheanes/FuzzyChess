from Scenes.RulesPageCommon import *
from guielements import *
from common import *


def QueenScene(screen):
    Page_Title = font.render("Queens", True, BLACK)
    Page_Text = ["Movement: 3 Squares any Direction",
                 "Attack Range: 1 Square any Direction",
                 "Min role to capture: Pawn=2, Rook=5, Bishop=4, Knight=4, Queen=4, King=4",
                 "",
        "The king’s right (or left) hand. She is the only other",
                 "piece that is considered royalty. This means that her attacks",
                 " are as powerful as the king, but she moves just as slowly."]

    img = Element("./Images/blue_queen.png", (4/8*WIDTH, 5/8*HEIGHT))

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
        img.draw(screen)
        pygame.display.flip()