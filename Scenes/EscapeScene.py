from pygame import KEYDOWN

from guielements import *

boxLoc = (400, 200, 400, 500)


def escapeScene(screen):
    #Define Text
    Top_Text = font.render("Escape Menu", True, BLACK)
    #define buttons
    Home_Button = button(pos = (600, 300),
                         font_size=48,
                         txt_col=BLACK,
                         bg_col=buttoncolor,
                         text="Game Menu",
                         bg_hover=buttonhover,
                         action=GameState.Home)
    Resume_Button = button(pos=(600, 375),
                          font_size=48,
                          txt_col=BLACK,
                          bg_col=buttoncolor,
                          text="Resume Game",
                          bg_hover=buttonhover,
                          action=GameState.Play)
    Save_Button = button(pos=(600, 450),
                          font_size=48,
                          txt_col=BLACK,
                          bg_col=buttoncolor,
                          text="Save Game",
                          bg_hover=buttonhover,
                          action=1)
    Rules_Button = button(pos=(600, 525),
                           font_size=48,
                           txt_col=BLACK,
                           bg_col=buttoncolor,
                           text="Game Rules",
                           bg_hover=buttonhover,
                           action=GameState.Rules)
    Quit_Button = button(pos=(600, 600),
                         font_size=48,
                         txt_col=BLACK,
                         bg_col=buttoncolor,
                         text="Quit Game",
                         bg_hover=buttonhover,
                         action=GameState.Quit)
    buttons = [Home_Button, Resume_Button, Save_Button, Rules_Button, Quit_Button]
    while True:
        mouse_down = False
        for event in pygame.event.get():
            if (event.type == KEYDOWN):
                if event.key == K_ESCAPE:
                    return GameState.Play
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        #draw a rectangle here!
        pygame.draw.rect(screen, BLACK, pygame.Rect(boxLoc))
        for b in buttons:
            ui_action = b.moused_over(pygame.mouse.get_pos(),mouse_down)
            if ui_action == 1:
                ui_action = SaveGame(screen)
            if ui_action is not None:
                return ui_action
            b.draw(screen)
        pygame.display.flip()

def SaveGame(screen):
    Back_Button = button((600, 300),
                         font_size=48,
                         txt_col=BLACK,
                         bg_col=buttoncolor,
                         text="Back",
                         bg_hover=buttonhover,
                         action=GameState.Escape)
    Save1_Button = button((600, 400),
                          font_size=48,
                          txt_col=BLACK,
                          bg_col=buttoncolor,
                          text="Save 1",
                          bg_hover=buttonhover,
                          action=GameState.Save1)
    Save2_Button = button((600, 500),
                          font_size=48,
                          txt_col=BLACK,
                          bg_col=buttoncolor,
                          text="Save 2",
                          bg_hover=buttonhover,
                          action=GameState.Save2)
    Save3_Button = button((600, 600),
                          font_size=48,
                          txt_col=BLACK,
                          bg_col=buttoncolor,
                          text="Save 3",
                          bg_hover=buttonhover,
                          action=GameState.Save3)
    tabs = [Back_Button, Save1_Button, Save2_Button, Save3_Button]

    while True:
        mouse_down = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            #draw stuff on screen here
            pygame.draw.rect(screen, BLACK, pygame.Rect(boxLoc))
            for tab in tabs:
                ui_action = tab.moused_over(pygame.mouse.get_pos(), mouse_down)
                if ui_action is not None:
                    return ui_action
                tab.draw(screen)
            pygame.display.flip()
