from Scenes.RulesPageCommon import *
from guielements import *
from common import *


def KnightScene(screen):
    Page_Title = font.render("Knights", True, BLACK)
    Page_Text = ["The mounted attackers charging into battle, they can "
        , "move up to four squares in any direction and do not "
        , "have to move in a straight line, they can attack any  "
        , "adjacent square, they also have the ability to move and "
        , "attack in the same turn, this counts as an ambush and "
        , "when capturing an enemy after moving they add one to  "
        , "the die roll (note: when the knight makes the attack, their "
        , "turn is over, you must move, then attack)."]
    img1 = Element("./Images/blue_knight.png", (positions6[0][0], positions6[0][1]))
    img2 = Element("./Images/purple_knight.png", (positions6[1][0], positions6[1][1]))
    img3 = Element("./Images/green_knight.png", (positions6[2][0], positions6[2][1]))
    img4 = Element("./Images/red_knight.png", (positions6[3][0], positions6[3][1]))
    img5 = Element("./Images/orange_knight.png", (positions6[4][0], positions6[4][1]))
    img6 = Element("./Images/yellow_knight.png", (positions6[5][0], positions6[5][1]))
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