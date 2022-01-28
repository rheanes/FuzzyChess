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

def start_menu():
    startText = font.render('This is the text for the start menu', True, slategrey)

    while True:
        screen.fill((black))
        screen.blit(startText, ((screen_width - startText.get_width()) /2, 0))
        create_button('Button Text here', WIDTH - 130, 7, 125, 26, lightgrey, slategrey)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(15)
        return True

def First_Level():
    startText = font.render('This is the text for something', True, slategrey)
    while True:
        screen.fill(BLACK)
        screen.blit(startText, ((WIDTH - startText.get_width()) / 2 , 0))
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


