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


def attack(attacker: int,
           defender: int) -> bool:
    num = attackRoll()
    if attackMatrix[attacker][defender] >= num:
        return True
    else:
        return False
