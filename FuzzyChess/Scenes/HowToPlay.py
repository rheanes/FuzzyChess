from Scenes.RulesPageCommon import *
from guielements import *
from common import *


def HowToPlayScene(screen):
    Page_Title = font.render("How to Play", True, BLACK)
    Page_Text = ["There are three extra action buttons on the side of the board.",
                 "The Deligate button allows the player to change the membership of a piece to a corp.",
                 "The end turn button will end the turn of the player and they will not be able",
                 "to make actions till next turn. The resign button will cause the player to instantly",
                 "forefit the game and lose.In order to move pieces, simply click the piece you would",
                 "like to move, and if it is possible to move that piece, then the potential movments will",
                 "be displayed on the board in blue. If a piece can attack another piece then it will",
                 "highlight the square with black. Simply click on the blue or red square to attack",
                 "or move the currently selected piece."]
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
        pygame.display.flip()