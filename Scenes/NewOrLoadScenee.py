from guielements import *
from common import *

def NewOrLoadScene(screen):
    Page_Title = font.render("How to Play", True, BLACK)
    Home_Button = button((WIDTH - 150, HEIGHT / 10 - 50),
                         font_size=25,
                         txt_col=BLACK,
                         bg_col=BACKGROUND,
                         text="Home",
                         bg_hover=buttonhover,
                         action=GameState.Home)