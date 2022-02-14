import pygame

pygame.init()
#tickrate
tickrate = 25
#screen dimensions
WIDTH = 1000  # screen width
HEIGHT = 800 # screen height
GAME_WIDTH = 800


#fonts
font = "Arial"
smallfont = pygame.font.SysFont("Arial", 30)
rulesfont = pygame.font.SysFont("Arial", 18)

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
buttoncolor = (112, 128, 144)
buttonhover = (165, 175, 185)
blackish = (10, 10, 10)
RED = (255, 0, 0) # highlight attack positions
BLUE = (50, 255, 255) # highlight potential positions
GREY = (128, 128, 128)
YELLOW = (204, 204, 0) # highlight pieces controlled by a commanders' pieces
BROWN = (222, 184, 135)
LIGHT_GRAY = (211, 211, 211)
BACKGROUND = (128, 0, 32)

#load images



