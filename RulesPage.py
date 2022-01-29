import common as cm
import sys
import pygame


pygame.init()
clock = pygame.time.Clock()

screen = pygame.display.set_mode((cm.WIDTH, cm.WIDTH))
pygame.display.set_caption('Midevil Fuzzy Logic Chess')

def start_menu():
    startText = cm.font.render("This is the text for the start menu", True, cm.WHITE)
    RulesPageText = cm.smallfont.render("Rules Page", True, cm.WHITE)
    while True:
        screen.fill((cm.BLACK))
        screen.blit(startText, ((cm.WIDTH - startText.get_width()) /2, 0))
        #button(left, top, width, height)
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if cm.WIDTH / 2 <= mouse[0] <= cm.WIDTH / 2 +140 and cm.WIDTH / 2 <= mouse[1] <= cm.WIDTH/2 +40:
                    rulespage()
        screen.fill(cm.blackish)
        if cm.WIDTH / 2 <= mouse[0] <= cm.WIDTH / 2 +140 and cm.WIDTH / 2 <= mouse[1] <= cm.WIDTH/2 +40:
            pygame.draw.rect(screen, cm.buttonhover, [cm.WIDTH/2, cm.WIDTH/2, 140, 40])
        else:
            pygame.draw.rect(screen, cm.buttoncolor, [cm.WIDTH/2, cm.WIDTH/2, 140, 40])
        screen.blit(RulesPageText, (cm.WIDTH/2 +30, cm.WIDTH/2))


        pygame.display.update()
        clock.tick(cm.tickrate)
        return True

def rulespage():
    HeaderText = cm.font.render("RULES PAGE", True, cm.WHITE)
    Tab1Text = cm.font.render("Objectives", True, cm.WHITE)
    Tab2Text = cm.font.render("Rules", True, cm.WHITE)
    Tab3Text = cm.font.render("Pieces", True, cm.WHITE)
    while True:
        screen.fill(cm.blackish)
        screen.blit(HeaderText, (cm.WIDTH / 2 , 0))
        screen.blit(Tab1Text, (200, 100))
        screen.blit(Tab2Text, (400, 100))
        screen.blit(Tab3Text, (600, 100))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clock.tick(cm.tickrate)

while True:
    start_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(cm.tickrate)


