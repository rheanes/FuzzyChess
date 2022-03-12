from Scenes.RulesPageCommon import *
from guielements import *
from common import *


def BishopScene(screen):
    Page_Title = font.render("Bishops", True, BLACK)
    Page_Text = ["Movement: 2 Squares any direction",
                 "Attack Range: 1 Squares any direction",
                 "Min role to capture: Pawn=3, Rook=5, Bishop=4, Knight=5, Queen=5, King=5",
                 "",
        "The king’s trusted advisors, if they are captured, then"
        , "the pieces under their command fall to the king’s "
        , "command and that corps’ action is lost for the remainder  "
        , "of the game. This makes them the second most valuable piece",
            "next to the king."]
    img1 = Element("./Images/green_bishop.png", (3/8*WIDTH, 5/8*HEIGHT))
    img2 = Element("./Images/purple_bishop.png", (5/8*WIDTH, 5/8*HEIGHT))
    imgs = [img1, img2]
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