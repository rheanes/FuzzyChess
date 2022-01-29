import enum

from board import *

"""
    ATTENTION: Fix the piece moves to return all highlighted squares
"""

class Team(enum.Enum):
    YELLOW = 0
    RED = 1
    ORANGE = 2
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

#creates a chess piece class that shows:
#team, attackable, and color
class Piece:
  def __init__(self, team, type, image, color, attackable=False):
    self.team = team
    self.type = type
    self.attackable = attackable
    self.image = image
    self.color = color

"""
    Create instances of pieces.
    Only the original instances of pieces is required. 
    We will chaneg the colors of pieces upon delegation.
"""

#kings
#blue king
bk = Piece(Team.BLUE, Type.KING, './images/blue_king.png', 'b')
#red king
rk = Piece('r', Type.KING, './images/red_king.png', 'r')

#queens
#blue queen
bq = Piece('b', Type.QUEEN, './images/blue_queen.png', 'b')
#red queen
rq = Piece('r', Type.QUEEN, './images/red_queen.png', 'r')

#rooks
#blue team rooks
#blue rook
br = Piece('b', Type.ROOK, './images/blue_rook.png', 'b')
#red rook
rr = Piece('r', Type.ROOK, './images/red_rook.png', 'r')

#bishops
#blue team bishops
#green bishop
gb = Piece('b', Type.BISHOP, './images/green_bishop.png', 'b')
#purple bishop
pb = Piece('b', Type.BISHOP, './images/purple_bishop.png', 'p')
#red team bishops
#yellow bishop
yb = Piece('r', Type.BISHOP, './images/yellow_bishop.png', 'y')
#orange bishop
ob = Piece('r', Type.BISHOP, './images/orange_bishop.png', 'o')

#knights
#blue team knights
#green knight
gn = Piece('b', Type.KNIGHT, './images/green_knight.png', 'b')
#purple knight
pn = Piece('b', Type.KNIGHT, './images/purple_knight.png', 'p')
#red team knights
#yellow knight
yn = Piece('r', Type.KNIGHT, './images/yellow_knight.png', 'y')
#orange knight
on = Piece('r', Type.KNIGHT, './images/orange_knight.png', 'o')

#pawns
#blue team pawns
#blue pawn
bp = Piece('b', 'p', './images/blue_pawn.png', 'b')
#green pawn
gp = Piece('b', 'p', './images/green_pawn.png', 'g')
#purple pawn
pp = Piece('b', 'p', './images/purple_pawn.png', 'p')
#red team pawns
#red pawn
rp = Piece('r', 'p', './images/red_pawn.png', 'r')
#yellow pawn
yp = Piece('r', 'p', './images/yellow_pawn.png', 'y')
#orange pawn
op = Piece('r', 'p', './images/orange_pawn.png', 'o')

coordinates = []

# returns input if it is within the boundries on the board
def on_board(position):
    if position[0] > -1 and position[1] > -1 and position[0] < 8 and position[-1] < 8:
        return True

"""
    MOVES OF PIECES
"""

#check pawn moves seperatly from other pieces. If space free then x to move.
#otherwise, the piece in front of it is targetable.
def pawn_moves_one(piece): # team on the bottom
    """
    if coord[0] == 1:
        if board[coord[0] + 2][coord[1]] == '  ' and board[coord[0] + 1][coord[1]] == '  ':
            board[coord[0] + 2][coord[1]] = 'x '

    bottom3 = [[coord[0] + 1, coord[1] + i] for i in range(-1, 2)]

    for positions in bottom3:
        if on_board(positions):
            if bottom3.index(positions) % 2 == 0:
                try:
                    if board[positions[0]][positions[1]].team != 'b':
                        board[positions[0]][positions[1]].killable = True
                except:
                    pass
            else:
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
    """
    positions = []



def pawn_moves_two(index): # team on the top

    if index[0] == 6:
        if board[index[0] - 2][index[1]] == '  ' and board[index[0] - 1][index[1]] == '  ':
            board[index[0] - 2][index[1]] = 'x '
    top3 = [[index[0] - 1, index[1] + i] for i in range(-1, 2)]

    for positions in top3:
        if on_board(positions):
            if top3.index(positions) % 2 == 0:
                try:
                    if board[positions[0]][positions[1]].team != 'w':
                        board[positions[0]][positions[1]].killable = True
                except:
                    pass
            else:
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
    return board

#piece moves
## This just checks a 3x3 tile surrounding the king. Empty spots get an "x" and pieces of the opposite team become killable.
def king_moves(index):
    for y in range(3):
        for x in range(3):
            if on_board((index[0] - 1 + y, index[1] - 1 + x)):
                if board[index[0] - 1 + y][index[1] - 1 + x] == '  ':
                    board[index[0] - 1 + y][index[1] - 1 + x] = 'x '
                else:
                    if board[index[0] - 1 + y][index[1] - 1 + x].team != board[index[0]][index[1]].team:
                        board[index[0] - 1 + y][index[1] - 1 + x].killable = True
    return board


## This creates 4 lists for up, down, left and right and checks all those spaces for pieces of the opposite team. The list comprehension is pretty long so if you don't get it just msg me.
def rook_moves(index):
    cross = [[[index[0] + i, index[1]] for i in range(1, 8 - index[0])],
             [[index[0] - i, index[1]] for i in range(1, index[0] + 1)],
             [[index[0], index[1] + i] for i in range(1, 8 - index[1])],
             [[index[0], index[1] - i] for i in range(1, index[1] + 1)]]

    for direction in cross:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    if board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                    break
    return board


## Same as the rook but this time it creates 4 lists for the diagonal directions and so the list comprehension is a little bit trickier.
def bishop_moves(index):
    diagonals = [[[index[0] + i, index[1] + i] for i in range(1, 8)],
                 [[index[0] + i, index[1] - i] for i in range(1, 8)],
                 [[index[0] - i, index[1] + i] for i in range(1, 8)],
                 [[index[0] - i, index[1] - i] for i in range(1, 8)]]

    for direction in diagonals:
        for positions in direction:
            if on_board(positions):
                if board[positions[0]][positions[1]] == '  ':
                    board[positions[0]][positions[1]] = 'x '
                else:
                    if board[positions[0]][positions[1]].team != board[index[0]][index[1]].team:
                        board[positions[0]][positions[1]].killable = True
                    break
    return board


## applies the rook moves to the board then the bishop moves because a queen is basically a rook and bishop in the same position.
def queen_moves(index):
    board = rook_moves(index)
    board = bishop_moves(index)
    return board


## Checks a 5x5 board_state around the piece and uses pythagoras to see if if a move is valid. Valid moves will be a distance of sqrt(5) from centre
def knight_moves(index):
    for i in range(-2, 3):
        for j in range(-2, 3):
            if i ** 2 + j ** 2 == 5:
                if on_board((index[0] + i, index[1] + j)):
                    if board[index[0] + i][index[1] + j] == '  ':
                        board[index[0] + i][index[1] + j] = 'x '
                    else:
                        if board[index[0] + i][index[1] + j].team != board[index[0]][index[1]].team:
                            board[index[0] + i][index[1] + j].killable = True
    return board