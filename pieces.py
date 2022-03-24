import enum
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
    KING = 1000
    QUEEN = 200
    BISHOP = 400
    KNIGHT = 200
    ROOK = 200
    PAWN = 50

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
                     Team.PURPLE: './Images/purple_pawn_d.png'}

del_matrix_rook = {Team.GREEN: './Images/green_rook_d.png',
                     Team.PURPLE: './Images/purple_rook_d.png'}

del_matrix_queen = {Team.BLUE: './Images/blue_queen.png',
                      Team.GREEN: './Images/green_queen.png',
                      Team.PURPLE: './Images/purple_queen.png',
                      Team.RED: './Images/red_queen.png',
                      Team.YELLOW: './Images/yellow_queen.png',
                      Team.ORANGE: './Images/orange_queen.png'
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
orange_pieces = []
red_pieces = []
yellow_pieces = []
blue_pieces = []
green_pieces = []
purple_pieces = []

#declare commanders here
orange_commander = Commander(orange_pieces, ob)
red_commander = King(red_pieces, rK)
yellow_commander = Commander(yellow_pieces, yb)
blue_commander = King(blue_pieces, bK)
green_commander = Commander(green_pieces, gb)
purple_commander = Commander(purple_pieces, pb)

player_commanders = [green_commander, blue_commander, purple_commander]
ai_commanders = [orange_commander, red_commander, yellow_commander]

# returns input if it is within the boundries on the board
def on_board(position: tuple[int, int]):
    x = position[0]
    y = position[1]
    """
    if -1 < position[0] < 8 and position[1] > -1 and position[-1] < 8:
        return True
    deployed_team
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

