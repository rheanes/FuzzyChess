import sys
import pygame
import time

from GameFunctions import attack
from common import *
from board import *

from guielements import *

DEFAULT_IMAGE_SIZE = (GAME_WIDTH / 8, GAME_WIDTH / 8)
SQUARE_WIDTH = SQUARE_HEIGHT = GAME_WIDTH / 8
clock = pygame.time.Clock()

delegation_mode = False
recall_mode = False

def turnChange():
    global turn
    if not turn:
        turn = True
    elif turn:
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
    pygame.draw.rect(screen, BACKGROUND, (0, GAME_WIDTH + 1, WIDTH, HEIGHT))
    # print('testing')


# These are the potential moves
def potential_piece_moves(square: Square):
    piece = square.piece
    if (piece.team == Team.YELLOW or (piece.team == Team.RED) or piece.team == Team.ORANGE):
        if piece.type == Type.PAWN:
            highlight_moves(pawn_moves_top((square.row, square.col)), square.piece.team)
        elif (piece.type == Type.KING) or (piece.type == Type.QUEEN):
            highlight_moves(
                maxMovement(3, 0, (square.row, square.col), (square.row, square.col), square.piece.type.value),
                square.piece.team)
        elif piece.type == Type.ROOK:
            highlight_moves(
                maxMovement(2, 0, (square.row, square.col), (square.row, square.col), square.piece.type.value),
                square.piece.team)
        elif piece.type == Type.BISHOP:
            highlight_moves(
                maxMovement(2, 0, (square.row, square.col), (square.row, square.col), square.piece.type.value),
                square.piece.team)
        elif piece.type == Type.KNIGHT:
            highlight_moves(
                maxMovement(4, 0, (square.row, square.col), (square.row, square.col), square.piece.type.value),
                square.piece.team)
    elif (piece.team == Team.GREEN or piece.team == Team.BLUE or piece.team == Team.PURPLE):
        if piece.type == Type.PAWN:
            highlight_moves(pawn_moves_bottom((square.row, square.col)), square.piece.team)
        if (piece.type == Type.KING) or (piece.type == Type.QUEEN):
            highlight_moves(
                maxMovement(3, 0, (square.row, square.col), (square.row, square.col), square.piece.type.value),
                square.piece.team)
        elif piece.type == Type.ROOK:
            highlight_moves(
                maxMovement(2, 0, (square.row, square.col), (square.row, square.col), square.piece.type.value),
                square.piece.team)
        elif piece.type == Type.BISHOP:
            highlight_moves(
                maxMovement(2, 0, (square.row, square.col), (square.row, square.col), square.piece.type.value),
                square.piece.team)
        elif piece.type == Type.KNIGHT:
            highlight_moves(
                maxMovement(4, 0, (square.row, square.col), (square.row, square.col), square.piece.type.value),
                square.piece.team)


# Only called after a Knight moves. Is used to highlight enemies in the general area
def knightAttack(square: Square):
    highlight_moves(knightAttackPieces((square.row, square.col), (square.row, square.col)), square.piece.team)


delegated_piece = None
delegated_commander = None
human_piece_delegated = False
action_count = len(player_commanders)
humanComms = len(player_commanders)
aiComms = len(ai_commanders)
turn = True  # True maeans human move
delegation_mode = False
recalled_piece = None
current_commander = None
recall_mode = False
commander = Team.GREEN
deployed_team = []


class DelegatedPiece:
    def __init__(self, pos: (int, int), team: Team):
        self.pos = pos
        self.team = team


# TODO: don't allow delegated pieces to be delegated
# TODO: currently pieces that have been moved cannot be delegated(i.e causes a bug where the piece activates the movement functions even when the delegation button has been pressed)
def delegate(chosen_square):
    global delegated_piece
    global delegated_commander
    global action_count
    global human_piece_delegated
    global delegation_mode
    if (chosen_square.piece is not None) and (chosen_square.piece.team not in enemies[Team.BLUE]):
        if (chosen_square.piece.type is not Type.KING) and \
                (chosen_square.piece.type is not Type.BISHOP) and \
                (chosen_square.piece.delegated is not True):
            delegated_piece = chosen_square.piece
            row, col = chosen_square.row, chosen_square.col
            return DelegatedPiece((row, col), chosen_square.piece.team)
            print('deligated piece selected')
        elif (chosen_square.piece.type is Type.KING) or (chosen_square.piece.type is Type.BISHOP):
            if chosen_square.piece.team is Team.BLUE:
                delegated_commander = blue_commander
            elif chosen_square.piece.team is Team.GREEN:
                delegated_commander = green_commander
            elif chosen_square.piece.team is Team.PURPLE:
                delegated_commander = purple_commander
            else:
                pass
            print('deligated commander selected')
        if (delegated_piece is not None) and (delegated_commander is not None):
            if (delegated_piece.type) == Type.PAWN and (delegated_piece.team == Team.BLUE):
                delegated_piece.switch_sprite(del_matrix_pawn[delegated_commander.leader.team])
            elif (delegated_piece.type == Type.ROOK) and (delegated_piece.team == Team.BLUE):
                delegated_piece.switch_sprite(del_matrix_rook[delegated_commander.leader.team])
            elif (delegated_piece.type == Type.QUEEN) and (delegated_piece.team == Team.BLUE):
                delegated_piece.switch_sprite(del_matrix_queen[delegated_commander.leader.team])
            else:
                print("Invalid piece type for delegation")
            blue_commander.delegate(delegated_piece, delegated_commander)
            human_piece_delegated = True
            reset_delegation()
            blue_commander.see_pieces()
            print('deligation completed')

def recall(chosen_square):
    global recalled_piece
    global current_commander
    global action_count
    global human_piece_delegated
    global recall_mode
    # selects chosen piece for recall
    if (chosen_square.piece is not None) and (chosen_square.piece.team not in enemies[Team.BLUE]):
        if(chosen_square.piece.type is not Type.BISHOP) and (chosen_square.piece.type is not Type.KING):
            recalled_piece = chosen_square.piece

    #checks for the commander of the currently delegated piece
    if recalled_piece is not None:
        if recalled_piece in green_commander.troops:
            current_commander = green_commander
        elif recalled_piece in purple_commander.troops:
            current_commander = purple_commander

    #calls recall function and switches sprite back to blue
    if (recalled_piece is not None) and (current_commander is not None):
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
    global recall_mode
    recall_mode = False

# ActionCount Text
class Action_Counttxt(Sprite):
    def __init__(self, pos, text, font_size, txt_col, bg_col, bg_hover, action=None):
        self.action = action
        # self.selected = False
        self.text = text
        self.pos = pos
        self.font_size = font_size
        self.txt_col = txt_col
        self.bg_col = bg_col
        # unselected_img = create_text_surface(self.text, font_size, txt_col, bg_col)
        # highlighted_img = create_text_surface(text, font_size * 1.3, txt_col, bg_hover)

        # self.images = unselected_img
        # self.rects = unselected_img.get_rect(center=pos)
        super().__init__()

    # def update_count(self, count):
    #    self.text = count

    @property
    def img(self):
        return create_text_surface(self.text, self.font_size, self.txt_col, self.bg_col)

    @property
    def rect(self):
        return create_text_surface(self.text, self.font_size, self.txt_col, self.bg_col).get_rect(center=self.pos)

    def moused_over(self, mouse_pos, mouse_down):
        pass
    #    if self.rect.collidepoint(mouse_pos):
    #        self.selected = False
    #       if mouse_down:
    #        return self.action

    #  else:
    #  self.selected = False

    def draw(self, surface):
        surface.blit(self.img, self.rect)

# class for interactable elements that have text
class DelegateButton(Sprite):
    def __init__(self, pos, text, font_size, txt_col, bg_col, bg_hover, action=None):
        self.action = action
        self.selected = False
        # self.remain_selected = False
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
                # self.remain_selected = True
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


class RecallButton(Sprite):
    def __init__(self, pos, text, font_size, txt_col, bg_col, bg_hover, action=None):
        self.action = action
        self.selected = False
        # self.remain_selected = False
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
        global recall_mode
        if self.rect.collidepoint(mouse_pos):
            self.selected = True
            if mouse_down:
                # self.remain_selected = True
                recall_mode = True
                print('!!!!!!!!!!!!!!!test!!!!!!!!!!!!!!!!!')
                return self.action
        else:
            if recall_mode:
                self.selected = True
            else:
                self.selected = False

    def draw(self, surface):
        surface.blit(self.img, self.rect)


# Sets the commanders turns to False to prevent their corp from making another action
def end_commander_turn(team: Team):
    global deployed_team
    deployed_team.append(team)
    if (team is Team.BLUE):
        blue_commander.action = False
    elif (team is Team.GREEN):
        green_commander.action = False
    elif (team is Team.PURPLE):
        purple_commander.action = False
    elif (team is Team.RED):
        red_commander.action = False
    elif (team is Team.YELLOW):
        yellow_commander.action = False
    elif (team is Team.ORANGE):
        orange_commander.action = False


# Checks to see if a given corp has acted on a given turn. False means they have, true means they haven't
def checkCommanderTurn(team: Team):
    if (team is Team.BLUE):
        return blue_commander.action
    elif (team is Team.GREEN):
        return green_commander.action
    elif (team is Team.PURPLE):
        return purple_commander.action
    elif (team is Team.RED):
        return red_commander.action
    elif (team is Team.YELLOW):
        return yellow_commander.action
    elif (team is Team.ORANGE):
        return orange_commander.action


# Removes the commander from their list (used for AI and determining action count)
def removeCommander(team: Team):
    global player_commanders
    global ai_commanders
    if team is Team.GREEN:
        player_commanders.remove(green_commander)
    elif team is Team.PURPLE:
        player_commanders.remove(purple_commander)
    elif team is Team.YELLOW:
        ai_commanders.remove(yellow_commander)
    elif team is Team.ORANGE:
        ai_commanders.remove(orange_commander)


# Resets the turns, including any corp actions
def reset_turn():
    global human_piece_deligated
    human_piece_deligated = False
    global action_count
    global player_commanders
    global ai_commanders
    if turn is True:
        action_count = len(player_commanders)
        for x in player_commanders:
            x.action = True
    elif turn is False:
        action_count = len(ai_commanders)
        for x in ai_commanders:
            x.action = True


def message_box(text):
    print(text)


# TODO:
def adjacent_enemies(pos: tuple[int, int], team: Team):
    row = pos[0]
    col = pos[1]
    new_pos_list = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                    (row, col - 1), (row, col + 1),
                    (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]

    consensus = False

    for new_pos in new_pos_list:
        print(new_pos)
        if on_board(new_pos):
            print(new_pos)
            if (board[new_pos[0]][new_pos[1]].piece is not None) and \
                    (board[new_pos[0]][new_pos[1]].piece.team in enemies[team]):
                return True

    return consensus


FirstRun = True

#This will take in a piece and the current team.
#Then it will remove the
def remove_piece(piece):
    print('removing piece.')
    team = piece.team
    if team == team.RED:
        red_commander.troops.remove(piece)

    elif team == team.YELLOW:
        yellow_commander.troops.remove(piece)

    elif team == team.ORANGE:
        orange_commander.troops.remove(piece)

    elif piece.team == team.BLUE:
        blue_commander.troops.remove(piece)

    elif piece.team == team.PURPLE:
        purple_commander.troops.remove(piece)

    elif piece.team == team.GREEN:
        green_commander.troops.remove(piece)

    return

def playgame(screen):
    Home_Button = button(pos=(WIDTH - 100, 100),
                         font_size=25,
                         txt_col=BLACK,
                         bg_col=buttoncolor,
                         text="Home",
                         bg_hover=buttonhover,
                         action=GameState.Home)

    Rules_Button = button(pos=(WIDTH - 100, 200),
                          font_size=25,
                          txt_col=BLACK,
                          bg_col=buttoncolor,
                          text="Rules",
                          bg_hover=buttonhover,
                          action=GameState.Rules)
    Delegate_Button = DelegateButton(pos=(WIDTH - 100, 350),
                                     font_size=25,
                                     txt_col=BLACK,
                                     bg_col=buttoncolor,
                                     text="Delegate",
                                     bg_hover=buttonhover,
                                     action=GameState.Play)
    Recall_Button = RecallButton(pos=(WIDTH-100, 450),
                           font_size=25,
                           txt_col=BLACK,
                           bg_col=buttoncolor,
                           text="Recall",
                           bg_hover=buttonhover,
                           action=GameState.Play)
    End_Turn_Button = button(pos=(WIDTH - 100, 550),
                             font_size=25,
                             txt_col=BLACK,
                             bg_col=buttoncolor,
                             text="End Turn",
                             bg_hover=buttonhover,
                             action=GameState.EndTurn)
    Resign_Button = button(pos=(WIDTH - 100, 650),
                           font_size=25,
                           txt_col=BLACK,
                           bg_col=buttoncolor,
                           text="Resign",
                           bg_hover=buttonhover,
                           action=GameState.Loss)

    Action_Counter = Action_Counttxt(pos=(WIDTH - 1090, 650),
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

    Bone_Pile = BoneP(pos=(WIDTH - 1125, 750),
                            font_size=25,
                            txt_col=BLACK,
                            bg_col=buttoncolor,
                            text="Bone Pile",
                            bg_hover=buttonhover,
                            action=GameState.Play)

    buttons = [Home_Button, Delegate_Button, Resign_Button, End_Turn_Button, Rules_Button, Recall_Button,
               Action_Counter, Current_turn, Bone_Pile]

    current_square = None
    global action_count
    global turn
    delegated_pieces = []
    global delegation_mode
    global recall_mode
    global commander
    global blue_commander
    global red_commander
    captured_pieces = []
    global deployed_team
    action_limit = 3
    knight_special_turn = False
    human_team = [Team.GREEN, Team.BLUE, Team.PURPLE]

    global FirstRun
    if FirstRun:
        create_board()
        FirstRun = False

    while True:
        mouse_down = False
        pygame.mouse.get_pressed()
        # print('Delegation: ', Delegate_Button.selected)
        # print('Delegation remain selected: ', Delegate_Button.remain_selected)
        # print('Delegation Mode: ', delegation_mode)
        # print('action count', action_count)
        Action_Counter.text = 'Action Count: ' + str(action_count)

        if action_count == 0:
            turnChange()
            reset_turn()

        if turn:
            # print('human turn')
            # print('enter pygame events')
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif(event.type == KEYDOWN):
                    if event.key == K_ESCAPE:
                        return GameState.Escape
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mouse_down = True

                    x, y = pygame.mouse.get_pos()
                    # if you dont click on the game board
                    if x >= GAME_WIDTH or y >= GAME_WIDTH:
                        if End_Turn_Button.selected:
                            turnChange()
                            reset_turn()

                    # if you do click on the game board
                    else:
                        row, col = find_square_coordinates((x, y))
                        # print('row ', row, ' col ', col)
                        chosen_square = board[row][col]  # refers to the square clicked by the mouse
                        """ current causes issues
                        # prevents clicking on enemy pieces
                        if (chosen_square.piece.team in enemies) and chosen_square.piece:
                            pass
                        else:
                        """

                        if Delegate_Button.selected and (chosen_square.piece.team not in deployed_team) and human_piece_delegated is not True:
                            # if (human_piece_deligated is not True):
                            # if not delegation_mode:
                            #    delegation_mode = True
                            # print('!!!!!!!!!!!!!!!!!!!check point!!!!!!!!!!!!!!!!!!!!!!!!')
                            # else:
                            # print('check point')
                            result = delegate(chosen_square)
                            if result is not None:
                                delegated_pieces.append(result)

                        elif Recall_Button.selected and human_piece_delegated is not True:
                            recall(chosen_square)
                            #delegated_pieces.remove(result)
                        else:
                            # if chosen_square.piece.team in human_team:
                            # conditions for selected_square
                            if current_square is None:
                                if chosen_square.piece is None:
                                    pass
                                elif (checkCommanderTurn(chosen_square.piece.team) or chosen_square.piece.type is Type.KNIGHT) and (chosen_square.piece.team not in enemies[Team.BLUE]):
                                    if chosen_square.piece.type is Type.KNIGHT:
                                        if knight_special_turn:
                                            current_square = chosen_square
                                            knightAttack(chosen_square)

                                        elif not knight_special_turn and checkCommanderTurn(chosen_square.piece.team):
                                            current_square = chosen_square
                                            potential_piece_moves(chosen_square)
                                    elif not knight_special_turn:
                                        current_square = chosen_square
                                        potential_piece_moves(chosen_square)
                                        # if chosen_square.piece is purple_commander.leader:
                                        # print("purple pieces")
                                        # purple_commander.see_pieces

                            else:  # a piece is currently selected
                                """
                                if chosen_square.piece is not None: # clicking alternative piece on your side
                                    remove_highlights()
                                    current_square = chosen_square
                                    potential_piece_moves(chosen_square)
                                """
                                #This check ensures that the chosen corp hasn't worked. If a knight is selected, then
                                #we bypass this condition if the knight's special turn is enabled.
                                if (checkCommanderTurn(current_square.piece.team) or current_square.piece.type is Type.KNIGHT) and (current_square.piece.team not in enemies[Team.BLUE]):
                                    if (chosen_square.color is WHITE) or (
                                            chosen_square.color is GREY):  # lets you unselect current piece
                                        remove_highlights()
                                        current_square = None
                                    elif knight_special_turn:
                                        if current_square.piece.type is Type.KNIGHT and chosen_square.color is BLACK:
                                            if attack(current_square.piece.type.value,
                                                      chosen_square.piece.type.value) is True:
                                                captured_pieces.append(chosen_square.piece)
                                                end_commander_turn(chosen_square.piece.team)

                                                if chosen_square.piece.type is Type.BISHOP:
                                                    removeCommander(chosen_square.piece)
                                                    remove_team(chosen_square.piece.team)
                                                elif (chosen_square.piece.type is Type.KING) and \
                                                        (chosen_square.piece.team is Team.RED):
                                                    return GameState.Win

                                                chosen_square.piece = None
                                                move_piece(current_square, chosen_square)
                                                current_square = None
                                                action_count -= 1
                                                remove_highlights()
                                                knight_special_turn = False
                                            else:
                                                end_commander_turn(current_square.team)
                                                chosen_square = None
                                                current_square = None
                                                remove_highlights()
                                                action_count -= 1
                                                knight_special_turn = False

                                    elif (chosen_square.color is BLUE) and \
                                            (current_square.color not in deployed_team) and \
                                            (chosen_square.piece is None):  # deals with movement

                                        """
                                            current_square = None
                                            remove_highlights()
                                            move_piece(current_square, chosen_square)
                                            action_count -= 1
                                        else:
                                        """
                                        if current_square.piece.type == Type.KNIGHT and adjacent_enemies((chosen_square.row, chosen_square.col), current_square.piece.team):
                                            # action_count -= 1
                                            # print('action count decreased')
                                            knight_team = current_square.piece.team
                                            if knight_team == Team.GREEN:
                                                green_commander.has_moved = True
                                            elif knight_team == Team.PURPLE:
                                                purple_commander.has_moved = True
                                            elif knight_team == Team.BLUE:
                                                blue_commander.has_moved = True
                                            else:
                                                pass
                                            end_commander_turn(current_square.piece.team)
                                            knight_special_turn = True

                                        if not knight_special_turn:
                                            end_commander_turn(current_square.piece.team)
                                            action_count -= 1
                                            #print('action count increased')
                                        else:
                                            #print('action count not increased')
                                            return

                                        move_piece(current_square, chosen_square)
                                        remove_highlights()
                                        current_square = None

                                    elif (chosen_square.color is BLACK) and (current_square.color not in deployed_team):
                                        if attack(current_square.piece.type.value,
                                                  chosen_square.piece.type.value) is True:
                                            captured_pieces.append(chosen_square.piece)
                                            remove_piece(chosen_square.piece)
                                            end_commander_turn(chosen_square.piece.team)

                                            if chosen_square.piece.type is Type.BISHOP:
                                                #We decrement the counter to ensure the actions done by a human are limited based on the number of commanders we have
                                                removeCommander(chosen_square.piece.team)
                                                remove_team(chosen_square.piece.team)
                                            elif (chosen_square.piece.type is Type.KING) and (
                                                    chosen_square.piece.team is Team.RED):
                                                return GameState.Win
                                            elif (chosen_square.piece.type is Type.KING) and (
                                                    chosen_square.piece.team is Team.BLUE):
                                                return GameState.Loss

                                            chosen_square.piece = None
                                            if (current_square.piece.type is not Type.ROOK):
                                                move_piece(current_square, chosen_square)
                                                end_commander_turn(chosen_square.piece.team)
                                            else:
                                                end_commander_turn(current_square.piece.team)
                                            current_square = None
                                            action_count -= 1
                                            remove_highlights()
                                        else:
                                            remove_highlights()
                                            end_commander_turn(current_square.piece.team)
                                            action_count -= 1
                                            current_square = None
                                else:
                                    remove_highlights()
                                    chosen_square = None
                                    current_square = None
                                    pass
                else:
                    pass
        elif not turn:  # AI starts
            Action_Counter.text = 'Action Count: ' + str(action_count)
            Current_turn.text = 'Current Turn: AI'
            # print('hello from computer')
            # after AI is done enable next line
            action_count -= 1
            # time.sleep(3)

            action_count -= 1
            # time.sleep(3)

            action_count -= 1
        # time.sleep(3)

        update_display(screen)
        for b in buttons:
            ui_action = b.moused_over(pygame.mouse.get_pos(), mouse_down)
            if ui_action is not None:
                # if b == Deligate_Button:

                return ui_action
            b.draw(screen)
        pygame.display.flip()
        clock.tick(15)
