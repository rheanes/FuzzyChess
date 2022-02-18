from Scenes.RulesPageCommon import *
from guielements import *
from common import *


def PawnScene(screen):
    Page_Title = font.render("Pawns", True, BLACK)
    Page_Text = ["The basic infantry and usually considered cannon ",
                "fodder, they can only move one square at a time",
                "and may only move forward or forward diagonally, ",
                "they can only attack in the same way they move, when",
                "they reach the other side, they do not gain a",
                "promotion like in traditional chess."]

    img1 = Element("./Images/blue_pawn.png", (positions6[0][0], positions6[0][1]))
    img2 = Element("./Images/purple_pawn.png", (positions6[1][0], positions6[1][1]))
    img3 = Element("./Images/green_pawn.png", (positions6[2][0], positions6[2][1]))
    img4 = Element("./Images/red_pawn.png", (positions6[3][0], positions6[3][1]))
    img5 = Element("./Images/orange_pawn.png", (positions6[4][0], positions6[4][1]))
    img6 = Element("./Images/yellow_pawn.png", (positions6[5][0], positions6[5][1]))
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