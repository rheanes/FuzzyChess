import pygame
import sys
import common as cm
import random

attackMatrix = [[4, 4, 4, 4, 5, 0],
                [4, 4, 4, 4, 5, 2],
                [5, 5, 4, 5, 5, 3],
                [5, 5, 5, 5, 5, 2],
                [4, 4, 5, 4, 5, 5],
                [6, 6, 5, 6, 6, 4]]


# ------------------------------ACTUAL DICE ROLL ---------------------
def attackRoll():
    minRoll = 1
    maxRoll = 6
    roll = random.randint(minRoll, maxRoll)
    return roll


# Attack action. This is called whenever a piece wants to claim another piece.
# It takes the values of the attacker and defender, and references the attackMatrix
# for it's given roll. If it rolls at least the number in that matrix, then the piece
# should claim it. Thus we return true. If we don't, then we return false. We have
# an optional parameter (hasMoved) as well in the event a knight is the attacker.
# The knight tells the attack function it has moved, and gets a bonus to its move.

def attack(attacker: int,
           defender: int,
           hasMoved: bool = False) -> bool:
    num = attackRoll()
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


