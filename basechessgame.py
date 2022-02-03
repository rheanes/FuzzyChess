# -*- coding: utf-8 -*-


# make sure pygame is downloaded

import pygame
import sys

from pieces import *
from board import *

# CREATE A 800 by 800 Pixel windowdow to play the game on.
# os.environ["SDL_VIDEODRIVER"] = "dummy"
WIDTH = 800  # screen width

# creates 800 by 800 Pixel window to play the game on
window = pygame.display.set_mode((WIDTH, WIDTH))
# Set caption for Window
pygame.display.set_caption("Chess")

WHITE = (255, 255, 255)
GREY = (128, 128, 128)
YELLOW = (204, 204, 0)
BLUE = (50, 255, 255)
BLACK = (0, 0, 0)

starting_order = {(0, 0): pygame.image.load(rr.image),
                  (1, 0): pygame.image.load(on.image),
                  (2, 0): pygame.image.load(ob.image),
                  (3, 0): pygame.image.load(rq.image),
                  (4, 0): pygame.image.load(rk.image),
                  (5, 0): pygame.image.load(yb.image),
                  (6, 0): pygame.image.load(yn.image),
                  (7, 0): pygame.image.load(rr.image),
                  (0, 1): pygame.image.load(op.image),
                  (1, 1): pygame.image.load(op.image),
                  (2, 1): pygame.image.load(op.image),
                  (3, 1): pygame.image.load(rp.image),
                  (4, 1): pygame.image.load(rp.image),
                  (5, 1): pygame.image.load(yp.image),
                  (6, 1): pygame.image.load(yp.image),
                  (7, 1): pygame.image.load(yp.image),

                  (0, 2): None, (1, 2): None, (2, 2): None, (3, 2): None,
                  (4, 2): None, (5, 2): None, (6, 2): None, (7, 2): None,
                  (0, 3): None, (1, 3): None, (2, 3): None, (3, 3): None,
                  (4, 3): None, (5, 3): None, (6, 3): None, (7, 3): None,
                  (0, 4): None, (1, 4): None, (2, 4): None, (3, 4): None,
                  (4, 4): None, (5, 4): None, (6, 4): None, (7, 4): None,
                  (0, 5): None, (1, 5): None, (2, 5): None, (3, 5): None,
                  (4, 5): None, (5, 5): None, (6, 5): None, (7, 5): None,

                  (0, 6): pygame.image.load(gp.image),
                  (1, 6): pygame.image.load(gp.image),
                  (2, 6): pygame.image.load(gp.image),
                  (3, 6): pygame.image.load(bp.image),
                  (4, 6): pygame.image.load(bp.image),
                  (5, 6): pygame.image.load(pp.image),
                  (6, 6): pygame.image.load(pp.image),
                  (7, 6): pygame.image.load(pp.image),
                  (0, 7): pygame.image.load(br.image),
                  (1, 7): pygame.image.load(gn.image),
                  (2, 7): pygame.image.load(gb.image),
                  (3, 7): pygame.image.load(bq.image),
                  (4, 7): pygame.image.load(bk.image),
                  (5, 7): pygame.image.load(pb.image),
                  (6, 7): pygame.image.load(pn.image),
                  (7, 7): pygame.image.load(br.image)}

DEFAULT_IMAGE_SIZE = (WIDTH / 8, WIDTH / 8)


class Square:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.color = WHITE
        self.piece = None


# creates the board
def create_board():
    board[0] = [Piece('r', 'r', './images/red_rook.png', 'r'), Piece('r', 'n', './images/orange_knight.png', 'o'),
                Piece('r', 'b', './images/orange_bishop.png', 'o'),
                Piece('r', 'q', './images/red_queen.png', 'r'), Piece('r', 'k', './images/red_king.png', 'r'),
                Piece('r', 'b', './images/yellow_bishop.png', 'y'),
                Piece('r', 'n', './images/yellow_knight.png', 'y'), Piece('r', 'r', './images/red_rook.png', 'r')]

    board[7] = [Piece('b', 'r', './images/blue_rook.png', 'b'), Piece('b', 'n', './images/green_knight.png', 'g'),
                Piece('b', 'b', './images/green_bishop.png', 'g'),
                Piece('b', 'q', './images/blue_queen.png', 'b'), Piece('b', 'k', './images/blue_king.png', 'b'),
                Piece('b', 'b', './images/purple_bishop.png', 'p'),
                Piece('b', 'n', './images/purple_knight.png', 'p'), Piece('b', 'r', './images/blue_rook.png', 'b')]

    for i in range(8):
        if i < 3:
            board[1][i] = Piece('r', 'p', 'orange_pawn.png', 'o')
            board[6][i] = Piece('b', 'p', 'green_pawn.png', 'g')
        if 3 < i < 5:
            board[1][i] = Piece('r', 'p', 'red_pawn.png', 'r')
            board[6][i] = Piece('b', 'p', 'blue_pawn.png', 'b')
        else:
            board[1][i] = Piece('r', 'p', 'yellow_pawn.png', 'y')
            board[6][i] = Piece('b', 'p', 'purple_pawn.png', 'p')


def readable_cords():
    output = ''
    for row in board:
        for col in row:
            try:
                output += col.team + col.type + ', '
            except:
                output += col + ', '
            output += '\n'
        return output


# reset captures and killable pieces
def deselect():
    for row in range(len(board)):
        for column in range(len(board[0])):
            if board[row][column] == 'x ':
                board[row][column] = ' '
            else:
                try:
                    board[row][column].killable = False
                except:
                    pass
        return readable_cords()


"""
    This will set the color of 
"""
def highlight_possible_moves(coordinates):
    moves = []
    for i in range(len(temp_board)):
        for j in range(len(temp_board[0])):
            if temp_board[i][j] == 'x':
                moves.append((i, j))
            else:
                try:
                    if temp_board[i][j].killable:
                        moves.append((i, j))
                except:
                    pass
    return moves


# take a piece and it's index to determine where the piece can move using functions that are defined for each piece.
def select_moves(piece, coordinate):
    if piece.type is Type.PAWN:
        if piece.team == 'r':
            highlight_possible_moves(pawn_moves_one(coordinate))
        else:
            highlight_possible_moves(pawn_moves_two(coordinate))
    elif piece.type == Type.KING:
        highlight_possible_moves(king_moves(coordinate))
    elif piece.type == Type.ROOK:
        highlight_possible_moves(rook_moves(coordinate))
    elif piece.type == Type.BISHOP:
        highlight_possible_moves(bishop_moves(coordinate))
    elif piece.type == Type.QUEEN:
        highlight_possible_moves(queen_moves(coordinate))
    else:
        highlight_possible_moves(knight_moves(coordinate))


"""
    For now it is drawing a rectangle but eventually we are going to need it
    to use blit to draw the chess pieces instead
"""


def create_board_state():
    board_state = []
    for i in range(8):
        board_state.append([])
        for j in range(8):
            square = Square(i, j, WIDTH // 8)
            board_state[i].append(square)
            if (i + j) % 2 == 1:
                board_state[i][j].color = GREY
    return board_state


"""
This is creating the Squares thats are on the board(so the chess tiles)
I've put them into a 2d array which is identical to the dimesions of the chessboard
"""


def draw_board_lines():
    gap = int(WIDTH // 8)
    for i in range(8):
        pygame.draw.line(window, BLACK, (0, i * gap), (WIDTH, i * gap))
        for j in range(8):
            pygame.draw.line(window, BLACK, (j * gap, 0), (j * gap, WIDTH))


"""
    The Squares are all white so this we need to draw the grey lines that separate all the chess tiles
    from each other and that is what this function does
"""


def update_display(board_state):
    for row in board_state:
        for square in row:
            # will draw squares with no piece
            pygame.draw.rect(window, square.color, (square.x, square.y, WIDTH / 8, WIDTH / 8))

            # will draw squares with pieces
            # if starting_order[(square.row, square.col)]:
            # if :
            #    pass
            if starting_order[(square.row, square.col)] is not None:
                window.blit(pygame.transform.scale(starting_order[(square.row, square.col)], DEFAULT_IMAGE_SIZE),
                            (square.x, square.y))
    draw_board_lines()
    pygame.display.update()


def find_square_coordinates(pos):
    interval = WIDTH / 8
    x, y = pos
    rows = x // interval
    columns = y // interval
    return int(rows), int(columns)


def display_potential_moves(positions, board_state):
    for i in positions:
        x, y = i
        board_state[x][y].color = BLUE
        """
        Displays all the potential moves
        """


def Do_Move(OriginalPos, FinalPosition):
    starting_order[FinalPosition] = starting_order[OriginalPos]
    starting_order[OriginalPos] = None


def remove_possible_moves(board_state):
    for i in range(len(board_state)):
        for j in range(len(board_state[0])):
            if (i + j) % 2 == 0:
                board_state[i][j].color = WHITE
            else:
                board_state[i][j].color = GREY
    return board_state


"""
    this takes in 2 co-ordinate parameters which you can get as the position of the piece and then the position of the Square it is moving to
    you can get those co-ordinates using my old function for swap
"""

if __name__ == '__main__':
    create_board()
    setup_pieces()
    piece_selected = False
    piece_to_move = []
    board_state = create_board_state()

    while True:
        pygame.time.delay(50)  # stops cpu dying
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:  # quits the program if the player closes the windowdow
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                x, y = find_square_coordinates(pos)
                print(x, ' ', y)
                if not piece_selected:
                    # try:
                    select_moves(board[x][y], (x, y))
                    """
                    for position in positions:
                        row, col = position
                        board_state[row][col].color = BLUE
                    """
                    # piece_to_move = x, y
                    piece_selected = True

                    """
                    except:
                        piece_to_move = []
                        print('Can\'t select')
                    """
                    # print(piece_to_move)
                else:
                    try:
                        if board[x][y].attackable:
                            row, col = piece_to_move  # coords of original piece
                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            deselect()
                            remove_possible_moves(board_state)
                            Do_Move((col, row), (y, x))
                            print(readable_cords())
                        else:
                            deselect()
                            remove_possible_moves(board_state)
                            piece_selected = False
                            print("Deselected")
                    except:
                        if board[x][y] == 'x ':
                            row, col = piece_to_move
                            board[x][y] = board[row][col]
                            board[row][col] = '  '
                            deselect()
                            remove_possible_moves(board_state)
                            Do_Move((col, row), (y, x))
                            print(readable_cords())
                        else:
                            deselect()
                            remove_possible_moves(board_state)
                            piece_selected = False
                            print("Invalid move")
                    piece_selected = False
            else:
                pass

        update_display(board_state)
