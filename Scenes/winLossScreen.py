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
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if homeButton.selected:
                    # return to main menu
                if playButton.selected:
                    # start a new game
        screen.fill(BACKGROUND)
        pygame.display.flip()