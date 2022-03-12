import pygame

from common import *
from pieces import Piece, Team, Type, Value, enemies, pawn_moves_top, pawn_moves_bottom

#----------------BOARD CREATING AND SQUATE CLASS ------------
class Square:
    def __init__(self, piece):
        super().__init__()
        self.row = 0
        self.col = 0
        # self.x_pos = self.row * (WIDTH // 8)
        # self.y_pos = self.col * (WIDTH // 8)
        self.color = (255, 255, 255)
        self.piece = piece


board = [[Square(None) for _ in range(8)] for _ in range(8)]

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

# creates the board
def create_board():
    board[0] = [Square(rr1),
                Square(ok),
                Square(ob),
                Square(rq),
                Square(rK),
                Square(yb),
                Square(yk),
                Square(rr2)]

    board[7] = [Square(br1),
                Square(gk),
                Square(gb),
                Square(bq),
                Square(bK),
                Square(pb),
                Square(pk),
                Square(br2)]

    
    board[1][0] = Square(op1)
    board[1][1] = Square(op2)
    board[1][2] = Square(op3)
    board[6][0] = Square(gp1)
    board[6][1] = Square(gp2)
    board[6][2] = Square(gp3)
        
    board[1][3] = Square(rp1)
    board[1][4] = Square(rp2)
    board[6][3] = Square(bp1)
    board[6][4] = Square(bp2)

    board[1][5] = Square(yp1)
    board[1][6] = Square(yp2)
    board[1][7] = Square(yp3)
    board[6][5] = Square(pp1)
    board[6][6] = Square(pp2)
    board[6][7] = Square(pp3)
#adding colors to squares
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col].color = GREY

            board[row][col].row = row
            board[row][col].col = col
            """
            board[row][col].x_pos = col * (WIDTH // 8)
            board[row][col].y_pos = row * (WIDTH // 8)
            """

def clear_board():
    for row in range(8):
        for col in range(8):
            board[row][col] = Square(None)
    # adding colors to squares
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col].color = GREY

            board[row][col].row = row
            board[row][col].col = col
            """
            board[row][col].x_pos = col * (WIDTH // 8)
            board[row][col].y_pos = row * (WIDTH // 8)
            """


    #_----------_SQUARE UTILITY-------------

def find_square_coordinates(position: tuple[int, int]):
    interval = GAME_WIDTH / 8
    x, y = position
    row = y // interval
    col = x // interval
    return int(row), int(col)

def move_piece(curr_pos: Square, new_pos: Square):
    board[new_pos.row][new_pos.col].piece = board[curr_pos.row][curr_pos.col].piece
    board[curr_pos.row][curr_pos.col].piece = None
    print('pieced moved')

#--------------__SQUARE HIGHLIGHTING AND UNHIGHLIGHTING------------------

# highlight possible moves
# add 'type: Action' for type of action
def highlight_moves(positions: tuple[int, int], team: Team):
    for row, col in positions:
        if board[row][col].color == BLUE:
            pass
        else:
            if board[row][col].piece is None:
                board[row][col].color = BLUE
            elif board[row][col].piece is not None:
                if board[row][col].piece.team in enemies[team]:
                    board[row][col].color = BLACK
                else:
                    pass
            else:
                pass

            """
            if type is Action.MOVE:
                board[row][col].color = BLUE
            elif type is Action.ATTACK:
                board[row][col].color = RED
            """
    print('finished highlighting')



def remove_highlights():
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col].color = GREY
            else:
                board[row][col].color = WHITE
    print('removed highlights')


#------------------_PATHFINDING STUFF-------------

# Takes an input piece, and determines the maximum movement it can make. This is done through a recursive BFS
# that goes as far as the piece has movement.
# Implement a BFS algorithm to check spots around the square, and the spots around the
# accompanying squares up to the length of which the Rook can move.
# Essentially, from your position, check the coords (x,y), and then their potential partners
# up to the maximum movement. If any of the spaces found within the BFS are unoccupied, then
# we will add it to the list we are making. Afterwards, we append the list to the positions
#############################################################################################
#                                  POSITIONS TO CHECK PER SPACE                             #
#############################################################################################
#                         (pos - 1, pos + 1) | (pos, pos + 1) | (pos + 1, pos + 1)          #
#                         (pos - 1, pos)     |  CURR_POS      | (pos + 1, pos)              #
#                         (pos - 1, pos - 1) | (pos, pos - 1) | (pos + 1, pos - 1)          #
#############################################################################################
def maxMovement(maxSpeed: int, iterations: int, position: tuple[int, int], startPos: tuple[int, int], piece: int, positions=None):

    if positions is None:
        positions = []

    currRow = position[0]
    currCol = position[1]

    if (currRow < 0) or (currCol < 0):
        return

    if (currRow > 7) or (currCol > 7):
        return

    if iterations > maxSpeed:
        return

    #Checks to the Right square
    maxMovement(maxSpeed, iterations + 1, (currRow, currCol + 1), startPos, piece, positions)

    #Checks to the Down-Right square
    maxMovement(maxSpeed, iterations + 1, (currRow + 1, currCol + 1), startPos, piece, positions)

    #Checks to the Down square
    maxMovement(maxSpeed, iterations + 1, (currRow + 1, currCol), startPos, piece, positions)

    #Checks to the Down-Left square
    maxMovement(maxSpeed, iterations + 1, (currRow + 1, currCol - 1), startPos, piece, positions)

    #Checks to the Left square
    maxMovement(maxSpeed, iterations + 1, (currRow, currCol - 1), startPos, piece, positions)

    #Checks to the Up-Left square
    maxMovement(maxSpeed, iterations + 1, (currRow - 1, currCol - 1), startPos, piece, positions)

    #Checks to the Up Square
    maxMovement(maxSpeed, iterations + 1, (currRow - 1, currCol), startPos, piece, positions)

    #Checks to the Up-Right square
    maxMovement(maxSpeed, iterations + 1, (currRow - 1, currCol + 1), startPos, piece, positions)

    if position in positions:
        return positions
    else:
        if board[currRow][currCol].piece is None:
            positions.append(position)
        elif piece == 4 and (position != startPos):
            if iterations < 3:
                positions.append(position)
        elif iterations < 2 and (position != startPos):
            positions.append(position)

    return positions
