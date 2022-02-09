import common as cm
from guielements import *
from rulepage import rulespage
from basechessgame import playgame
clock = pygame.time.Clock()
screen = pygame.display.set_mode((cm.WIDTH, cm.WIDTH))
pygame.display.set_caption('Medieval Fuzzy Logic Chess')

while True:
    b_knight = Element("./Images/blue_knight.png", (cm.WIDTH * 0.375, cm.HEIGHT * 0.5))
    b_knight.scale(400, 400)

    play_button = button(pos=(cm.WIDTH * 0.75, cm.HEIGHT * 0.375), font_size=50, txt_col=cm.BLACK, bg_col=cm.LIGHT_GRAY,
                         text="Play")
    rules_button = button(pos=(cm.WIDTH * 0.75, cm.HEIGHT * 0.5), font_size=50, txt_col=cm.BLACK, bg_col=cm.BROWN,
                          text="Rules")
    quit_button = button(pos=(cm.WIDTH * 0.75, cm.HEIGHT * 0.625), font_size=50, txt_col=cm.BLACK, bg_col=cm.RED,
                         text="Quit Game")
    yeet = [play_button, rules_button, quit_button]
    while True:
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if quit_button.selected:
                    pygame.quit()
                    sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                if rules_button.selected:
                    rulespage(screen)
            if event.type == MOUSEBUTTONDOWN:
                if play_button.selected:
                    playgame(screen)
        screen.fill(cm.WHITE)
        b_knight.draw(screen)

        for yee in yeet:
            yee.moused_over(pygame.mouse.get_pos())
            yee.draw(screen)

        pygame.display.update()
        clock.tick(cm.tickrate)