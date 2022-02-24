import sys
import pygame

from common import *
from board import *
from pieces import *
from guielements import *

DEFAULT_IMAGE_SIZE = (GAME_WIDTH / 8, GAME_WIDTH / 8)
SQUARE_WIDTH = SQUARE_HEIGHT = GAME_WIDTH / 8
clock = pygame.time.Clock()
turn = 0

def turnChange():
    global turn
    if turn == 0:
        turn += 1
    else:
        turn -= 1

def update_display(screen):
    """ Draw board squares """
    for row in board:
        for square in row:
            x_pos = square.col * (GAME_WIDTH // 8)
            y_pos = square.row * (GAME_WIDTH // 8)
            # will draw squares with no piece
            pygame.draw.rect(screen, square.color, (x_pos, y_pos, GAME_WIDTH, HEIGHT))
            # if square.color == BLUE:
            # print('square color:', square.color)
            # print('finished drawing highlighted rectangles')
            # will draw squares with pieces
            # if starting_order[(square.row, square.col)]:
            # if :
            #    pass
            # if starting_order[(square.row, square.col)] is not None:
            if square.piece is not None:
                screen.blit(pygame.transform.scale(square.piece.image, DEFAULT_IMAGE_SIZE), (x_pos, y_pos))
                # screen.blit(pygame.transform.scale(starting_order[(square.row, square.col)], DEFAULT_IMAGE_SIZE), (square.x_pos, square.y_pos))
    """ Draw board lines """
    gap = GAME_WIDTH // 8
    for i in range(9):
        pygame.draw.line(screen, BLACK, (0, i * gap), (GAME_WIDTH, i * gap))
        for j in range(9):
            pygame.draw.line(screen, BLACK, (j * gap, 0), (j * gap, GAME_WIDTH))

    pygame.draw.rect(screen, BACKGROUND, (GAME_WIDTH + 1, 0, WIDTH, HEIGHT))
    pygame.draw.rect(screen, BACKGROUND, (0, GAME_WIDTH+1, WIDTH, HEIGHT))
    #print('testing')

def potential_piece_moves(square: Square):
    piece = square.piece
    if (piece.team == Team.YELLOW or (piece.team == Team.RED) or piece.team == Team.ORANGE) and turn == 1:
        if piece.type == Type.PAWN:
            highlight_moves(pawn_moves_top((square.row, square.col)), square.piece.team)
        elif (piece.type == Type.KING) or (piece.type == Type.QUEEN):
            highlight_moves(maxMovement(4, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)
        elif piece.type == Type.ROOK:
            highlight_moves(maxMovement(3, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)
        elif piece.type == Type.BISHOP:
            highlight_moves(maxMovement(3, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)
        elif piece.type == Type.KNIGHT:
            highlight_moves(maxMovement(5, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)
    elif (piece.team == Team.GREEN or piece.team == Team.BLUE or piece.team == Team.PURPLE) and turn == 0:
        if piece.type == Type.PAWN:
            highlight_moves(pawn_moves_bottom((square.row, square.col)), square.piece.team)
        if (piece.type == Type.KING) or (piece.type == Type.QUEEN):
            highlight_moves(maxMovement(4, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)
        elif piece.type == Type.ROOK:
            highlight_moves(maxMovement(3, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)
        elif piece.type == Type.BISHOP:
            highlight_moves(maxMovement(3, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)
        elif piece.type == Type.KNIGHT:
            highlight_moves(maxMovement(5, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)


FirstRun=True
def playgame(screen):
    Home_Button = button(pos=(WIDTH-100, 100),
                             font_size=25,
                             txt_col=BLACK,
                             bg_col=buttoncolor,
                             text="Home",
                             bg_hover=buttonhover,
                             action=GameState.Home)

    Rules_Button = button(pos=(WIDTH-100, 200),
                              font_size=25,
                              txt_col=BLACK,
                              bg_col=buttoncolor,
                              text="Rules",
                              bg_hover=buttonhover,
                              action=GameState.Rules)
    Deligate_Button = button(pos=(WIDTH-100, 450),
                             font_size=25, txt_col=BLACK,
                             bg_col=buttoncolor,
                             text="Deligate",
                             bg_hover=buttonhover,
                             action=GameState.Delegate)
    End_Turn_Button = button(pos=(WIDTH-100, 550),
                             font_size=25,
                             txt_col=BLACK,
                             bg_col=buttoncolor,
                             text="End Turn",
                             bg_hover=buttonhover,
                             action=GameState.EndTurn)
    Resign_Button = button(pos=(WIDTH-100, 650),
                           font_size=25,
                           txt_col=BLACK,
                           bg_col=buttoncolor,
                           text="Resign",
                           bg_hover=buttonhover,
                           action=GameState.Loss)
    buttons = [Home_Button, Deligate_Button, Resign_Button, End_Turn_Button, Rules_Button]
    square_group = []
    current_square = None
    bottom_player_turn = True
    global FirstRun
    if FirstRun:
        create_board()
        FirstRun=False
    while True:
        mouse_down = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True

                pos = pygame.mouse.get_pos()
                #if you dont click on the game board
                if pos[0] >= GAME_WIDTH:
                    chosen_square = None

                elif pos[1] >= GAME_WIDTH:
                    chosen_square = None

                #if you do click on the game board
                else:
                    row, col = find_square_coordinates(pos)
                    print('row ', row, ' col ', col)
                    chosen_square = board[row][col]

                # conditions for selected_square
                    if current_square is None:  # have piece selected
                        # positions = potential_piece_moves(board[row][col], (row, col))
                        if chosen_square.piece is None:
                            pass
                        else:
                            current_square = chosen_square
                            potential_piece_moves(board[row][col])
                        """
                        for position in positions:
                            row, col = position
                            board[row][col].color = BLUE
                        """
                    else:  # a piece is already selected
                        if chosen_square.piece is not None:
                            remove_highlights()
                            current_square = chosen_square
                            potential_piece_moves(board[row][col])
                        elif (board[row][col].color is WHITE) or (board[row][col].color is GREY):
                            remove_highlights()
                            current_square = None
                        elif board[row][col].color is BLUE:
                            if board[row][col].piece is not None:
                                remove_highlights()
                                move_piece(current_square, chosen_square)
                                turnChange()
                            else:
                                remove_highlights()
                                move_piece(current_square, chosen_square)
                                turnChange()
                        else:
                            pass
            else:
                pass

        update_display(screen)
        for b in buttons:
            ui_action = b.moused_over(pygame.mouse.get_pos(), mouse_down)
            if ui_action is not None:
                return ui_action
            b.draw(screen)
        pygame.display.flip()
        clock.tick(15)
