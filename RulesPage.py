import common
import sys
import pygame

common.init()
pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('Midevil Fuzzy Logic Chess')

def create_button(msg, x, y, width, height, hovercolor, defaultcolor):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hovercolor, (x, y, width, height))
        if click[0] == 1:
            first_level()
    else:
        pygame.draw.rect(screen, defaultcolor, (x, y, width, height))
    startbuttontext = smallfont.render(msg, True, blackish)
    screen.blit(startbuttontext, (int(890 + (width / 2)), int(y + (y / 2))))

