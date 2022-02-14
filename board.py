import pygame

from common import *
from pieces import Piece, Team, Type, Value


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


def remove_highlights():
    for row in range(8):
        for col in range(8):
            #if (board[row][col].color == BLUE) or :
            if (row + col) % 2 == 1:
                board[row][col].color = GREY
            else:
                board[row][col].color = WHITE
    print('removed highlights')
