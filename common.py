import pygame

pygame.init()
#tickrate
tickrate = 25
#screen dimensions
WIDTH = 800  # screen width
HEIGHT = 800 # screen height

#button locations
ObjButtonLoc = [WIDTH / 6, HEIGHT / 8, 140, 40]
RuleButtonLoc = [WIDTH / 2, HEIGHT / 8, 140, 40]
PieceButtonLoc = [5*WIDTH / 6, HEIGHT / 8, 140, 40]

#fonts
font = pygame.font.SysFont("comicsansms", 30)
smallfont = pygame.font.SysFont("comicsansms", 30)

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
buttonhover = (112, 128, 144)
buttoncolor = (165, 175, 185)
blackish = (10, 10, 10)
RED = (255, 0, 0)
BROWN = (222, 184, 135)
LIGHT_GRAY = (211, 211, 211)

#load images



