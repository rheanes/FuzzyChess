from Scenes.RulesPageCommon import *
from guielements import *
from common import *


def KnightScene(screen):
    Page_Title = font.render("Knights", True, BLACK)
    Page_Text = ["Movement: 4 Squares any Direction",
                 "Attack Range: 1 Square any Direction",
                 "Min role to capture: Pawn=2, Rook=5, Bishop=5, Knight=5, Queen=5, King=5",
                 "",
        " Knights have the special ability to move and "
        , "attack in the same turn, this counts as an ambush and "
        , "when capturing an enemy after moving they add one to  "
        , "the die roll (note: when the knight makes the attack, their "
        , "turn is over, you must move, then attack)."]
    img1 = Element("./Images/blue_knight.png", (positions3[0][0], positions3[0][1]))
    img2 = Element("./Images/purple_knight.png", (positions3[1][0], positions3[1][1]))
    img3 = Element("./Images/green_knight.png", (positions3[2][0], positions3[2][1]))
    imgs = [img1, img2, img3]
    while True:
        mouse_down = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        drawscreen(screen, Page_Title, Page_Text)
        for tab in tabs:
            ui_action = tab.moused_over(pygame.mouse.get_pos(),mouse_down)
            if ui_action is not None:
                return ui_action
            tab.draw(screen)
        for img in imgs:
            img.draw(screen)
        pygame.display.flip()