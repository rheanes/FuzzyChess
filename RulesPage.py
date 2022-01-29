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
        mouse = pygame.mouse.get_pos()
        screen.fill((cm.BLACK))
        screen.blit(startText, ((cm.WIDTH - startText.get_width()) /2, 0))
        #button(left, top, width, height)
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
        #follow mouse
        mouse = pygame.mouse.get_pos()
        #first color the screen and add headers.
        screen.fill(cm.blackish)
        screen.blit(HeaderText, (cm.WIDTH / 2 , 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #if u click on objective tab, open objective tab
                if cm.ObjButtonLoc[0] <= mouse[0] <= cm.ObjButtonLoc[0] + cm.ObjButtonLoc[2] and \
                        cm.ObjButtonLoc[1] <= mouse[1] <= cm.ObjButtonLoc[1] + cm.ObjButtonLoc[3]:
                    ObjectiveTab()
                #if u click on RulesTab, open Rules Tab
                if cm.RuleButtonLoc[0] <= mouse[0] <= cm.RuleButtonLoc[0] + cm.RuleButtonLoc[2] and \
                        cm.RuleButtonLoc[1] <= mouse[1] <= cm.RuleButtonLoc[1] + cm.RuleButtonLoc[3]:
                    RulesTab()
                #If u click on Pieces Tab, Open Pieces Tab
                if cm.PieceButtonLoc[0] <= mouse[0] <= cm.PieceButtonLoc[0] + cm.PieceButtonLoc[2] and \
                        cm.PieceButtonLoc[1] <= mouse[1] <= cm.PieceButtonLoc[1] + cm.PieceButtonLoc[3]:
                    PiecesTab()
            #if u are hovering Objective Tab
        if cm.ObjButtonLoc[0] <= mouse[0] <= cm.ObjButtonLoc[0] + cm.ObjButtonLoc[2] and\
                cm.ObjButtonLoc[1] <= mouse[1] <= cm.ObjButtonLoc[1] + cm.ObjButtonLoc[3]:
            pygame.draw.rect(screen, cm.buttonhover, cm.ObjButtonLoc)
            pygame.draw.rect(screen, cm.buttoncolor, cm.RuleButtonLoc)
            pygame.draw.rect(screen, cm.buttoncolor, cm.PieceButtonLoc)
            # if u are hovering Rules Tab
        elif cm.RuleButtonLoc[0] <= mouse[0] <= cm.RuleButtonLoc[0] + cm.RuleButtonLoc[2] and \
                cm.RuleButtonLoc[1] <= mouse[1] <= cm.RuleButtonLoc[1] + cm.RuleButtonLoc[3]:
            pygame.draw.rect(screen, cm.buttoncolor, cm.ObjButtonLoc)
            pygame.draw.rect(screen, cm.buttonhover, cm.RuleButtonLoc)
            pygame.draw.rect(screen, cm.buttoncolor, cm.PieceButtonLoc)
            # if u are hovering Pieces Tab
        elif cm.PieceButtonLoc[0] <= mouse[0] <= cm.PieceButtonLoc[0] + cm.PieceButtonLoc[2] and \
                cm.PieceButtonLoc[1] <= mouse[1] <= cm.PieceButtonLoc[1] + cm.PieceButtonLoc[3]:
            pygame.draw.rect(screen, cm.buttoncolor, cm.ObjButtonLoc)
            pygame.draw.rect(screen, cm.buttoncolor, cm.RuleButtonLoc)
            pygame.draw.rect(screen, cm.buttonhover, cm.PieceButtonLoc)
            #if not hovering any, then just put buttons there.
        else:
                pygame.draw.rect(screen, cm.buttoncolor, cm.ObjButtonLoc)
                pygame.draw.rect(screen, cm.buttoncolor, cm.RuleButtonLoc)
                pygame.draw.rect(screen, cm.buttoncolor, cm.PieceButtonLoc)
        screen.blit(Tab1Text, (cm.WIDTH / 6, 100))
        screen.blit(Tab2Text, (cm.WIDTH / 2, 100))
        screen.blit(Tab3Text, (5 * cm.WIDTH / 6, 100))


        pygame.display.update()
        clock.tick(cm.tickrate)

while True:
    rulespage()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    clock.tick(cm.tickrate)


