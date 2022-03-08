import sys
import pygame

import GameFunctions
from common import *
from board import *
from pieces import *
from guielements import *

DEFAULT_IMAGE_SIZE = (GAME_WIDTH / 8, GAME_WIDTH / 8)
SQUARE_WIDTH = SQUARE_HEIGHT = GAME_WIDTH / 8
clock = pygame.time.Clock()
turn = True # True maeans human move

orange_pieces = [op1, op2, op3, ok, ob]
orange_commander = Commander(orange_pieces, ob)
red_pieces = [rr1, rr2, rp1, rp2, rq, rK]
red_commander = King(red_pieces, rK)
yellow_pieces = [yp1, yp2, yp3, yk, yb]
yellow_commander = Commander(yellow_pieces, yb)
blue_pieces = [br1, br2, bp1, bp2, bq, bK]
blue_commander = King(blue_pieces, bK)
green_pieces = [gp1, gp2, gp3, gk, gb]
green_commander = Commander(green_pieces, gb)
purple_pieces = [pp1, pp2, pp3, pk, pb]
purple_commander = Commander(purple_pieces, pb)

player_commanders = [green_commander, blue_commander, purple_commander]
ai_commanders = [orange_commander, red_commander, yellow_commander]

#deligated

def turnChange():
    global turn
    turn = not turn

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
    if (piece.team == Team.YELLOW or (piece.team == Team.RED) or piece.team == Team.ORANGE):
        if piece.type == Type.PAWN:
            highlight_moves(pawn_moves_top((square.row, square.col)), square.piece.team)
        elif (piece.type == Type.KING) or (piece.type == Type.QUEEN):
            highlight_moves(maxMovement(3, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)
        elif piece.type == Type.ROOK:
            highlight_moves(maxMovement(2, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)
        elif piece.type == Type.BISHOP:
            highlight_moves(maxMovement(2, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)
        elif piece.type == Type.KNIGHT:
            highlight_moves(maxMovement(4, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)
    elif (piece.team == Team.GREEN or piece.team == Team.BLUE or piece.team == Team.PURPLE):
        if piece.type == Type.PAWN:
            highlight_moves(pawn_moves_bottom((square.row, square.col)), square.piece.team)
        if (piece.type == Type.KING) or (piece.type == Type.QUEEN):
            highlight_moves(maxMovement(3, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)
        elif piece.type == Type.ROOK:
            highlight_moves(maxMovement(2, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)
        elif piece.type == Type.BISHOP:
            highlight_moves(maxMovement(2, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)
        elif piece.type == Type.KNIGHT:
            highlight_moves(maxMovement(4, 0, (square.row, square.col), (square.row, square.col)), square.piece.team)

def start_deligation(p, c, k):
    team_king = k
    selected_piece = p
    selected_commander = c
    team_king.delegate(selected_piece, selected_commander)
def display_turn_count():
    pass


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
    enemies = [Team.RED, Team.YELLOW, Team.ORANGE]
    current_square = None

    global FirstRun
    if FirstRun:
        create_board()
        FirstRun=False

    while True:
        mouse_down = False

        global turn
        if turn:
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mouse_down = True

                    x,y = pygame.mouse.get_pos()
                    #if you dont click on the game board
                    if x >= GAME_WIDTH or y >= GAME_WIDTH:
                        if End_Turn_Button.selected:
                            turn = False
                    #if you do click on the game board
                    else:
                        row, col = find_square_coordinates((x,y))
                        print('row ', row, ' col ', col)
                        chosen_square = board[row][col]
                        """ current causes issues
                        # prevents clicking on enemy pieces
                        if (chosen_square.piece.team in enemies) and chosen_square.piece:
                            pass
                        else:
                        """
                        # conditions for selected_square
                        if current_square is None:
                            if chosen_square.piece is None:
                                pass
                            else:
                                current_square = chosen_square
                                potential_piece_moves(chosen_square)
                                if current_square.piece == blue_commander.leader:
                                    blue_commander.see_pieces()
                        else:  # a piece is already selected
                            if chosen_square.piece is not None and chosen_square.piece.team == current_square.piece.team:
                                remove_highlights()
                                current_square = chosen_square
                                potential_piece_moves(chosen_square)
                            if (chosen_square.color is WHITE) or (chosen_square.color is GREY):
                                remove_highlights()
                                current_square = None
                            elif chosen_square.color is BLUE:
                                if chosen_square.piece is not None:
                                    current_square = None
                                    remove_highlights()
                                    move_piece(current_square, chosen_square)
                                else:
                                    remove_highlights()
                                    move_piece(current_square, chosen_square)
                                    current_square = None
                            elif chosen_square.color is BLACK:
                                if chosen_square.piece is not None:
                                    if GameFunctions.attack(current_square.piece.type._value_, chosen_square.piece.type._value_) is True:
                                        remove_highlights()
                                        chosen_square.piece = None
                                        move_piece(current_square, chosen_square)
                                        current_square = None
                                    else:
                                        remove_highlights()


                            else:
                                pass
                else:
                    pass
        else:
            pass

        update_display(screen)
        for b in buttons:
            ui_action = b.moused_over(pygame.mouse.get_pos(), mouse_down)
            if ui_action is not None:
                #if b == Deligate_Button:
                        
                return ui_action
            b.draw(screen)
        pygame.display.flip()
        clock.tick(15)
