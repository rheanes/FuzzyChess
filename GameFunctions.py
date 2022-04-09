import pygame
import sys
from common import *
import random
from guielements import *

attackMatrix = [[4, 4, 4, 4, 5, 0],
                [4, 4, 4, 4, 5, 2],
                [5, 5, 4, 5, 5, 3],
                [5, 5, 5, 5, 5, 2],
                [4, 4, 5, 4, 5, 5],
                [6, 6, 5, 6, 6, 4]]


# ------------------------------ACTUAL DICE ROLL --------------------- #
def attackAnimation(screen, roll: int):
    dieImage1 = pygame.image.load('./Images/dieFace1.png')
    dieImage2 = pygame.image.load('./Images/dieFace2.png')
    dieImage3 = pygame.image.load('./Images/dieFace3.png')
    dieImage4 = pygame.image.load('./Images/dieFace4.png')
    dieImage5 = pygame.image.load('./Images/dieFace5.png')
    dieImage6 = pygame.image.load('./Images/dieFace6.png')
    dieImages = [dieImage1, dieImage2, dieImage3, dieImage4, dieImage5, dieImage6]
    cycles = 3
    dieImage = dieImages[roll - 1]
    while True:
        mouse_down = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        okButton = button(pos=(275, 400),
                         font_size=65,
                         txt_col=BLACK,
                         bg_col=buttoncolor,
                         text="ok",
                         bg_hover=buttonhover,
                         action=GameState.Play)

        pygame.draw.rect(screen, BLACK, pygame.Rect(75, 75, 400, 400))
        while cycles > 0:
            for i in dieImages:
                screen.blit(i, (225, 200))
                pygame.display.flip()
                pygame.time.delay(100)
            cycles = cycles - 1
        screen.blit(dieImage, (225, 200))
        ui_action = okButton.moused_over(pygame.mouse.get_pos(), mouse_down)
        if ui_action is not None:
            return ui_action
        okButton.draw(screen)
        pygame.display.flip()

def attackRoll(screen):
    minRoll = 1
    maxRoll = 6
    roll = random.randint(minRoll, maxRoll)
    attackAnimation(screen, roll)
    return roll


# Attack action. This is called whenever a piece wants to claim another piece.
# It takes the values of the attacker and defender, and references the attackMatrix
# for it's given roll. If it rolls at least the number in that matrix, then the piece
# should claim it. Thus we return true. If we don't, then we return false. We have
# an optional parameter (hasMoved) as well in the event a knight is the attacker.
# The knight tells the attack function it has moved, and gets a bonus to its move.

def attack(screen, attacker: int, defender: int, hasMoved: bool = False) -> bool:
    num = attackRoll(screen)
    if hasMoved:
        if num + 1 >= attackMatrix[attacker][defender]:
            return True
        else:
            return False

    else:
        if num >= attackMatrix[attacker][defender]:
            return True
        else:
            return False


