import pygame.event
from guielements import *
from common import *


def MenuScene(screen):
    b_knight = Element("./Images/blue_knight.png", (WIDTH * 0.375, HEIGHT * 0.5))
    HeaderText = font.render("Medieval Fuzzy Logic Chess", True, BLACK)
    play_button = button(pos=(WIDTH * 0.75, HEIGHT * 0.375),
                         font_size=65,
                         txt_col=BLACK,
                         bg_col=buttoncolor,
                         text="Play",
                         bg_hover=buttonhover,
                         action=GameState.NewOrLoad)
    rules_button = button(pos=(WIDTH * 0.75, HEIGHT * 0.5),
                          font_size=65,
                          txt_col=BLACK,
                          bg_col=buttoncolor,
                          text="Rules",
                          bg_hover=buttonhover,
                          action=GameState.Rules)
    quit_button = button(pos=(WIDTH * 0.75, HEIGHT * 0.625),
                         font_size=65,
                         txt_col=BLACK,
                         bg_col=buttoncolor,
                         text="Quit",
                         bg_hover=buttonhover,
                         action=GameState.Quit)
    buttons = [play_button, rules_button, quit_button]
    while True:
        mouse_down = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        screen.fill(BACKGROUND)
        pygame.draw.lines(screen, BLACK, True, [(20, 20), (WIDTH - 20, 20), (WIDTH - 20, HEIGHT - 20),
                                                   (20, HEIGHT - 20)], width=4)
        b_knight.draw(screen)
        screen.blit(HeaderText, (50, HEIGHT / 8))
        for b in buttons:
            ui_action = b.moused_over(pygame.mouse.get_pos(),mouse_down)
            if ui_action is not None:
                return ui_action
            b.draw(screen)
        pygame.display.flip()

