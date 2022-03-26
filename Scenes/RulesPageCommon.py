import pygame.draw_py

from guielements import *
from common import *

Home_Button = button((WIDTH-150, HEIGHT/10-50),
                     font_size=25,
                     txt_col=BLACK,
                     bg_col=BACKGROUND,
                     text="Home",
                     bg_hover= buttonhover,
                     action= GameState.Home)
Rules_Button = button(pos=(70, 2*HEIGHT/12),
                 font_size=25,
                 txt_col=BLACK,
                 bg_col = BACKGROUND,
                 text="Rules" ,
                 bg_hover= buttonhover,
                 action=GameState.Rules)
HowTo_Button = button(pos=(70, 3*HEIGHT / 12),
                 font_size=25,
                 txt_col=BLACK,
                 bg_col = BACKGROUND,
                 text="How2Play" ,
                 bg_hover= buttonhover,
                 action=GameState.HowTo)
Pieces_Button = button(pos=(70, 4* HEIGHT / 12),
                 font_size=25,
                 txt_col=BLACK,
                 bg_col = BACKGROUND,
                 text="Pieces" ,
                 bg_hover= buttonhover,
                 action=GameState.Pieces)
Pawn_Button = button(pos=(70, 5* HEIGHT / 12),
                 font_size=25,
                 txt_col=BLACK,
                 bg_col = BACKGROUND,
                 text="Pawns" ,
                 bg_hover= buttonhover,
                 action=GameState.Pawn)
Knight_Button = button(pos=(70, 6*HEIGHT / 12),
                 font_size=25,
                 txt_col=BLACK,
                 bg_col = BACKGROUND,
                 text="Knights" ,
                 bg_hover= buttonhover,
                 action=GameState.Knight)
Rook_button = button(pos=(70, 7* HEIGHT / 12),
                 font_size=25,
                 txt_col=BLACK,
                 bg_col = BACKGROUND,
                 text="Rooks" ,
                 bg_hover= buttonhover,
                 action=GameState.Rook)
Queen_Button = button(pos=(70, 8* HEIGHT / 12),
                 font_size=25,
                 txt_col=BLACK,
                 bg_col = BACKGROUND,
                 text="Queens" ,
                 bg_hover= buttonhover,
                 action=GameState.Queen)
Bishop_Button = button(pos=(70, 9* HEIGHT/ 12),
                 font_size=25,
                 txt_col=BLACK,
                 bg_col = BACKGROUND,
                 text="Bishops" ,
                 bg_hover= buttonhover,
                 action=GameState.Bishop)
King_Button = button(pos=(70, 10* HEIGHT/12 ),
                 font_size=25,
                 txt_col=BLACK,
                 bg_col = BACKGROUND,
                 text="Kings" ,
                 bg_hover= buttonhover,
                 action=GameState.King)


tabs = [Home_Button, Rules_Button, HowTo_Button, Pieces_Button,
        Pawn_Button, Rook_button, Knight_Button, Queen_Button, Bishop_Button, King_Button]

positions3 = [(3/8*WIDTH, 5/8*HEIGHT),
              (5/8*WIDTH, 5/8*HEIGHT),
              (7/8*WIDTH, 5/8*HEIGHT)]
positions6 = [(WIDTH / 6, 5 / 8 * HEIGHT), (WIDTH / 3, 5 / 8 * HEIGHT),
                 (WIDTH / 2, 5 / 8 * HEIGHT),
                 (2 / 3 * WIDTH, 5 / 8 * HEIGHT), (5 / 6 * WIDTH, 5 / 8 * HEIGHT),
                 (WIDTH, 5 / 8 * HEIGHT)]

positions4 = [(WIDTH / 3, 5 / 8 * HEIGHT), (WIDTH / 2, 5 / 8 * HEIGHT),
                 (WIDTH * 2 / 3, 5 / 8 * HEIGHT), (5 / 6 * WIDTH, 5 / 8 * HEIGHT)]

positions2 = [(WIDTH / 4, 5 / 8 * HEIGHT), (WIDTH * 3 / 4, 5 / 8 * HEIGHT)]

def rules_multiline_text(text):
    pos = 175, 175
    out = []
    for t in text:
        out.append(rulesfont.render(t, True, LIGHT_GRAY))
    return out, pos


def drawscreen(screen, Page_Title, Page_Text):
    #set background color
    screen.fill(BACKGROUND)
    #draw lines around the screen
    pygame.draw.lines(screen, BLACK, True,[(2, 2), (WIDTH - 2, 2), (WIDTH-2, HEIGHT-2), (2, HEIGHT-2)], width=4)
    #draw line to under title
    pygame.draw.line(screen, BLACK, (0, HEIGHT/10 + 50), (WIDTH, HEIGHT/10 + 50), width = 4)
    pygame.draw.line(screen, BLACK, (140, 0), (140, HEIGHT ), width=4)

    #Write Page title
    screen.blit(Page_Title, (WIDTH /2 - 50, HEIGHT / 12))
    #write page content
    text_label , text_pos = rules_multiline_text(Page_Text)
    for line in range(len(text_label)):
        screen.blit(text_label[line], (text_pos[0], text_pos[1] + (line * 30) + (5 * line)))
