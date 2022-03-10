from Scenes.RulesPageCommon import *
from guielements import *
from common import *

def LoadScene(screen):
    Page_Title = font.render("Choose a game to load", True, BLACK)
    Home_Button = button((WIDTH - 150, HEIGHT / 10 - 50),
                         font_size=25,
                         txt_col=BLACK,
                         bg_col=BACKGROUND,
                         text="Home",
                         bg_hover=buttonhover,
                         action=GameState.Home)
    Load1_Button = button((WIDTH - 150, HEIGHT / 10 - 50),
                         font_size=25,
                         txt_col=BLACK,
                         bg_col=BACKGROUND,
                         text="Home",
                         bg_hover=buttonhover,
                         action=GameState.Load1)
    Load2_Button = button((WIDTH - 150, HEIGHT / 10 - 50),
                         font_size=25,
                         txt_col=BLACK,
                         bg_col=BACKGROUND,
                         text="Home",
                         bg_hover=buttonhover,
                         action=GameState.Load2)
    Load3_Button = button((WIDTH-150, HEIGHT/10-50),
                     font_size=25,
                     txt_col=BLACK,
                     bg_col=BACKGROUND,
                     text="Home",
                     bg_hover= buttonhover,
                     action= GameState.Load3)
    buttons = [Home_Button, Load1_Button, Load2_Button, Load3_Button]
    while True:
        mouse_down = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        drawscreen(screen, Page_Title, Page_Title)
        for b in buttons:
            ui_action = b.moused_over(pygame.mouse.get_pos(),mouse_down)
            if ui_action is not None:
                return ui_action
            b.draw(screen)
        pygame.display.flip()