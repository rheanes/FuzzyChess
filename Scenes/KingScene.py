from Scenes.RulesPageCommon import *
from guielements import *
from common import *


def KingScene(screen):
    Page_Title = font.render("Kings", True, BLACK)
    Page_Text = ["Movement: 3 Squares any Direction",
                 "Attack Range: 1 Square any Direction",
                 "Min role to capture: Pawn=1, Rook=5, Bishop=4, Knight=4, Queen=4, King=4",
                 "",
        "If the king is captured you lose the leader of the army"
        , "and you also lose the game."
        , "The king can delegate pieces in his corps to another corps or "
        ,"pull pieces from the other corps into his own (this counts as "
        , "this corps action)."]

    img = Element("./Images/blue_king.png", (4/8*WIDTH, 5/8*HEIGHT))

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
        img.draw(screen)
        pygame.display.flip()