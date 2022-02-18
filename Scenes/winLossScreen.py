from guielements import *


def winLossScreen(screen, win):
    if (win == True):
        headerText = cm.font.render("You Win", True, cm.black)
    else:
        headerText = cm.font.render("You Lose", True, cm.black)
    homeButton = button(pos=(cm.WIDTH * 0.2, 0.8 * cm.HEIGHT), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                        text="Main Menu", bg_hover=cm.buttonhover)
    playButton = button(pos=(cm.WIDTH * 0.8, 0.8 * cm.HEIGHT), font_size=50, txt_col=cm.BLACK, bg_col=cm.buttoncolor,
                        text="Play again", bg_hover=cm.buttonhover)
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
        screen.fill(cm.BACKGROUND)
        pygame.display.flip()