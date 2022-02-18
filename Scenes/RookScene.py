from Scenes.RulesPageCommon import *
from guielements import *
from common import *


def RookScene(screen):
    Page_Title = font.render("Rooks", True, BLACK)
    Page_Text = ["The archers, they provide long range support, they "
        , "can move up to two squares in any direction and do "
        , "not have to move in a straight line, they can make an  "
        , "attack in any direction up to three squares away,  "
        , "they do this by shooting over any squares between "
        , "them and their target  so only the target is hit."]
    img1 = Element("./Images/blue_rook.png", (positions6[0][0], positions6[0][1]))
    img2 = Element("./Images/purple_rook.png", (positions6[1][0], positions6[1][1]))
    img3 = Element("./Images/green_rook.png", (positions6[2][0], positions6[2][1]))
    img4 = Element("./Images/red_rook.png", (positions6[3][0], positions6[3][1]))
    img5 = Element("./Images/orange_rook.png", (positions6[4][0], positions6[4][1]))
    img6 = Element("./Images/yellow_rook.png", (positions6[5][0], positions6[5][1]))
    imgs = [img1, img2, img3, img4, img5, img6]
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