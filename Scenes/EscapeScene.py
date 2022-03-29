from pygame import KEYDOWN

from guielements import *

def escapeScene(screen):
    #Define Text
    Top_Text = font.render("Escape Menu", True, BLACK)
    #define buttons
    Home_Button = button(pos = (400, 300),
                         font_size=25,
                         txt_col=BLACK,
                         bg_col=BACKGROUND,
                         text="Game Menu",
                         bg_hover=buttonhover,
                         action=GameState.Home)
    Resume_Button = button(pos=(400, 400),
                          font_size=25,
                          txt_col=BLACK,
                          bg_col=BACKGROUND,
                          text="Resume Game",
                          bg_hover=buttonhover,
                          action=GameState.Play)
    Save_Button = button(pos=(400, 500),
                          font_size=25,
                          txt_col=BLACK,
                          bg_col=BACKGROUND,
                          text="Save Game",
                          bg_hover=buttonhover,
                          action=GameState.HowTo)
    Load_Button = button(pos=(400, 600),
                           font_size=25,
                           txt_col=BLACK,
                           bg_col=BACKGROUND,
                           text="Load Different Game",
                           bg_hover=buttonhover,
                           action=GameState.Pieces)
    Quit_Button = button(pos=(400, 700),
                         font_size=25,
                         txt_col=BLACK,
                         bg_col=BACKGROUND,
                         text="Quit Game",
                         bg_hover=buttonhover,
                         action=GameState.Quit)
    buttons = [Home_Button, Resume_Button, Save_Button, Load_Button, Quit_Button]
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
        pygame.draw.rect(screen, BLACK, pygame.Rect(200,200, 600, 600))
        for b in buttons:
            ui_action = b.moused_over(pygame.mouse.get_pos(),mouse_down)
            if ui_action is not None:
                return ui_action
            b.draw(screen)
        pygame.display.flip()