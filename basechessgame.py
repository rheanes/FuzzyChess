import sys
import pygame

from common import *
from board import *
from pieces import *
from guielements import *

DEFAULT_IMAGE_SIZE = (GAME_WIDTH / 8, GAME_WIDTH / 8)
SQUARE_WIDTH = SQUARE_HEIGHT = GAME_WIDTH / 8
clock = pygame.time.Clock()

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


def find_square_coordinates(position: tuple[int, int]):
    interval = GAME_WIDTH / 8
    x, y = position
    row = y // interval
    col = x // interval
    return int(row), int(col)


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
                    board[row][col].color = RED
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


def potential_piece_moves(square: Square):
    piece = square.piece
    if piece.type == Type.PAWN:
        if piece.team == Team.YELLOW or (piece.team == Team.RED) or piece.team == Team.ORANGE:
            highlight_moves(pawn_moves_top((square.row, square.col)), square.piece.team)
        else:
            highlight_moves(pawn_moves_bottom((square.row, square.col)), square.piece.team)
    if (piece.type == Type.KING) or (piece.type == Type.QUEEN):
        #Old call first
        #highlight_moves(king_queen_moves((square.row, square.col)), square.piece.team)
        highlight_moves(maxMovement(4, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)

    elif piece.type == Type.ROOK:
        highlight_moves(maxMovement(3, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)

    elif piece.type == Type.BISHOP:
        highlight_moves(maxMovement(3, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)

    elif piece.type == Type.KNIGHT:
        highlight_moves(maxMovement(5, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)


def move_piece(curr_pos: Square, new_pos: Square):
    board[new_pos.row][new_pos.col].piece = board[curr_pos.row][curr_pos.col].piece
    board[curr_pos.row][curr_pos.col].piece = None
    print('pieced moved')


#Comment out def playgame(): and uncomment if __name__ = '__main__' if you want to run
#basechessgame.py without ScreenGUI.py
#if __name__ == '__main__':
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
                           action=GameState.Resign)
    buttons = [Home_Button, Deligate_Button, Resign_Button, End_Turn_Button, Rules_Button]
    create_board()
    square_group = []
    current_square = None
    bottom_player_turn = True
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
                            else:
                                remove_highlights()
                                move_piece(current_square, chosen_square)
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
