from guielements import *
from common import *

def NewOrLoadScene(screen):
    Page_Title = font.render("How to Play", True, BLACK)
    Home_Button = button((WIDTH/ 2, 100),
                         font_size=48,
                         txt_col=BLACK,
                         bg_col=buttoncolor,
                         text="Return Home",
                         bg_hover=buttonhover,
                         action=GameState.Home)
    New_Button = button((WIDTH / 2, 300),
                         font_size=48,
                         txt_col=BLACK,
                         bg_col=buttoncolor,
                         text="New Game",
                         bg_hover=buttonhover,
                         action=GameState.NewGame)
    Continue_Button = button((WIDTH / 2, 400),
                         font_size=48,
                         txt_col=BLACK,
                         bg_col=buttoncolor,
                         text="Continue Game",
                         bg_hover=buttonhover,
                         action=GameState.Play)

    Load_Button = button((WIDTH / 2, 500),
                         font_size=48,
                         txt_col=BLACK,
                         bg_col=buttoncolor,
                         text="Load Game",
                         bg_hover=buttonhover,
                         action=1)

    tabs = [Home_Button, New_Button, Continue_Button, Load_Button]
    while True:
        mouse_down = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #draw stuff on screen here
            screen.fill(BACKGROUND)
            for tab in tabs:
                ui_action = tab.moused_over(pygame.mouse.get_pos(), mouse_down)
                if ui_action == 1:
                    ui_action = LoadGame(screen)
                if ui_action is not None:
                    return ui_action
                tab.draw(screen)
            pygame.display.flip()



def LoadGame(screen):
    Back_Button = button((WIDTH / 2, 100),
                         font_size=48,
                         txt_col=BLACK,
                         bg_col=buttoncolor,
                         text="Back",
                         bg_hover=buttonhover,
                         action=GameState.NewOrLoad)
    Load1_Button = button((WIDTH / 2, 200),
                        font_size=48,
                        txt_col=BLACK,
                        bg_col=buttoncolor,
                        text="Load 1",
                        bg_hover=buttonhover,
                        action=GameState.Load1)
    Load2_Button = button((WIDTH / 2, 300),
                             font_size=48,
                             txt_col=BLACK,
                             bg_col=buttoncolor,
                             text="Load 2",
                             bg_hover=buttonhover,
                             action=GameState.Load2)
    Load3_Button = button((WIDTH / 2, 400),
                         font_size=48,
                         txt_col=BLACK,
                         bg_col=buttoncolor,
                         text="Load 3",
                         bg_hover=buttonhover,
                         action=GameState.Load3)
    tabs = [Back_Button, Load1_Button, Load2_Button, Load3_Button]
    while True:
        mouse_down = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #draw stuff on screen here
            screen.fill(BACKGROUND)
            for tab in tabs:
                ui_action = tab.moused_over(pygame.mouse.get_pos(), mouse_down)
                if ui_action is not None:
                    return ui_action
                tab.draw(screen)
            pygame.display.flip()
