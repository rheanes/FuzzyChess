import common as cm
import sys
import pygame


pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((cm.WIDTH, cm.WIDTH))
pygame.display.set_caption('Midevil Fuzzy Logic Chess')

def create_button(msg, x, y, width, height, hovercolor, defaultcolor):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed(3)
    if x + width > mouse[0] > x and y + height > mouse[1] > y:
        pygame.draw.rect(screen, hovercolor, (x, y, width, height))
        if click[0] == 1:
            firstlevel()
    else:
        pygame.draw.rect(screen, defaultcolor, (x, y, width, height))
    startbuttontext = cm.smallfont.render(msg, True, cm.blackish)
    screen.blit(startbuttontext, (int(890 + (width / 2)), int(y + (y / 2))))

def start_menu():
    startText = cm.font.render('This is the text for the start menu', True, cm.slategrey)

    while True:
        screen.fill((cm.BLACK))
        screen.blit(startText, ((cm.WIDTH - startText.get_width()) /2, 0))
        create_button('Button Text here', cm.WIDTH - 130, 7, 125, 26, cm.lightgrey, cm.slategrey)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(15)
        return True

def firstlevel():
    startText = cm.font.render('This is the text for something', True, slategrey)
    while True:
        screen.fill(cm.BLACK)
        screen.blit(startText, ((cm.WIDTH - startText.get_width()) / 2 , 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(15)

while True:
    start_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(15)


