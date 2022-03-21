import enum
import board as bd
import pygame
"""
    ATTENTION: Fix the piece moves to return all highlighted squares
"""

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


class Action(enum.Enum):
    MOVE = 0
    ATTACK = 1

class Value(enum.Enum):
    KING = 20
    QUEEN = 18
    BISHOP = 15
    KNIGHT = 13
    ROOK = 10
    PAWN = 5

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
        self.delegated = False

    def switch_sprite(self, new_img):
        self.image = pygame.image.load(new_img)

#-------------COMMANDER STUFF IS HERE ------------

class Commander:
    def __init__(self, troops, leader) -> None:
        self.leader = leader
        self.troops = troops
        self.targets = []
        self.authority = True
        self.action = True
        self.has_moved = False

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
        #self.delegate_action = True

    #sub refers to sub commander
    def delegate(self, piece, sub):
        # if the piece is not delegated
        if piece.delegated == False and piece is not self.leader and piece in self.troops:
            piece.delegated = True
            self.troops.remove(piece)
            sub.troops.append(piece)
            self.use_turn()
        else:
            print("invalid target for delegation")
        #self.see_pieces

    def recall(self, piece, sub):
        # if the piece has already been delegated
        if piece.delegated == True and piece is not sub.leader and piece in sub.troops:
            piece.delegated = False
            sub.troops.remove(piece)
            self.troops.append(piece)
            self.use_turn()
            #self.see_pieces
"""
King commander must be able to delegate and undelegate pieces
"""
'''
orange_pieces = [board[0][1].piece, board[0][2].piece, board[1][0].piece, board[1][1].piece, board[1][2].piece]
orange_commander = Commander(orange_pieces, board[0][2].piece)
red_pieces = [board[0][0].piece, board[0][7].piece, board[0][3].piece, board[0][4].piece, board[1][3].piece, board[1][4].piece]
red_commander = King(red_pieces, board[0][4].piece)
yellow_pieces = [board[0][5].piece, board[0][6].piece, board[1][5].piece, board[1][6].piece, board[1][7].piece]
yellow_commander = Commander(yellow_pieces, board[0][5].piece)
blue_pieces = [board[7][4].piece, board[7][3].piece, board[7][0].piece, board[7][7].piece, board[6][3].piece, board[6][4].piece]
blue_commander = King(yellow_pieces, board[7][4])
green_pieces = [board[7][1].piece, board[7][2].piece, board[6][0].piece, board[6][1].piece, board[6][2].piece]
green_commander = Commander(yellow_pieces, board[7][2].piece)
purple_pieces = [board[7][5].piece, board[7][6].piece, board[6][5].piece, board[6][6].piece, board[6][7].piece]
purple_commander = Commander(yellow_pieces, board[7][5].piece)
orange_commander.see_pieces()
'''

enemies = {
    Team.BLUE : [Team.RED, Team.ORANGE, Team.YELLOW],
    Team.GREEN : [Team.RED, Team.ORANGE, Team.YELLOW],
    Team.PURPLE : [Team.RED, Team.ORANGE, Team.YELLOW],
    Team.RED : [Team.BLUE, Team.GREEN, Team.PURPLE],
    Team.ORANGE : [Team.BLUE, Team.GREEN, Team.PURPLE],
    Team.YELLOW : [Team.BLUE, Team.GREEN, Team.PURPLE]
}

"""
    Create instances of pieces.
    Only the original instances of pieces is required. 
    We will chaneg the colors of pieces upon delegation.
"""

coordinates = []

# returns input if it is within the boundries on the board
def on_board(position: tuple[int, int]):
    x, y = position
    """
    if -1 < position[0] < 8 and position[1] > -1 and position[-1] < 8:
        return True
    
    """
    if (-1 < x < 8) and (-1 < y < 8):
        return True

#----------_PAWN MOVES HERE--------------

def pawn_moves_top(position: tuple[int, int]): # team on the top
    row, col = position

    positions = []
    for i in range(3):
        curr_col = i + col - 1
        curr_row = row + 1
        if on_board((curr_col, curr_row)):
            # print('row', curr_row, 'col', curr_col)
            positions.append((curr_row, curr_col))

    return positions


# check pawn moves seperatly from other pieces. If space free then x to move.
# otherwise, the piece in front of it is targetable.
def pawn_moves_bottom(position: tuple[int, int]): # team on the bottom
    row, col = position

    positions = []
    for i in range(3):
        curr_col = i + col - 1
        curr_row = row - 1
        if on_board((curr_col, curr_row)):
            # print('row', curr_row, 'col', curr_col)
            positions.append((curr_row, curr_col))

    return positions

