import sys
import pygame

from GameFunctions import attack
from common import *
from board import *
from pieces import *
from guielements import *

DEFAULT_IMAGE_SIZE = (GAME_WIDTH / 8, GAME_WIDTH / 8)
SQUARE_WIDTH = SQUARE_HEIGHT = GAME_WIDTH / 8
clock = pygame.time.Clock()

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

delegation_mode = False

def turnChange():
    global turn
    if not turn:
        turn = True;
    else:
        turn = False

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

deligated_piece = None
deligated_commander = None
enemies = [Team.RED, Team.YELLOW, Team.ORANGE]
human_piece_deligated = False
action_count = 0
turn = True  # True maeans human move
delegation_mode = False
commander = Team.GREEN

def delegate(chosen_square):
    global deligated_piece
    global deligated_commander
    global action_count
    global human_piece_deligated
    global delegation_mode
    if (chosen_square.piece is not None) and (chosen_square.piece.team not in enemies):
        if (chosen_square.piece.type is not Type.KING) and (chosen_square.piece.type is not Type.BISHOP):
            deligated_piece = chosen_square.piece
            print('deligated piece selected')
            # deligation_count += 1
        elif (chosen_square.piece.type is Type.KING) or (chosen_square.piece.type is Type.BISHOP):
            deligated_commander = chosen_square.piece
            # deligation_count += 1
            print('deligated commander selected')
        if (deligated_piece is not None) and (deligated_commander is not None):
            blue_commander.delegate(deligated_piece, deligated_commander)
            human_piece_deligated = True
            action_count += 1
            delegation_mode = False
            reset_delieation()
            print('deligation completed')

def reset_delieation():
    global human_piece_deligated
    human_piece_deligated = False
    global deligated_piece
    deligated_piece = None
    global deligated_commander
    deligated_commander = None
    global action_count
    global delegation_mode

def display_turn_count():
    pass

# class for interactable elements that have text
class DelegateButton(Sprite):
    def __init__(self, pos, text, font_size, txt_col, bg_col, bg_hover, action=None):
        self.action = action
        self.selected = False
        self.remain_selected = False
        unselected_img = create_text_surface(text, font_size, txt_col, bg_col)
        highlighted_img = create_text_surface(text, font_size * 1.3, txt_col, bg_hover)

        self.images = [unselected_img, highlighted_img]
        self.rects = [unselected_img.get_rect(center=pos), highlighted_img.get_rect(center=pos)]

        super().__init__()

    @property
    def img(self):
        return self.images[1] if self.selected else self.images[0]

    @property
    def rect(self):
        return self.rects[1] if self.selected else self.rects[0]

    # selects different button images depending if the mouse is hovered over it
    def moused_over(self, mouse_pos, mouse_down):
        global delegation_mode
        if self.rect.collidepoint(mouse_pos):
            self.selected = True
            if mouse_down:
                self.remain_selected = True
                delegation_mode = True
                print('test')
                return self.action
        else:
            if delegation_mode:
                self.selected = True
            else:
                self.selected = False

    def draw(self, surface):
        surface.blit(self.img, self.rect)

def next_commander():
    pass

def reset_turn():
    global human_piece_deligated
    human_piece_deligated = False
    global action_count
    action_count = 0
    global turn
    turn = True

def message_box(text):
    print(text)

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
    Delegate_Button = DelegateButton(pos=(WIDTH-100, 450),
                                     font_size=25,
                                     txt_col=BLACK,
                                     bg_col=buttoncolor,
                                     text="Delegate",
                                     bg_hover=buttonhover,
                                     action=GameState.Play)
    #Recall_Button None
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
    buttons = [Home_Button, Delegate_Button, Resign_Button, End_Turn_Button, Rules_Button]

    current_square = None
    global action_count
    global turn
    delegated_pieces = []
    global delegation_mode
    global commander

    global FirstRun
    if FirstRun:
        create_board()
        FirstRun=False

    while True:
        mouse_down = False
        pygame.mouse.get_pressed()
        #print('Delegation: ', Delegate_Button.selected)
        #print('Delegation remain selected: ', Delegate_Button.remain_selected)
        #print('Delegation Mode: ', delegation_mode)
        print('action count', action_count)

        if turn:
            print('human turn')
            for event in pygame.event.get():
                if event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mouse_down = True

                    x,y = pygame.mouse.get_pos()
                    #if you dont click on the game board
                    if x >= GAME_WIDTH or y >= GAME_WIDTH:
                        if End_Turn_Button.selected:
                            turnChange()

                    #if you do click on the game board
                    else:
                        row, col = find_square_coordinates((x,y))
                        print('row ', row, ' col ', col)
                        chosen_square = board[row][col] # refers to the square clicked by the mouse
                        """ current causes issues
                        # prevents clicking on enemy pieces
                        if (chosen_square.piece.team in enemies) and chosen_square.piece:
                            pass
                        else:
                        """

                        if (Delegate_Button.selected or delegation_mode) and (commander == Type.KING):
                            #if (human_piece_deligated is not True):
                            #if not delegation_mode:
                            #    delegation_mode = True
                                #print('!!!!!!!!!!!!!!!!!!!check point!!!!!!!!!!!!!!!!!!!!!!!!')
                            #else:
                            delegate(chosen_square)
                        #elif Recall_Button.selected:
                        #    recall()
                        else:
                            # conditions for selected_square
                            if current_square is None:
                                if chosen_square.piece is None:
                                    pass
                                else:
                                    current_square = chosen_square
                                    potential_piece_moves(chosen_square)
                                    if current_square.piece == blue_commander.leader:
                                        blue_commander.see_pieces()
                            else:  # a piece is currently selected
                                if chosen_square.piece is not None: # clicking alternative piece on your side
                                    remove_highlights()
                                    current_square = chosen_square
                                    potential_piece_moves(chosen_square)
                                elif (chosen_square.color is WHITE) or (chosen_square.color is GREY):  # lets you unselect current piece
                                    remove_highlights()
                                    current_square = None
                                elif chosen_square.color is BLUE: # deals with movement
                                    if (chosen_square.piece is not None) and (): # there is a piece there
                                        current_square = None
                                        remove_highlights()
                                        move_piece(current_square, chosen_square)
                                        action_count += 1
                                    else:
                                        remove_highlights()
                                        move_piece(current_square, chosen_square)
                                        current_square = None
                                        action_count += 1
                                elif chosen_square.color is BLACK:
                                    if chosen_square.piece is not None:
                                        if attack(current_square.piece.type._value_, chosen_square.piece.type._value_) is True:
                                            chosen_square = None
                                            move_piece(current_square, chosen_square)
                                            current_square = None
                                            action_count += 1
                                        remove_highlights()
                                else:
                                    pass
                else:
                    pass
        else: # AI starts
            print('hello from computer')
            reset_turn()

        if action_count == 3:
            turnChange()

        update_display(screen)
        for b in buttons:
            ui_action = b.moused_over(pygame.mouse.get_pos(), mouse_down)
            if ui_action is not None:
                #if b == Deligate_Button:
                        
                return ui_action
            b.draw(screen)
        pygame.display.flip()
        clock.tick(15)
