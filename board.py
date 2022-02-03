import pygame

from common import *
from pieces import Piece, Team, Type


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
    board[0] = [Square(Piece(Team.RED, Type.ROOK, pygame.image.load('./images/red_rook.png'))),
                Square(Piece(Team.ORANGE, Type.KNIGHT, pygame.image.load('./images/orange_knight.png'))),
                Square(Piece(Team.ORANGE, Type.BISHOP, pygame.image.load('./images/orange_bishop.png'))),
                Square(Piece(Team.RED, Type.QUEEN, pygame.image.load('./images/red_queen.png'))),
                Square(Piece(Team.RED, Type.KING, pygame.image.load('./images/red_king.png'))),
                Square(Piece(Team.YELLOW, Type.BISHOP, pygame.image.load('./images/yellow_bishop.png'))),
                Square(Piece(Team.YELLOW, Type.KNIGHT, pygame.image.load('./images/yellow_knight.png'))),
                Square(Piece(Team.RED, Type.ROOK, pygame.image.load('./images/red_rook.png')))]

    board[7] = [Square(Piece(Team.BLUE, Type.ROOK, pygame.image.load('./images/blue_rook.png'))),
                Square(Piece(Team.GREEN, Type.KNIGHT, pygame.image.load('./images/green_knight.png'))),
                Square(Piece(Team.GREEN, Type.BISHOP, pygame.image.load('./images/green_bishop.png'))),
                Square(Piece(Team.BLUE, Type.QUEEN, pygame.image.load('./images/blue_queen.png'))),
                Square(Piece(Team.BLUE, Type.KING, pygame.image.load('./images/blue_king.png'))),
                Square(Piece(Team.PURPLE, Type.BISHOP, pygame.image.load('./images/purple_bishop.png'))),
                Square(Piece(Team.PURPLE, Type.KNIGHT, pygame.image.load('./images/purple_knight.png'))),
                Square(Piece(Team.BLUE, Type.ROOK, pygame.image.load('./images/blue_rook.png')))]

    for col in range(8):
        if col < 3:
            board[1][col] = Square(Piece(Team.ORANGE, Type.PAWN, pygame.image.load('./images/orange_pawn.png')))
            board[6][col] = Square(Piece(Team.GREEN, Type.PAWN, pygame.image.load('./images/green_pawn.png')))

        if 3 < col < 5:
            board[1][col] = Square(Piece(Team.RED, Type.PAWN, pygame.image.load('./images/red_pawn.png')))
            board[6][col] = Square(Piece(Team.BLUE, Type.PAWN, pygame.image.load('./images/blue_pawn.png')))
        else:
            board[1][col] = Square(Piece(Team.YELLOW, Type.PAWN, pygame.image.load('./images/yellow_pawn.png')))
            board[6][col] = Square(Piece(Team.PURPLE, Type.PAWN, pygame.image.load('./images/purple_pawn.png')))

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
            if board[row][col].color == BLUE:
                if (row + col) % 2 == 1:
                    board[row][col].color = GREY
                else:
                    board[row][col].color = WHITE
    print('removed highlights')
