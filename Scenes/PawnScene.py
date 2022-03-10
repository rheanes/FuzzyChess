from Scenes.RulesPageCommon import *
from guielements import *
from common import *


def PawnScene(screen):
    Page_Title = font.render("Pawns", True, BLACK)
    Page_Text = ["Movement: 1 Square forward direction only",
                 "Attack Range: 1 Square forward direction only",
                 "Min role to capture: Pawn=4, Rook=6, Bishop=5, Knight=6, Queen=6, King=6",
                 "",
                "The pawn is the basic infantry and usually considered a cannon ",
                "they can only attack in the same way they move, when",
                "they reach the other side, they do not gain a",
                "promotion like in traditional chess. For their first move,",
                 "they can't move two squares like in traditional chess."]

    img1 = Element("./Images/blue_pawn.png", (positions3[0][0], positions3[0][1]))
    img2 = Element("./Images/purple_pawn.png", (positions3[1][0], positions3[1][1]))
    img3 = Element("./Images/green_pawn.png", (positions3[2][0], positions3[2][1]))
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