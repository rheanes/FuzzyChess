from guielements import *
from common import *

def winLossScreen(screen, win):
    if (win == True):
        headerText = font.render("You Win", True, BLACK)
    else:
        headerText = font.render("You Lose", True, BLACK)
    homeButton = button(pos=(WIDTH * 0.2, 0.8 * HEIGHT), font_size=50, txt_col=BLACK, bg_col=buttoncolor,
                        text="Main Menu", bg_hover=buttonhover, action=GameState.Home)
    playButton = button(pos=(WIDTH * 0.8, 0.8 * HEIGHT), font_size=50, txt_col=BLACK, bg_col=buttoncolor,
                        text="Play again", bg_hover=buttonhover, action=GameState.Play)
    buttons = [homeButton, playButton]
    while True:
        #for event in pygame.event.get():
        #    if event.type == pygame.QUIT:
        #        pygame.quit()
        #        exit()
        mouse_down = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill(BACKGROUND)
        screen.blit(headerText, (50, HEIGHT / 8))
        for b in buttons:
            ui_action = b.moused_over(pygame.mouse.get_pos(),mouse_down)
            if ui_action is not None:
                return ui_action
            b.draw(screen)
        pygame.display.flip()