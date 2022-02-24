<<<<<<<< HEAD:GameFunctions.py
import pygame
import sys
import common as cm
import random
 #------------------------------ACTUAL DICE ROLL ---------------------
def attack():
    attackRoll = 0
    min = 1
    max = 6
    attackRoll = random.randint(min, max)
    return attackRoll
========

>>>>>>>> origin/main:attackRolls.py
