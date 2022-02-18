from Scenes.RulesPageCommon import *
from guielements import *
from common import *


def BishopScene(screen):
    Page_Title = font.render("Bishops", True, BLACK)
    Page_Text = ["The king’s trusted advisors, if they are captured, then"
        , "the pieces under their command fall to the king’s "
        , "command and that corps’ action is lost for the remainder  "
        , "of the game, they can move up to two squares  "
        , "in any direction and do not have to move in a straight "
        , "line, they can attack any adjacent square."]
    img1 = Element("./Images/green_bishop.png", (positions4[0][0], positions4[0][1]))
    img2 = Element("./Images/purple_bishop.png", (positions4[1][0], positions4[1][1]))
    img3 = Element("./Images/orange_bishop.png", (positions4[2][0], positions4[2][1]))
    img4 = Element("./Images/yellow_bishop.png", (positions4[3][0], positions4[3][1]))
    imgs = [img1, img2, img3, img4]
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