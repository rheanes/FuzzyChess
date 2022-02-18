from Scenes.RulesPageCommon import *
from guielements import *
from common import *


def KingScene(screen):
    Page_Title = font.render("Kings", True, BLACK)
    Page_Text = ["if this piece is captured you lose, the leader of the army"
        , "and commander of the center corps, can move up to "
        , "three squares in any direction and does not have to  "
        , "move in a straight line, can attack any adjacent square, "
        , "can delegate pieces in his corps to another corps or ",
                "pull pieces from the other corps into his own (this counts as "
        , "this corps action)."]
    img1 = Element("./Images/blue_king.png", (positions2[0][0], positions2[0][1]))
    img2 = Element("./Images/red_king.png", (positions2[1][0], positions2[1][1]))
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