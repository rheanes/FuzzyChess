from Scenes.RulesPageCommon import *
from guielements import *
from common import *


def RookScene(screen):
    Page_Title = font.render("Rooks", True, BLACK)
    Page_Text = ["Movement: 2 Squares any direction",
                 "Attack Range: 3 Squares any direction",
                 "Min role to capture: Pawn=4, Rook=4, Bishop=4, Knight=5, Queen=5, King=5",
                 "",
                "The Rooks, or archers provide long range support, they ",
                " do this by shooting over any squares between ",
                 "them and their target  so only the target is hit."]

    img1 = Element("./Images/blue_rook.png", (positions3[0][0], positions3[0][1]))
    img2 = Element("./Images/purple_rook.png", (positions3[1][0], positions3[1][1]))
    img3 = Element("./Images/green_rook.png", (positions3[2][0], positions3[2][1]))
    imgs = [img1, img2, img3]

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
        for img in imgs:
            img.draw(screen)
        pygame.display.flip()