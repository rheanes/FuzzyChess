from Scenes.RulesPageCommon import *
from guielements import *
from common import *


def QueenScene(screen):
    Page_Title = font.render("Queens", True, BLACK)
    Page_Text = ["The king’s right (or left) hand, she can move up to three "
        , "squares in any direction and does not have to move in a "
        , "straight line, she can also attack any adjacent squares."]
    img1 = Element("./Images/blue_queen.png", (positions2[0][0], positions2[0][1]))
    img2 = Element("./Images/red_queen.png", (positions2[1][0], positions2[1][1]))
    imgs = [img1, img2]
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