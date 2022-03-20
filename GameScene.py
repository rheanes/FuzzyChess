import sys
import pygame
import pygame.event

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

color_matrix_pawn = {Team.BLUE: './Images/blue_pawn.png',
                Team.GREEN: './Images/green_pawn_d.png',
                Team.PURPLE: './Images/purple_pawn_d.png'}

color_matrix_rook = {Team.BLUE: './Images/blue_rook.png',
                Team.GREEN: './Images/green_rook_d.png',
                Team.PURPLE: './Images/purple_rook_d.png'}

color_matrix_queen = {Team.BLUE: './Images/blue_queen.png',
                Team.GREEN: './Images/green_queen.png',
                Team.PURPLE: './Images/purple_queen.png'}

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
            highlight_moves(maxMovement(2, 0, (square.row, square.col), (square.row, square.col)),square.piece.team)
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


delegated_piece = None
delegated_commander = None
human_piece_delegated = False
action_count = 0
turn = True  # True maeans human move
delegation_mode = False
commander = Team.GREEN


class DelegatedPiece:
    def __init__(self, pos: (int, int), team: Team):
        self.pos = pos
        self.team = team


def delegate(chosen_square):
    global delegated_piece
    global delegated_commander
    global action_count
    global human_piece_delegated
    global delegation_mode
    if (chosen_square.piece is not None) and (chosen_square.piece.team not in enemies[Team.BLUE]):
        if (chosen_square.piece.type is not Type.KING) and (chosen_square.piece.type is not Type.BISHOP):
            delegated_piece = chosen_square.piece
            row, col = chosen_square.row, chosen_square.col
            return DelegatedPiece((row, col), chosen_square.piece.team)
            print('deligated piece selected')
            # deligation_count += 1
        elif (chosen_square.piece.type is Type.KING) or (chosen_square.piece.type is Type.BISHOP):
            if chosen_square.piece.team is Team.BLUE:
                delegated_commander = blue_commander
            elif chosen_square.piece.team is Team.GREEN:
                delegated_commander = green_commander
            elif chosen_square.piece.team is Team.PURPLE:
                delegated_commander = purple_commander
            else:
                pass
            # deligation_count += 1
            print('deligated commander selected')
        if (delegated_piece is not None) and (delegated_commander is not None):
            if (delegated_piece.type) == Type.PAWN and (delegated_piece.team == Team.BLUE):
                delegated_piece.switch_sprite(color_matrix_pawn[delegated_commander.leader.team])
            elif (delegated_piece.type == Type.ROOK) and (delegated_piece.team == Team.BLUE):
                delegated_piece.switch_sprite(color_matrix_rook[delegated_commander.leader.team])
            elif (delegated_piece.type == Type.QUEEN) and (delegated_piece.team == Team.BLUE):
                delegated_piece.switch_sprite(color_matrix_queen[delegated_commander.leader.team])
            else:
                print("Invalid piece type for delegation")
            blue_commander.delegate(delegated_piece, delegated_commander)
            human_piece_delegated = True
            action_count += 1
            reset_delegation()
            print('deligation completed')

def recall(chosen_square):
    global recalled_piece
    global current_commander
    global action_count
    global human_piece_delegated
    #selects chosen piece for recall
    if (chosen_square.piece is not None) and (chosen_square.piece.team not in enemies[Team.BLUE]):
        if(chosen_square.piece.type is not Type.BISHOP) and (chosen_square.piece.type is not Type.KING) and (chosen_square.piece.team is not Team.BLUE):
            recalled_piece = chosen_square.piece

    #checks for the commander of the currently delegated piece
    if recalled_piece is not None:
        if recalled_piece.team is Team.GREEN:
            current_commander = green_commander
        elif recalled_piece.team is Team.PURPLE:
            current_commander = purple_commander

    #calls recall function and switches sprite back to blue
    if (recalled_piece) is not None and (current_commander is not None):
        if recalled_piece.type == Type.PAWN:
            recalled_piece.switch_sprite(color_matrix_pawn[Team.BLUE])
        elif recalled_piece.type == Type.ROOK:
            recalled_piece.switch_sprite(color_matrix_rook[Team.BLUE])
        elif recalled_piece.type == Type.QUEEN:
            recalled_piece.switch_sprite(color_matrix_queen[Team.BLUE])
        else:
            print("Invalid piece type for recall")
        blue_commander.recall(recalled_piece, current_commander)
        human_piece_delegated = False
        action_count += 1
        reset_recall()
        print('Recall complete')

def reset_delegation():
    global delegated_piece
    delegated_piece = None
    global delegated_commander
    delegated_commander = None
    global delegation_mode
    delegation_mode = False

def reset_recall():
    global recalled_piece
    recalled_piece = None
    global current_commander
    current_commander = None
    global delegation_mode
    delegation_mode = False

def display_turn_count():
    pass
# ActionCount Text
class Action_Counttxt(Sprite):
    def __init__(self, pos, text, font_size, txt_col, bg_col, bg_hover, action=None):
        self.action = action
       #self.selected = False
        unselected_img = create_text_surface(text, font_size, txt_col, bg_col)
        #highlighted_img = create_text_surface(text, font_size * 1.3, txt_col, bg_hover)

        self.images = unselected_img
        self.rects = unselected_img.get_rect(center=pos)
        super().__init__()

    @property
    def img(self):
        return self.images

    @property
    def rect(self):
        return self.rects

    def moused_over(self, mouse_pos, mouse_down):
        if self.rect.collidepoint(mouse_pos):
            self.selected = False
            #if mouse_down:
                #return self.action
      #  else:
          #  self.selected = False

    def draw(self, surface):
        surface.blit(self.img, self.rect)

# Current Turn Text
class WhosTurn(Sprite):
    def __init__(self, pos, text, font_size, txt_col, bg_col, bg_hover, action=None):
        self.action = action
       #self.selected = False
        unselected_img = create_text_surface(text, font_size, txt_col, bg_col)
        #highlighted_img = create_text_surface(text, font_size * 1.3, txt_col, bg_hover)

        self.images = unselected_img
        self.rects = unselected_img.get_rect(center=pos)
        super().__init__()

    @property
    def img(self):
        return self.images

    @property
    def rect(self):
        return self.rects

    def moused_over(self, mouse_pos, mouse_down):
        if self.rect.collidepoint(mouse_pos):
            self.selected = False
            #if mouse_down:
                #return self.action
      #  else:
          #  self.selected = False

    def draw(self, surface):
        surface.blit(self.img, self.rect)
# class for interactable elements that have text
class DelegateButton(Sprite):
    def __init__(self, pos, text, font_size, txt_col, bg_col, bg_hover, action=None):
        self.action = action
        self.selected = False
        #self.remain_selected = False
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
                #self.remain_selected = True
                delegation_mode = True
                print('!!!!!!!!!!!!!!!test!!!!!!!!!!!!!!!!!')
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
    Delegate_Button = DelegateButton(pos=(WIDTH-100, 350),
                                     font_size=25,
                                     txt_col=BLACK,
                                     bg_col=buttoncolor,
                                     text="Delegate",
                                     bg_hover=buttonhover,
                                     action=GameState.Play)
    Recall_Button = DelegateButton(pos=(WIDTH-100, 450),
                           font_size=25,
                           txt_col=BLACK,
                           bg_col=buttoncolor,
                           text="Recall",
                           bg_hover=buttonhover,
                           action=GameState.Play)
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

    Action_Counter = Action_Counttxt(pos=(WIDTH - 1100, 650),
                           font_size=25,
                           txt_col=BLACK,
                           bg_col=buttoncolor,
                           text="Action Count: ",
                           bg_hover=buttonhover,
                           action=GameState.Play)

    Current_turn = WhosTurn(pos=(WIDTH - 1060, 700),
                                     font_size=25,
                                     txt_col=BLACK,
                                     bg_col=buttoncolor,
                                     text="Current Turn: Human",
                                     bg_hover=buttonhover,
                                     action=GameState.Play)

    buttons = [Home_Button, Delegate_Button, Resign_Button, End_Turn_Button, Rules_Button, Recall_Button, Action_Counter, Current_turn]


    current_square = None
    global action_count
    global turn
    delegated_pieces = []
    global delegation_mode
    global commander
    captured_pieces = []
    #chosen_team = None
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
        #print('action count', action_count)

        if turn:
            #print('human turn')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
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

                        if Delegate_Button.selected:
                            #if (human_piece_deligated is not True):
                            #if not delegation_mode:
                            #    delegation_mode = True
                                #print('!!!!!!!!!!!!!!!!!!!check point!!!!!!!!!!!!!!!!!!!!!!!!')
                            #else:
                            print('check point')
                            result = delegate(chosen_square)
                            if result is not None:
                                delegated_pieces.append(result)
                        elif Recall_Button.selected:
                            recall(chosen_square)
                            delegated_pieces.remove(result)
                        else:
                            # conditions for selected_square
                            if current_square is None:
                                if chosen_square.piece is None:
                                    pass
                                else:
                                    current_square = chosen_square
                                    potential_piece_moves(chosen_square)
                                    if current_square.piece == blue_commander.leader:
                                        print("Blue pieces")
                                        blue_commander.see_pieces()
                                    elif current_square.piece == green_commander.leader:
                                        print("Green pieces")
                                        green_commander.see_pieces()
                                    elif current_square.piece == purple_commander.leader:
                                        print("Purple pieces")
                                        purple_commander.see_pieces()

                            else:  # a piece is currently selected
                                #global chosen_team
                                """
                                if chosen_square.piece is None:
                                    print('chosen square is none')
                                else:
                                    print('chosen square is not none')
                                """
                                """
                                if chosen_square.piece is not None: # clicking alternative piece on your side
                                    remove_highlights()
                                    current_square = chosen_square
                                    potential_piece_moves(chosen_square)
                                """
                                if (chosen_square.color is WHITE) or (chosen_square.color is GREY):  # lets you unselect current piece
                                    remove_highlights()
                                    current_square = None
                                elif chosen_square.color is BLUE: # deals with movement
                                    if chosen_square.piece is None: # there is a piece there
                                        """
                                            current_square = None
                                            remove_highlights()
                                            move_piece(current_square, chosen_square)
                                            action_count += 1
                                        else:
                                        """
                                        remove_highlights()
                                        move_piece(current_square, chosen_square)
                                        current_square = None
                                        action_count += 1
                                elif chosen_square.color is BLACK:
                                    if attack(current_square.piece.type.value, chosen_square.piece.type.value) is True:
                                        captured_pieces.append(chosen_square.piece)
                                        chosen_square.piece = None
                                        move_piece(current_square, chosen_square)
                                        current_square = None
                                        action_count += 1
                                        remove_highlights()
                                    else:
                                        remove_highlights()
                                        action_count += 1
                                        current_square = None
                                else:
                                    pass
                else:
                    pass
        else: # AI starts
            print('hello from computer')
            reset_turn()
            # after AI is done enable next line
            turnChange()

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

