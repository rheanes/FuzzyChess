import pygame

pygame.init()
#tickrate
tickrate = 25
#screen dimensions
WIDTH = 1200  # screen width
HEIGHT = 1000 # screen height
GAME_WIDTH = 800


#fonts

fonttype = "menlo"
font = pygame.font.SysFont(fonttype, 45)
rulesfont = pygame.font.SysFont(fonttype, 20)

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
buttoncolor = (211, 211, 211)
buttonhover =  (222, 184, 135)
blackish = (10, 10, 10)
RED = (255, 0, 0) # highlight attack positions
BLUE = (50, 255, 255) # highlight potential positions
GREY = (128, 128, 128)
YELLOW = (204, 204, 0) # highlight pieces controlled by a commanders' pieces
BROWN = (222, 184, 135)
LIGHT_GRAY = (211, 211, 211)
BACKGROUND = (128, 0, 32)

#load images



