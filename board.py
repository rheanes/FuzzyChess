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


# creates the board
def create_board():
    board[0] = [Square(Piece(Team.RED, Type.ROOK, pygame.image.load('./Images/red_rook.png'), Value.ROOK)),
                Square(Piece(Team.ORANGE, Type.KNIGHT, pygame.image.load('./Images/orange_knight.png'), Value.KNIGHT)),
                Square(Piece(Team.ORANGE, Type.BISHOP, pygame.image.load('./Images/orange_bishop.png'), Value.BISHOP)),
                Square(Piece(Team.RED, Type.QUEEN, pygame.image.load('./Images/red_queen.png'), Value.QUEEN)),
                Square(Piece(Team.RED, Type.KING, pygame.image.load('./Images/red_king.png'), Value.KING)),
                Square(Piece(Team.YELLOW, Type.BISHOP, pygame.image.load('./Images/yellow_bishop.png'), Value.BISHOP)),
                Square(Piece(Team.YELLOW, Type.KNIGHT, pygame.image.load('./Images/yellow_knight.png'), Value.KNIGHT)),
                Square(Piece(Team.RED, Type.ROOK, pygame.image.load('./Images/red_rook.png'), Value.ROOK))]

    board[7] = [Square(Piece(Team.BLUE, Type.ROOK, pygame.image.load('./Images/blue_rook.png'), Value.ROOK)),
                Square(Piece(Team.GREEN, Type.KNIGHT, pygame.image.load('./Images/green_knight.png'), Value.KNIGHT)),
                Square(Piece(Team.GREEN, Type.BISHOP, pygame.image.load('./Images/green_bishop.png'), Value.BISHOP)),
                Square(Piece(Team.BLUE, Type.QUEEN, pygame.image.load('./Images/blue_queen.png'), Value.QUEEN)),
                Square(Piece(Team.BLUE, Type.KING, pygame.image.load('./Images/blue_king.png'), Value.KING)),
                Square(Piece(Team.PURPLE, Type.BISHOP, pygame.image.load('./Images/purple_bishop.png'), Value.BISHOP)),
                Square(Piece(Team.PURPLE, Type.KNIGHT, pygame.image.load('./Images/purple_knight.png'), Value.KNIGHT)),
                Square(Piece(Team.BLUE, Type.ROOK, pygame.image.load('./Images/blue_rook.png'), Value.ROOK))]

    for col in range(8):
        if col <= 2:
            board[1][col] = Square(Piece(Team.ORANGE, Type.PAWN, pygame.image.load('./Images/orange_pawn.png'), Value.PAWN))
            board[6][col] = Square(Piece(Team.GREEN, Type.PAWN, pygame.image.load('./Images/green_pawn.png'), Value.PAWN))
        if col == 3 or col == 4:
            board[1][col] = Square(Piece(Team.RED, Type.PAWN, pygame.image.load('./Images/red_pawn.png'), Value.PAWN))
            board[6][col] = Square(Piece(Team.BLUE, Type.PAWN, pygame.image.load('./Images/blue_pawn.png'), Value.PAWN))
        if col >= 5:
            board[1][col] = Square(Piece(Team.YELLOW, Type.PAWN, pygame.image.load('./Images/yellow_pawn.png'), Value.PAWN))
            board[6][col] = Square(Piece(Team.PURPLE, Type.PAWN, pygame.image.load('./Images/purple_pawn.png'), Value.PAWN))
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
def maxMovement(maxSpeed: int, iterations: int, position: tuple[int, int], startPos: tuple[int, int], positions=None):

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

    if (board[currRow][currCol].piece is not None) and position != startPos:
        positions.append(position)
        return

    maxMovement(maxSpeed, iterations + 1, (currRow, currCol + 1), startPos, positions)
    maxMovement(maxSpeed, iterations + 1, (currRow + 1, currCol + 1), startPos, positions)
    maxMovement(maxSpeed, iterations + 1, (currRow + 1, currCol), startPos, positions)
    maxMovement(maxSpeed, iterations + 1, (currRow - 1, currCol + 1), startPos, positions)
    maxMovement(maxSpeed, iterations + 1, (currRow + 1, currCol - 1), startPos, positions)
    maxMovement(maxSpeed, iterations + 1, (currRow - 1, currCol), startPos, positions)
    maxMovement(maxSpeed, iterations + 1, (currRow - 1, currCol - 1), startPos, positions)
    maxMovement(maxSpeed, iterations + 1, (currRow + 1, currCol), startPos, positions)

    if position in positions:
        return positions
    else:
        positions.append(position)

    return positions
