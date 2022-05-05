from cmath import inf
import enum
import pygame
import random
from common import *


"""
    ATTENTION: Fix the piece moves to return all highlighted squares
"""
#called during evaluation for each piece. represents positions on board and rewards/punishes ai for moving pieces in certain positions

pawn_pos_table = [[0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 10, 10, 10, 0, 0],
                        [4, 4, 4, 4, 4, 4, 4, 4],
                        [4, 4, 4, 4, 4, 4, 4, 4],
                        [4, 4, 4, 4, 4, 4, 4, 4],
                        [4, 4, 4, 4, 4, 4, 4, 4],
                        [-5, -5, -5, -5, -5, -5, -5, -5],
                        [-10, -10, -10, -10, -10, -10, -10, -10]]


rook_pos_table = [[0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 5, 6, 4, 4, 6, 5, 1],
                  [1, 5, 10, 10, 10, 10, 5, 1],
                  [1, 5, 10, 10, 10, 10, 5, 1],
                  [1, 5, 9, 9, 9, 9, 5, 1],
                  [1, 5, 7, 7, 7, 7, 5, 1],
                  [1, 5, 5, 5, 5, 5, 5, 1],
                  [0, 0, 0, 0, 0, 0, 0, 0]]

bishop_pos_table = [[0, 0, 3, 10, 0, 10, 0, 0],
                  [2, 2, 2, 2, 2, 2, 2, 2],
                  [2, 2, 2, 2, 2, 2, 2, 2],
                  [2, 2, 2, 2, 2, 2, 2, 2],
                  [2, 2, 2, 2, 2, 2, 2, 2],
                  [2, 2, 2, 2, 2, 2, 2, 2],
                  [2, 2, 2, 2, 2, 2, 2, 2],
                  [2, 2, 2, 2, 2, 2, 2, 2]]

knight_pos_table = [[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 5, 5, 5, 5, 5, 5, 0],
                  [0, 5, 7, 7, 7, 7, 5, 0],
                  [0, 5, 7, 10, 10, 7, 5, 0],
                  [0, 5, 7, 10, 10, 7, 5, 0],
                  [0, 5, 7, 7, 7, 7, 5, 0],
                  [0, 5, 5, 5, 5, 5, 5, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]]

queen_pos_table = [[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 5, 5, 5, 5, 5, 5, 0],
                  [0, 5, 7, 7, 7, 7, 5, 0],
                  [0, 5, 7, 10, 10, 7, 5, 0],
                  [0, 5, 7, 9, 9, 7, 5, 0],
                  [0, 5, 7, 7, 7, 7, 5, 0],
                  [0, 5, 5, 5, 5, 5, 5, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]]

king_pos_table = [[1, 1, 1, 1, 10, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1]]


class Action(enum.Enum):
    MOVE = 0
    ATTACK = 1
    DELEGATE = 2
    RECALL = 3
    PASS = 4

class CommanderMessage:
    def __init__(self, comm, message):
        self.commander = comm
        self.message = message

class PieceAction:
    def __init__(self, action: Action, square=None):
        self.action = action
        self.square = square

class Value(enum.Enum):
    KING = 1000000
    QUEEN = 300
    BISHOP = 800
    KNIGHT = 500
    ROOK = 200
    PAWN = 50

class DecisionMode(enum.Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2
    EXTRA_HARD = 3

class Team(enum.Enum):
    # Player AI
    YELLOW = 0
    RED = 1
    ORANGE = 2
    # Player Human
    PURPLE = 3
    BLUE = 4
    GREEN = 5


class Type(enum.Enum):
    KING = 0
    QUEEN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    PAWN = 5

enemies = {
    Team.BLUE : [Team.RED, Team.ORANGE, Team.YELLOW],
    Team.GREEN : [Team.RED, Team.ORANGE, Team.YELLOW],
    Team.PURPLE : [Team.RED, Team.ORANGE, Team.YELLOW],
    Team.RED : [Team.BLUE, Team.GREEN, Team.PURPLE],
    Team.ORANGE : [Team.BLUE, Team.GREEN, Team.PURPLE],
    Team.YELLOW : [Team.BLUE, Team.GREEN, Team.PURPLE]
}

moveVal = {
        Type.KNIGHT:  10,
        Type.ROOK:   9,
        Type.QUEEN:   8,
        Type.PAWN:   3,
        Type.BISHOP:   4,
        Type.KING:   5,
}
#following dictionaries associate enemy piece type with the probability of successful capture for each piece type
pawn_atk_chnc = {Type.KING: 0.17,
                Type.QUEEN: 0.17,
                Type.KNIGHT: 0.17,
                Type.BISHOP: 0.33,
                Type.ROOK: 0.17,
                Type.PAWN: 0.5}

king_atk_chnc = {Type.KING: 0.5,
                Type.QUEEN: 0.5,
                Type.KNIGHT: 0.5,
                Type.BISHOP: 0.5,
                Type.ROOK: 0.33,
                Type.PAWN: 1.0}
queen_atk_chnc = {Type.KING: 0.5,
                Type.QUEEN: 0.5,
                Type.KNIGHT: 0.5,
                Type.BISHOP: 0.5,
                Type.ROOK: 0.33,
                Type.PAWN: 0.83}
#add 0.17 to chance when knight has moved before attacking
knight_atk_chnc = {Type.KING: 0.33,
                Type.QUEEN: 0.33,
                Type.KNIGHT: 0.33,
                Type.BISHOP: 0.33,
                Type.ROOK: 0.33,
                Type.PAWN: 0.83}

bishop_atk_chnc = {Type.KING: 0.33,
                Type.QUEEN: 0.33,
                Type.KNIGHT: 0.33,
                Type.BISHOP: 0.5,
                Type.ROOK: 0.33,
                Type.PAWN: 0.67}

rook_atk_chnc = {Type.KING: 0.5,
                Type.QUEEN: 0.5,
                Type.KNIGHT: 0.5,
                Type.BISHOP: 0.33,
                Type.ROOK: 0.33,
                Type.PAWN: 0.33}



#creates a chess piece class that shows:
#team, attackable, and color
class Piece:
    def __init__(self, team, type, image, value, delegated):
        super().__init__()
        self.team = team
        self.type = type
        self.action = None
        self.image = image
        self.value = value
        self.targets = []
        self.delegated = False
        self.pos = None

    def switch_sprite(self, new_img):
        self.image = pygame.image.load(new_img)

    # for ai, checks to see if there are enemies in the pieces attack range. If there are, add them to targets and return targets
    def detect_targets(self, board, positions: tuple[int, int], team: Team):
        for row, col in positions:
            if board[row][col].piece is not None:
                if board[row][col].piece.team in enemies[team]:
                    self.targets.append(board[row][col].piece)
                    print("hi")
        return self.targets

#-------------COMMANDER STUFF IS HERE ------------
# TODO:
#  1) check if troop are being attacked
#  2) is 1) is true then
class Commander:
    def __init__(self, troops, leader) -> None:
        self.leader = leader
        self.troops = troops
        self.targets = []
        self.authority = True
        self.action = True
        self.has_moved = False
        self.knight_special_move = False

    def update_commander(self, commander):
        self.leader = commander.leader
        self.troops = commander.troops
        self.targets = commander.targets
        self.authority = commander.authority
        self.action = commander.action
        self.has_moved = commander.action


    def see_pieces(self):
        for i in range(len(self.troops)):
            print(self.troops[i].type)


    def use_turn(self):
        self.action = False

    def commander_lost(self):
        if self.leader not in self.troops:
            self.authority = False


"""
Each commander needs to know their living troops
Also needs to know all targets in range of troops
Needs to keep track of authority or action it posseses
"""
class King(Commander):
    def __init__(self, troops, leader):
        Commander.__init__(self, troops, leader)
        self.message = None
        #self.delegate_action = True

    #sub refers to sub commander
    def delegate(self, piece, sub):
        # if the piece is not delegated
        if piece.delegated == False and piece is not self.leader and piece in self.troops:
            piece.delegated = True
            self.troops.remove(piece)
            sub.troops.append(piece)
        else:
            print("invalid target for delegation")
        

    def recall(self, piece, sub):
        # if the piece has already been delegated
        if piece.delegated == True and piece is not sub.leader and piece in sub.troops:
            piece.delegated = False
            sub.troops.remove(piece)
            self.troops.append(piece)
            


color_matrix_bishop = {Team.GREEN: './Images/green_bishop.png',
                       Team.PURPLE: './Images/purple_bishop.png',
                       Team.ORANGE: './Images/orange_bishop.png',
                       Team.YELLOW: './Images/yellow_bishop.png',
                       Team.RED: './Images/red_bishop.png',
                       Team.BLUE: './Images/blue_bishop.png'
}
color_matrix_king = {Team.BLUE: './Images/blue_king.png',
                     Team.RED: './Images/red_king.png'
}
color_matrix_pawn = {Team.BLUE: './Images/blue_pawn.png',
                     Team.GREEN: './Images/green_pawn.png',
                     Team.PURPLE: './Images/purple_pawn.png',
                     Team.RED: './Images/red_pawn.png',
                     Team.YELLOW: './Images/yellow_pawn.png',
                     Team.ORANGE: './Images/orange_pawn.png'}

color_matrix_knight = {Team.BLUE: './Images/blue_knight.png',
                       Team.GREEN: './Images/green_knight.png',
                       Team.PURPLE: './Images/purple_knight.png',
                       Team.RED: './Images/red_knight.png',
                       Team.YELLOW: './Images/yellow_knight.png',
                       Team.ORANGE: './Images/orange_knight.png'
                       }

color_matrix_queen = {Team.BLUE: './Images/blue_queen.png',
                      Team.GREEN: './Images/green_queen.png',
                      Team.PURPLE: './Images/purple_queen.png',
                      Team.RED: './Images/red_queen.png',
                      Team.YELLOW: './Images/yellow_queen.png',
                      Team.ORANGE: './Images/orange_queen.png'
                      }

color_matrix_rook = {Team.BLUE: './Images/blue_rook.png',
                     Team.GREEN: './Images/green_rook.png',
                     Team.PURPLE: './Images/purple_rook.png',
                     Team.RED: './Images/red_rook.png',
                     Team.ORANGE: './Images/orange_rook.png',
                     Team.YELLOW: './Images/yellow_rook.png'}

del_matrix_pawn = {Team.GREEN: './Images/green_pawn_d.png',
                     Team.PURPLE: './Images/purple_pawn_d.png',
                     Team.ORANGE: './Images/orange_pawn_d.png',
                     Team.YELLOW: './Images/yellow_pawn_d.png',
                     Team.BLUE: './Images/blue_pawn.png',
                     Team.RED: './Images/red_pawn.png'}

del_matrix_knight = {Team.GREEN: './Images/green_knight_d.png',
                     Team.PURPLE: './Images/purple_knight_d.png',
                     Team.ORANGE: './Images/orange_knight_d.png',
                     Team.YELLOW: './Images/yellow_knight_d.png',
                     Team.BLUE: './Images/blue_knight.png',
                     Team.RED: './Images/red_knight.png'}

del_matrix_rook = {Team.GREEN: './Images/green_rook_d.png',
                     Team.PURPLE: './Images/purple_rook_d.png',
                     Team.ORANGE: './Images/orange_rook_d.png',
                     Team.YELLOW: './Images/yellow_rook_d.png',
                     Team.BLUE: './Images/blue_rook.png',
                     Team.RED: './Images/red_rook.png'}

del_matrix_queen = {Team.BLUE: './Images/blue_queen.png',
                      Team.GREEN: './Images/green_queen.png',
                      Team.PURPLE: './Images/purple_queen.png',
                      Team.RED: './Images/red_queen.png',
                      Team.YELLOW: './Images/yellow_queen.png',
                      Team.ORANGE: './Images/orange_queen.png',
                      Team.RED: './Images/red_queen.png'
                      }
"""
    Create instances of pieces.
    Only the original instances of pieces is required. 
    We will chaneg the colors of pieces upon delegation.
"""

coordinates = []

#declare all of the pieces here
rr1 = Piece(Team.RED, Type.ROOK, pygame.image.load('./Images/red_rook.png'), Value.ROOK, False)
ok = Piece(Team.ORANGE, Type.KNIGHT, pygame.image.load('./Images/orange_knight.png'), Value.KNIGHT, False)
ob = Piece(Team.ORANGE, Type.BISHOP, pygame.image.load('./Images/orange_bishop.png'), Value.BISHOP, False)
rK = Piece(Team.RED, Type.KING, pygame.image.load('./Images/red_king.png'), Value.KING, False)
rq = Piece(Team.RED, Type.QUEEN, pygame.image.load('./Images/red_queen.png'), Value.QUEEN, False)
yk = Piece(Team.YELLOW, Type.KNIGHT, pygame.image.load('./Images/yellow_knight.png'), Value.KNIGHT, False)
yb = Piece(Team.YELLOW, Type.BISHOP, pygame.image.load('./Images/yellow_bishop.png'), Value.BISHOP, False)
rr2 = Piece(Team.RED, Type.ROOK, pygame.image.load('./Images/red_rook.png'), Value.ROOK, False)

rp1 = Piece(Team.RED, Type.PAWN, pygame.image.load('./Images/red_pawn.png'), Value.PAWN, False)
rp2 = Piece(Team.RED, Type.PAWN, pygame.image.load('./Images/red_pawn.png'), Value.PAWN, False)
op1 = Piece(Team.ORANGE, Type.PAWN, pygame.image.load('./Images/orange_pawn.png'), Value.PAWN, False)
op2 = Piece(Team.ORANGE, Type.PAWN, pygame.image.load('./Images/orange_pawn.png'), Value.PAWN, False)
op3 = Piece(Team.ORANGE, Type.PAWN, pygame.image.load('./Images/orange_pawn.png'), Value.PAWN, False)
yp1 = Piece(Team.YELLOW, Type.PAWN, pygame.image.load('./Images/yellow_pawn.png'), Value.PAWN, False)
yp2 = Piece(Team.YELLOW, Type.PAWN, pygame.image.load('./Images/yellow_pawn.png'), Value.PAWN, False)
yp3 = Piece(Team.YELLOW, Type.PAWN, pygame.image.load('./Images/yellow_pawn.png'), Value.PAWN, False)

br1 = Piece(Team.BLUE, Type.ROOK, pygame.image.load('./Images/blue_rook.png'), Value.ROOK, False)
gk = Piece(Team.GREEN, Type.KNIGHT, pygame.image.load('./Images/green_knight.png'), Value.KNIGHT, False)
gb = Piece(Team.GREEN, Type.BISHOP, pygame.image.load('./Images/green_bishop.png'), Value.BISHOP, False)
bq = Piece(Team.BLUE, Type.QUEEN, pygame.image.load('./Images/blue_queen.png'), Value.QUEEN, False)
bK = Piece(Team.BLUE, Type.KING, pygame.image.load('./Images/blue_king.png'), Value.KING, False)
pb = Piece(Team.PURPLE, Type.BISHOP, pygame.image.load('./Images/purple_bishop.png'), Value.BISHOP, False)
pk = Piece(Team.PURPLE, Type.KNIGHT, pygame.image.load('./Images/purple_knight.png'), Value.KNIGHT, False)
br2 = Piece(Team.BLUE, Type.ROOK, pygame.image.load('./Images/blue_rook.png'), Value.ROOK, False)

bp1 = Piece(Team.BLUE, Type.PAWN, pygame.image.load('./Images/blue_pawn.png'), Value.PAWN, False)
bp2 = Piece(Team.BLUE, Type.PAWN, pygame.image.load('./Images/blue_pawn.png'), Value.PAWN, False)
gp1 = Piece(Team.GREEN, Type.PAWN, pygame.image.load('./Images/green_pawn.png'), Value.PAWN, False)
gp2 = Piece(Team.GREEN, Type.PAWN, pygame.image.load('./Images/green_pawn.png'), Value.PAWN, False)
gp3 = Piece(Team.GREEN, Type.PAWN, pygame.image.load('./Images/green_pawn.png'), Value.PAWN, False)
pp1 = Piece(Team.PURPLE, Type.PAWN, pygame.image.load('./Images/purple_pawn.png'), Value.PAWN, False)
pp2 = Piece(Team.PURPLE, Type.PAWN, pygame.image.load('./Images/purple_pawn.png'), Value.PAWN, False)
pp3 = Piece(Team.PURPLE, Type.PAWN, pygame.image.load('./Images/purple_pawn.png'), Value.PAWN, False)

#declare teams here
orange_pieces = [op1, op2, op3, ok]
red_pieces = [rp1, rp2, rr1, rr2, rq]
yellow_pieces = [yp1, yp2, yp3, yk]
blue_pieces = []
green_pieces = []
purple_pieces = []
player_delegated_pieces = []
ai_delegated_pieces = []
player_captured_pieces = []
ai_captured_pieces = []
#declare commanders here
orange_commander = Commander(orange_pieces, ob)
red_commander = King(red_pieces, rK)
yellow_commander = Commander(yellow_pieces, yb)
blue_commander = King(blue_pieces, bK)
green_commander = Commander(green_pieces, gb)
purple_commander = Commander(purple_pieces, pb)

player_commanders = [green_commander, blue_commander, purple_commander]
ai_commanders = [orange_commander, red_commander, yellow_commander]

def ReCommand():
    if orange_commander not in ai_commanders:
        ai_commanders.append(orange_commander)
    if yellow_commander not in ai_commanders:
        ai_commanders.append(yellow_commander)
    if green_commander not in player_commanders:
        player_commanders.append(green_commander)
    if purple_commander not in player_commanders:
        player_commanders.append(purple_commander)


# returns input if it is within the boundries on the board
def on_board(position: tuple[int, int]):
    x = position[0]
    y = position[1]
   
    if (-1 < x < 8) and (-1 < y < 8):
        return True
    else:
        return False

