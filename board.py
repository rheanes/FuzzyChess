from common import *

class Square:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.x_pos = self.row * (WIDTH // 8)
        self.y_pos = self.col * (WIDTH // 8)
        self.color = WHITE
        self.piece = None


board = [[ Square(None) for _ in range(8)] for _ in range(8)]

# creates the board
def create_board():
    board[0] = [Square(Piece('r', 'r', './images/red_rook.png', 'r')), Square(Piece('r', 'n', './images/orange_knight.png', 'o')),
                Square(Piece('r', 'b', './images/orange_bishop.png', 'o')), Square(Piece('r', 'q', './images/red_queen.png', 'r')),
                Square(Piece('r', 'k', './images/red_king.png', 'r')), Square(Piece('r', 'b', './images/yellow_bishop.png', 'y')),
                Square(Piece('r', 'n', './images/yellow_knight.png', 'y')), Square(Piece('r', 'r', './images/red_rook.png', 'r'))]

    board[7] = [Square(Piece('b', 'r', './images/blue_rook.png', 'b')), Square(Piece('b', 'n', './images/green_knight.png', 'g')),
                Square(Piece('b', 'b', './images/green_bishop.png', 'g')), Square(Piece('b', 'q', './images/blue_queen.png', 'b')),
                Square(Piece('b', 'k', './images/blue_king.png', 'b')), Square(Piece('b', 'b', './images/purple_bishop.png', 'p')),
                Square(Piece('b', 'n', './images/purple_knight.png', 'p')), Square(Piece('b', 'r', './images/blue_rook.png', 'b'))]

    for i in range(8):
        if i < 3:
            board[1][i] = Square(Piece('r', 'p', 'orange_pawn.png', 'o'))
            board[6][i] = Square(Piece('b', 'p', 'green_pawn.png', 'g'))
        if 3 < i < 5:
            board[1][i] = Square(Piece('r', 'p', 'red_pawn.png', 'r'))
            board[6][i] = Square(Piece('b', 'p', 'blue_pawn.png', 'b'))
        else:
            board[1][i] = Square(Piece('r', 'p', 'yellow_pawn.png', 'y'))
            board[6][i] = Square(Piece('b', 'p', 'purple_pawn.png', 'p'))

    i, j = 0, 0
    for b_row in board:
        for square in b_row:
            # board_state[i].append(square)
            if (i + j) % 2 == 1:
                square.color = GREY
            j += 1
        i += 1

def setup_display():
    pass
