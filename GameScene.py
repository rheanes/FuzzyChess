import sys
import pygame
import time

from GameFunctions import attack
from common import *
from board import *
from ai import evaluation, available_moves, generate_moves, greedy_search, generateRandomMove
from guielements import *
#from ai import *

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
            if square.piece is not None and square.piece.image is not None:
                screen.blit(pygame.transform.scale(square.piece.image, DEFAULT_IMAGE_SIZE), (x_pos, y_pos))
                # screen.blit(pygame.transform.scale(starting_order[(square.row, square.col)], DEFAULT_IMAGE_SIZE), (square.x_pos, square.y_pos))
    """ Draw board lines """
    gap = GAME_WIDTH // 8
    for i in range(9):
        pygame.draw.line(screen, BLACK, (0, i * gap), (GAME_WIDTH, i * gap))
        for j in range(9):
            pygame.draw.line(screen, BLACK, (j * gap, 0), (j * gap, GAME_WIDTH))

    pygame.draw.rect(screen, BACKGROUND, (0, GAME_WIDTH + 1, WIDTH, HEIGHT))

    #Creates the bone pile
    for row in bonePile:
        for square in row:
            x_pos = square.col * (GAME_WIDTH // 8)
            y_pos = square.row * (GAME_WIDTH // 8) + 710
            pygame.draw.rect(screen, square.color, (x_pos, y_pos, GAME_WIDTH, HEIGHT))
            if square.piece is not None and square.piece.image is not None:
                screen.blit(pygame.transform.scale(square.piece.image, DEFAULT_IMAGE_SIZE), (x_pos, y_pos))

    for i in range(4):
        pygame.draw.line(screen, BLACK, (0, 710 + i * gap), (GAME_WIDTH, 710 + i * gap))
        for j in range(9):
            pygame.draw.line(screen, BLACK, (j * gap, 710), (j * gap, HEIGHT))

    pygame.draw.rect(screen, BACKGROUND, (GAME_WIDTH + 1, 0, WIDTH, HEIGHT))
    # print('testing')

#Adds pieces to the bone pile. AI pieces appear in the upper rows, player pieces on the lower ones
def insertBonepile(): #
    global ai_captured_pieces
    global player_captured_pieces
    aiRow = 0
    aiCol = 0
    for troop in ai_captured_pieces:
        bonePile[aiRow][aiCol].piece = troop
        aiCol += 1
        if aiCol > 7:
            aiCol = 0
            aiRow += 1
    humRow = 2
    humCol = 0
    for troop in player_captured_pieces:
        bonePile[humRow][humCol].piece = troop
        humCol += 1
        if humCol > 7:
            humCol = 0
            humRow += 1

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

def findActionCount(array):
    num = 0
    for c in array:
        if c.action == True:
            num += 1

    return num

delegated_piece = None
delegated_commander = None
human_piece_delegated = False
action_count = findActionCount(player_commanders)
humanComms = len(player_commanders)
aiComms = len(ai_commanders)
turn = True  # True maeans human move
delegation_mode = False
commMoveMode = False
recalled_piece = None
current_commander = None
recall_mode = False
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
        if (chosen_square.piece.type is not Type.KING) and \
                (chosen_square.piece.type is not Type.BISHOP):
            #Modified here to include the check later on. THis is to provide an exit condition if we don't select a valid piece
                if (chosen_square.piece.delegated is not True):
                    delegated_piece = chosen_square.piece
                    row, col = chosen_square.row, chosen_square.col
                    print('deligated piece selected')
                    return DelegatedPiece((row, col), chosen_square.piece.team)
                else:
                    reset_delegation()
                    print("Invalid choice")
                    return

        elif (chosen_square.piece.type is Type.KING) or (chosen_square.piece.type is Type.BISHOP):
            if chosen_square.piece.team is Team.BLUE:
                delegated_commander = blue_commander
            elif chosen_square.piece.team is Team.GREEN:
                delegated_commander = green_commander
            elif chosen_square.piece.team is Team.PURPLE:
                delegated_commander = purple_commander
            else:
                pass

        #A Bishop may delegate no more than 6 troops at a given time
        if(len(delegated_commander.troops) >= 6):
            reset_delegation()
            print("Max delegation reached")
            return

        print('deligated commander selected')
        if (delegated_piece is not None) and (delegated_commander is not None):
            if (delegated_piece.type) == Type.PAWN and (delegated_piece.team == Team.BLUE):
                delegated_piece.switch_sprite(del_matrix_pawn[delegated_commander.leader.team])
            elif (delegated_piece.type == Type.ROOK) and (delegated_piece.team == Team.BLUE):
                delegated_piece.switch_sprite(del_matrix_rook[delegated_commander.leader.team])
            elif (delegated_piece.type == Type.QUEEN) and (delegated_piece.team == Team.BLUE):
                delegated_piece.switch_sprite(del_matrix_queen[delegated_commander.leader.team])

                #Added to deal with delegation of knights if and when a Bishop dies
            elif (delegated_piece.type == Type.KNIGHT) and (delegated_piece.team == Team.BLUE):
                delegated_piece.switch_sprite(del_matrix_queen[delegated_commander.leader.team])
            else:
                print("Invalid piece type for delegation")
                #If we don't select a valid piece, we want to reset everything
                reset_delegation()
                return
            blue_commander.delegate(delegated_piece, delegated_commander)

            #Sets the given pieces to the team they are going to.
            if delegated_commander is green_commander:
                delegated_piece.team = Team.GREEN
            elif delegated_commander is purple_commander:
                delegated_piece.team = Team.PURPLE
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
        if(chosen_square.piece.type is not Type.BISHOP) and (chosen_square.piece.type is not Type.KING) and chosen_square.piece.delegated is True:
            recalled_piece = chosen_square.piece
            print("Recalling " + str(recalled_piece))
        else:
            reset_recall()
            print("Invalid choice")
            return
    else:
        reset_recall()
        print("Invalid choice")
        return

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
        recalled_piece.team = Team.BLUE
        human_piece_delegated = True
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

    # selects different button images depending on if the mouse is hovered over it
    def moused_over(self, mouse_pos, mouse_down):
        global delegation_mode
        if self.rect.collidepoint(mouse_pos):
            self.selected = True
            if mouse_down and human_piece_delegated is False and checkCommanderTurn(Team.BLUE) and recall_mode is False:
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

    # selects different button images depending on if the mouse is hovered over it
    def moused_over(self, mouse_pos, mouse_down):
        global recall_mode
        if self.rect.collidepoint(mouse_pos):
            self.selected = True
            if mouse_down and human_piece_delegated is False and checkCommanderTurn(Team.BLUE) and delegation_mode is False:
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

#This class is for use of the Commander's Free Movement. They are able to move a small amount depending
#on the piece. Kings can move 2 spaces, and Bishops can move one space.
class CommFreeMove(Sprite):
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

    # selects different button images depending on if the mouse is hovered over it
    def moused_over(self, mouse_pos, mouse_down):
        global commMoveMode
        if self.rect.collidepoint(mouse_pos):
            self.selected = True
            if mouse_down and delegation_mode is False and recall_mode is False:
                # self.remain_selected = True
                commMoveMode = True
                print('Commander Movement Initiating')
                return self.action
        else:
            if commMoveMode:
                self.selected = True
            else:
                self.selected = False

    def draw(self, surface):
        surface.blit(self.img, self.rect)

# Sets the commanders turns to False in order to prevent their corp from making another action
def end_commander_turn(team: Team):
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

def checkCommanderHasMoved(team: Team):
    if (team is Team.BLUE):
        return blue_commander.has_moved
    elif (team is Team.GREEN):
        return green_commander.has_moved
    elif (team is Team.PURPLE):
        return purple_commander.has_moved
    elif (team is Team.RED):
        return red_commander.has_moved
    elif (team is Team.YELLOW):
        return yellow_commander.has_moved
    elif (team is Team.ORANGE):
        return orange_commander.has_moved


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
    global human_piece_delegated
    human_piece_delegated = False
    global action_count
    global player_commanders
    global ai_commanders
    if turn:
        action_count = len(player_commanders)
        print("PLayer Turn")
        for x in player_commanders:
            x.action = True
            x.has_moved = False
            x.authority = True
    elif not turn:
        action_count = len(ai_commanders)
        print("AI Turn")
        for x in ai_commanders:
            x.action = True
            x.has_moved = False
            x.authority = True


def message_box(text):
    print(text)


def adjacent_enemies(pos: tuple[int, int], team: Team):
    row = pos[0]
    col = pos[1]
    new_pos_list = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                    (row, col - 1), (row, col + 1),
                    (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]

    consensus = False

    for new_pos in new_pos_list:
        if on_board(new_pos):
            if (board[new_pos[0]][new_pos[1]].piece is not None) and \
                    (board[new_pos[0]][new_pos[1]].piece.team in enemies[team]):
                return True

    return consensus


FirstRun = True

#This will take in a piece and the current team.
#Then it will remove the
def remove_piece(piece):
    team = piece.team
    if team is Team.RED:
        red_commander.troops.remove(piece)

    elif team is Team.YELLOW:
        yellow_commander.troops.remove(piece)

    elif team is Team.ORANGE:
        orange_commander.troops.remove(piece)

    elif piece.team is Team.BLUE:
        blue_commander.troops.remove(piece)

    elif piece.team is Team.PURPLE:
        purple_commander.troops.remove(piece)

    elif piece.team is Team.GREEN:
        green_commander.troops.remove(piece)
    return

#This checks the commanders authority and returns its value. If we don't have a piece,
#or the selected piece isn't a commander, we return false
def commAuth(square: Square):
    global commMoveMode
    chosen_piece = square.piece

    if chosen_piece is not None:
        if chosen_piece.type is Type.KING or chosen_piece.type is Type.BISHOP:
            if chosen_piece.team is Team.BLUE:
                return blue_commander.authority
            elif chosen_piece.team is Team.PURPLE:
                return purple_commander.authority
            elif chosen_piece.team is Team.GREEN:
                return green_commander.authority
            elif chosen_piece.team is Team.RED:
                return red_commander.authority
            elif chosen_piece.team is Team.ORANGE:
                return orange_commander.authority
            elif chosen_piece.team is Team.YELLOW:
                return yellow_commander.authority
        else:
            commMoveMode = False
            return False
    else:
        commMoveMode = False
        return False

#Does special highlights for commander authority. They cannot capture while performing this movement.
def commMove(square: Square):
    piece = square.piece
    highlight_moves(commAuthMovement(1, 0, (square.row, square.col), (square.row, square.col),piece.value.value), piece.team)

def playgame(screen):
    #Button handles the free move commanders can make each turn
    Command_Move_Button = CommFreeMove(pos=(WIDTH - 300, 200),
                                     font_size=40,
                                     txt_col=BLACK,
                                     bg_col=buttoncolor,
                                     text="Com. Free Move",
                                     bg_hover=buttonhover,
                                     action=GameState.Play)

    Delegate_Button = DelegateButton(pos=(WIDTH - 300, 275),
                                     font_size=50,
                                     txt_col=BLACK,
                                     bg_col=buttoncolor,
                                     text="Delegate",
                                     bg_hover=buttonhover,
                                     action=GameState.Play)

    Recall_Button = RecallButton(pos=(WIDTH - 300, 350),
                           font_size=50,
                           txt_col=BLACK,
                           bg_col=buttoncolor,
                           text="Recall",
                           bg_hover=buttonhover,
                           action=GameState.Play)
    End_Turn_Button = button(pos=(WIDTH - 300, 425),
                             font_size=50,
                             txt_col=BLACK,
                             bg_col=buttoncolor,
                             text="End Turn",
                             bg_hover=buttonhover,
                             action=GameState.EndTurn)

    Action_Counter = Action_Counttxt(pos=(WIDTH - 300, 125),
                                     font_size=50,
                                     txt_col=BLACK,
                                     bg_col=buttoncolor,
                                     text="Action Count: ",
                                     bg_hover=buttonhover,
                                     action=GameState.Play)

    Current_turn = WhosTurn(pos=(WIDTH - 300, 50),
                            font_size=50,
                            txt_col=BLACK,
                            bg_col=buttoncolor,
                            text="Current Turn: Human",
                            bg_hover=buttonhover,
                            action=GameState.Play)

    Special_Text = Action_Counttxt(pos=(WIDTH - 975, 625),
                            font_size=25,
                            txt_col=BLACK,
                            bg_col=buttoncolor,
                            text="",
                            bg_hover=buttonhover,
                            action=GameState.Play)

    Bone_Pile = BoneP(pos=(WIDTH - 1075, 700),
                            font_size=50,
                            txt_col=BLACK,
                            bg_col=buttoncolor,
                            text="Bone Pile",
                            bg_hover=buttonhover,
                            action=GameState.Play)

    buttons = [Delegate_Button, End_Turn_Button, Recall_Button,
               Action_Counter, Current_turn, Bone_Pile, Command_Move_Button, Special_Text]

    current_square = None
    global action_count
    global turn
    global delegation_mode
    global recall_mode
    global commander
    global blue_commander
    global red_commander
    global commMoveMode
    knight_special_turn = False
    human_team = [Team.GREEN, Team.BLUE, Team.PURPLE]
    CAPTURE_TABLE_SIZE = (600, 340)
    captureTableImage = pygame.image.load('./Images/Capture Table.PNG')
    #ai = AI
    action_count = findActionCount(player_commanders)

    while True:
        mouse_down = False
        pygame.mouse.get_pressed()
        # print('Delegation: ', Delegate_Button.selected)
        # print('Delegation remain selected: ', Delegate_Button.remain_selected)
        # print('Delegation Mode: ', delegation_mode)
        # print('action count', action_count)
        Action_Counter.text = 'Action Count: ' + str(action_count)

        if turn:
            # print('human turn')
            # print('enter pygame events')

            if(recall_mode):
                Special_Text.text = "Select Piece"

            elif(delegation_mode):
                Special_Text.text = "Select Piece then Commander"

            elif not (delegation_mode or recall_mode):
                Special_Text.text = ""

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
                    # if you don't click on the game board
                    if x >= GAME_WIDTH or y >= GAME_WIDTH:
                        if End_Turn_Button.selected:
                            delegation_mode = False
                            recall_mode = False
                            commMoveMode = False

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

                        if delegation_mode and human_piece_delegated is not True and checkCommanderTurn(Team.BLUE):
                                result = delegate(chosen_square)
                                if result is not None:
                                    player_delegated_pieces.append(result)

                        elif delegation_mode and chosen_square.piece is None:
                            delegation_mode = False

                        elif recall_mode and human_piece_delegated is not True and checkCommanderTurn(Team.BLUE):
                            recall(chosen_square)
                            Special_Text.text = ""

                        elif recall_mode and chosen_square.piece is None:
                            recall_mode = False

                        #Defines the free movement the commander can make without expending its corp turn
                        #This only occurs if the button is pressed
                        else:
                            # if chosen_square.piece.team in human_team:
                            # conditions for selected_square
                            if current_square is None:
                                if chosen_square.piece is None:
                                    remove_highlights()
                                    pass

                                elif commMoveMode:
                                    if (commAuth(chosen_square)):
                                        current_square = chosen_square
                                        commMove(chosen_square)
                                    else:
                                        commMoveMode = False

                                elif (checkCommanderTurn(chosen_square.piece.team) or chosen_square.piece.type is Type.KNIGHT) and (chosen_square.piece.team not in enemies[Team.BLUE]):
                                    if chosen_square.piece.type is Type.KNIGHT:
                                        # deals with knight' s attack pieces after move
                                        if knight_special_turn and adjacent_enemies((chosen_square.row, chosen_square.col), chosen_square.piece.team):
                                            if(chosen_square.piece.team is Team.BLUE):
                                                if(blue_commander.has_moved):
                                                    current_square = chosen_square
                                                    knightAttack(chosen_square)
                                                else:
                                                    current_square = chosen_square
                                                    potential_piece_moves(chosen_square)
                                            elif(chosen_square.piece.team is Team.GREEN):
                                                if(green_commander.has_moved):
                                                    current_square = chosen_square
                                                    knightAttack(chosen_square)
                                                else:
                                                    current_square = chosen_square
                                                    potential_piece_moves(chosen_square)
                                            elif(chosen_square.piece.team is Team.PURPLE):
                                                if(purple_commander.has_moved):
                                                    current_square = chosen_square
                                                    knightAttack(chosen_square)
                                                else:
                                                    current_square = chosen_square
                                                    potential_piece_moves(chosen_square)

                                        elif knight_special_turn and not adjacent_enemies((chosen_square.row, chosen_square.col), chosen_square.piece.team):
                                            current_square = chosen_square
                                            potential_piece_moves(chosen_square)

                                        elif not knight_special_turn and checkCommanderTurn(chosen_square.piece.team):
                                            current_square = chosen_square
                                            potential_piece_moves(chosen_square)
                                    elif not knight_special_turn or chosen_square.piece.type is not Type.KNIGHT:
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
                                if (checkCommanderTurn(current_square.piece.team) or current_square.piece.type is Type.KNIGHT or commMoveMode) and (current_square.piece.team not in enemies[Team.BLUE]):
                                    if (chosen_square.color is WHITE) or (
                                            chosen_square.color is GREY):  # lets you unselect current piece
                                        remove_highlights()
                                        current_square = None
                                        if commMoveMode:
                                            commMoveMode = False
#knight attacks, upddate here then do normal attacks.
                                    elif knight_special_turn and current_square.piece.type is Type.KNIGHT and adjacent_enemies((current_square.row, current_square.col), current_square.piece.team):
                                        if chosen_square.color is BLACK:
                                            if attack(screen, current_square.piece,
                                                      chosen_square.piece, checkCommanderHasMoved(current_square.piece.team)) is True:
                                                if chosen_square.piece.type is Type.BISHOP:
                                                    removeCommander(chosen_square.piece.team)
                                                    #changes color of all pieces in commander.troops to red
                                                    #adds pieces to red commander troop array
                                                    #removed pieces from original commander array
                                                    #changes sprite color
                                                    remove_team(chosen_square.piece.team)
                                                elif (chosen_square.piece.type is Type.KING) and \
                                                        (chosen_square.piece.team is Team.RED):
                                                    return GameState.Win
                                                else:
                                                    remove_piece(chosen_square.piece)
                                                ai_captured_pieces.append(chosen_square.piece)
                                                # Recoloring must be done after remove piece or that function gets killed
                                                chosen_square.piece.team = Team.RED
                                                ReturnPieceSprite(chosen_square.piece)
                                                end_commander_turn(current_square.piece.team)



                                                chosen_square.piece = None
                                                move_piece(current_square, chosen_square)
                                                current_square = None
                                                action_count -= 1
                                                remove_highlights()
                                                knight_special_turn = False
                                                if (chosen_square.piece.team is Team.BLUE):
                                                    blue_commander.has_moved = False
                                                elif (chosen_square.piece.team is Team.GREEN):
                                                    green_commander.has_moved = False
                                                elif (chosen_square.piece.team is Team.PURPLE):
                                                    purple_commander.has_moved = False
                                            else:
                                                end_commander_turn(current_square.piece.team)
                                                remove_highlights()
                                                action_count -= 1
                                                if (current_square.piece.team is Team.BLUE):
                                                    blue_commander.has_moved = False
                                                elif (current_square.piece.team is Team.GREEN):
                                                    green_commander.has_moved = False
                                                elif (current_square.piece.team is Team.PURPLE):
                                                    purple_commander.has_moved = False
                                                knight_special_turn = False

                                        elif chosen_square.color is BLUE:
                                            action_count -= 1
                                            end_commander_turn(current_square.piece.team)
                                            move_piece(current_square, chosen_square)
                                            remove_highlights()
                                            current_square = None



                                    elif (chosen_square.color is BLUE) and \
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

                                        if not knight_special_turn and not commMoveMode:
                                            end_commander_turn(current_square.piece.team)
                                            action_count -= 1

                                        #Extra check so that the user can choose to not attack with the Knight and make another action
                                        #that affects the turn count
                                        elif knight_special_turn and not commMoveMode and current_square.piece.type != Type.KNIGHT:
                                            end_commander_turn(current_square.piece.team)
                                            action_count -= 1

                                        #We only end turn and reduce action count if we aren't performing a commander move.
                                        #If we are, then we can ignore the above and just set the commander's authority to false
                                        if (commMoveMode):
                                            commMoveMode = False
                                            if current_square.piece.team is Team.BLUE:
                                                blue_commander.authority = False
                                            elif current_square.piece.team is Team.GREEN:
                                                green_commander.authority = False
                                            elif current_square.piece.team is Team.PURPLE:
                                                purple_commander.authority = False
                                        move_piece(current_square, chosen_square)
                                        remove_highlights()
                                        current_square = None

                                    elif (chosen_square.color is BLACK):
                                        if attack(screen, current_square.piece,
                                                  chosen_square.piece) is True:
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
                                            else:
                                                remove_piece(chosen_square.piece)
                                            #append to captured pieces
                                            ai_captured_pieces.append(chosen_square.piece)
                                            #remove from commander array
                                            #Recoloring must be done after remove piece or that function gets killed
                                            chosen_square.piece.team = Team.RED
                                            ReturnPieceSprite(chosen_square.piece)
                                            end_commander_turn(chosen_square.piece.team)
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
            if(board[1][2].piece is not None) and (board[1][2].piece.type == Type.PAWN):
                '''
            ) and (board[1][6] is not None and board[1][6].piece.type == Type.PAWN)\
                    and (board[1][2] is not None and board[0][3].piece.type == Type.QUEEN):
                '''
                move_piece(board[1][2], board[2][2])
                move_piece(board[1][6], board[2][6])
                move_piece(board[0][3], board[2][3])
                for c in ai_commanders:
                    c.action = False
                action_count = 0

            for c in ai_commanders:
                update_display(screen)
                pygame.display.flip()
                if c.action is not False:

                    moves = []
                    pieces = []
                    #copied_board = copy_board(board)
                    #temp = search(c, -inf, inf, True, 3, copied_board)
                    temp = greedy_search(c)

                    if temp.piece is None:
                        while temp.piece is None:
                            temp = generateRandomMove(c)

                    moves.append(temp)
                    chosen_piece = temp.piece  # acceses piece attribute of move object from temp
                    pieces.append(chosen_piece)
                    pieceSq = temp.start_position  # records starting square of piece
                    team = chosen_piece.team
                    chosen_move = moves[0]
                    finalMove = chosen_move.end_position


                    print("Piece: " + str(temp.piece.type) + "\n" +
                          "Start position: " + str(temp.start_position) + "\n" +
                          "End position: " + str(temp.end_position) + "\n" +
                          "Team: " + str(temp.piece.team) + "\n" +
                          "eval value: " + str(evaluation(temp.piece,temp.start_position ,temp.end_position, board)) + "\n")

                    highlight_move(finalMove, team)
                    #general movement
                    if (board[finalMove[0]][finalMove[1]].color is BLUE):
                        board[pieceSq[0]][pieceSq[1]].piece.pos = [finalMove[0], finalMove[1]]
                        tempSquare = board[pieceSq[0]][pieceSq[1]]
                        finalSquare = board[finalMove[0]][finalMove[1]]
                        move_piece(tempSquare, finalSquare)
                        action_count -= 1
                        end_commander_turn(team)
                        remove_highlights()

                        #attacking for knight
                        if (finalSquare.piece.type is Type.KNIGHT):
                            if adjacent_enemies((finalSquare.row, finalSquare.col), finalSquare.piece.team):
                                knightAttacks = knightAttackPieces((finalSquare.row, finalSquare.col),
                                                                   (finalSquare.row, finalSquare.col))

                                chosenAttack = None
                                maxScore = -inf
                                for move in knightAttacks:
                                    score = evaluation(chosen_piece,pieceSq ,move, board)
                                    if score > maxScore:
                                        chosenAttack = move
                                        maxScore = score

                                attackSquare = board[chosenAttack[0]][chosenAttack[1]]
                                knightAttack(finalSquare)
                                if attack(screen, finalSquare.piece, attackSquare.piece, True):
                                    if attackSquare.piece.type is Type.BISHOP:
                                        # We decrement the counter to ensure the actions done by a human are limited based on the number of commanders we have
                                        removeCommander(attackSquare.piece.team)
                                        remove_team(attackSquare.piece.team)
                                    elif (attackSquare.piece.type is Type.KING) and (
                                            attackSquare.piece.team is Team.BLUE):
                                        return GameState.Loss
                                    else:
                                        print(attackSquare.piece, 'removed by: ' ,finalSquare.piece.type)
                                        remove_piece(attackSquare.piece)
                                    # append to captured pieces
                                    player_captured_pieces.append(attackSquare.piece)
                                    # remove from commander array
                                    # Recoloring must be done after remove piece or that function gets killed
                                    attackSquare.piece.team = Team.BLUE
                                    ReturnPieceSprite(attackSquare.piece)
                                    end_commander_turn(attackSquare.piece.team)
                                    finalSquare.piece.pos = [attackSquare.row, attackSquare.col]
                                    move_piece(finalSquare, attackSquare)
                                    board[finalMove[0]][finalMove[1]].piece = None
                                    remove_highlights()
                                else:
                                    remove_highlights()
                    #attacking for non knight pieces
                    elif (board[finalMove[0]][finalMove[1]].color is BLACK):
                        if(attack(screen, board[pieceSq[0]][pieceSq[1]].piece,
                                   board[finalMove[0]][finalMove[1]].piece)):
                            if board[finalMove[0]][finalMove[1]].piece.type is Type.BISHOP:
                                # We decrement the counter to ensure the actions done by a human are limited based on the number of commanders we have
                                removeCommander(board[finalMove[0]][finalMove[1]].piece.team)
                                remove_team(board[finalMove[0]][finalMove[1]].piece.team)
                            elif (board[finalMove[0]][finalMove[1]].piece.type is Type.KING) and (
                                    board[finalMove[0]][finalMove[1]].piece.team is Team.BLUE):
                                return GameState.Loss
                            else:
                                remove_piece(board[finalMove[0]][finalMove[1]].piece)
                            # append to captured pieces
                            player_captured_pieces.append(board[finalMove[0]][finalMove[1]].piece)
                            # remove from commander array
                            # Recoloring must be done after remove piece or that function gets killed
                            board[finalMove[0]][finalMove[1]].piece.team = Team.BLUE
                            ReturnPieceSprite(board[finalMove[0]][finalMove[1]].piece)
                            end_commander_turn(board[finalMove[0]][finalMove[1]].piece.team)
                            board[finalMove[0]][finalMove[1]].piece = None
                            if (board[pieceSq[0]][pieceSq[1]].piece.type is not Type.ROOK):
                                board[pieceSq[0]][pieceSq[1]].piece.pos = [finalMove[0], finalMove[1]]
                                move_piece(board[pieceSq[0]][pieceSq[1]], board[finalMove[0]][finalMove[1]])
                                end_commander_turn(board[finalMove[0]][finalMove[1]].piece.team)
                            else:
                                end_commander_turn(board[pieceSq[0]][pieceSq[1]].piece.team)
                            action_count -= 1
                            remove_highlights()
                        else:
                            end_commander_turn(board[pieceSq[0]][pieceSq[1]].piece.team)
                            action_count -= 1
                            current_square = None
                            remove_highlights()
                else:
                    action_count -= 1
                    remove_highlights()
            if action_count <= 0:
                turnChange()
                reset_turn()

            remove_highlights()
            update_display(screen)




        #return GameState.AiPlay

        update_display(screen)
        insertBonepile()
        screen.blit(pygame.transform.scale(captureTableImage, CAPTURE_TABLE_SIZE), (WIDTH * .5, HEIGHT * .665)) # (change this)
        for b in buttons:
            ui_action = b.moused_over(pygame.mouse.get_pos(), mouse_down)
            if ui_action is not None:
                # if b == Delegate_Button:

                return ui_action
            b.draw(screen)
        pygame.display.flip()
        clock.tick(15)

        #OLD RANDOM AI
        """if c.action is not False:
                            for troop in c.troops:
                                if troop.type is Type.PAWN:
                                    pawn_moves = pawn_moves_top(troop.pos)
                                    if pawn_moves is not None:
                                        moves.append(pawn_moves)
                                        pieces.append(troop.pos)
                                elif troop.type is Type.KING or Type.QUEEN:
                                    kqmoves = maxMovement(3, 0, troop.pos, troop.pos, troop.type.value)
                                    if kqmoves is not None:
                                        moves.append(kqmoves)
                                        pieces.append(troop.pos)
                                elif troop.type is Type.KNIGHT:
                                    kmoves = maxMovement(4, 0, troop.pos, troop.pos, troop.type.value)
                                    if kmoves is not None:
                                        moves.append(kmoves)
                                        pieces.append(troop.pos)
                                elif troop.type is Type.BISHOP:
                                    bmoves = maxMovement(2, 0, troop.pos, troop.pos, troop.type.value)
                                    if bmoves is not None:
                                        moves.append(bmoves)
                                        pieces.append(troop.pos)
                                elif troop.type is Type.ROOK:
                                    rmoves = maxMovement(2, 0, troop.pos, troop.pos, troop.type.value)
                                    if rmoves is not None:
                                        moves.append(rmoves)
                                        pieces.append(troop.pos)

                            chosen_piece = 0
                            while True:
                                chosen_piece = random.randint(0, len(pieces) - 1)
                                if (len(moves[chosen_piece]) > 0):
                                    break
                            pieceSq = pieces[chosen_piece]
                            print(pieces[chosen_piece])
                            team = board[pieceSq[0]][pieceSq[1]].piece.team
                            chosen_move = moves[chosen_piece]
                            for move in chosen_move:
                                print(move)
                            update_display(screen)
                            highlight_moves(chosen_move, team)
                            update_display(screen)
                            finalMove = chosen_move[random.randint(0, len(chosen_move) - 1)]
                            if(board[finalMove[0]][finalMove[1]].color is BLUE):
                                board[pieceSq[0]][pieceSq[1]].piece.pos = [finalMove[0], finalMove[1]]
                                tempSquare = board[pieceSq[0]][pieceSq[1]]
                                finalSquare = board[finalMove[0]][finalMove[1]]
                                move_piece(tempSquare, finalSquare)
                                action_count -= 1
                                end_commander_turn(team)
                                remove_highlights()
                                if(finalSquare.piece.type is Type.KNIGHT):
                                    if adjacent_enemies((finalSquare.row, finalSquare.col), finalSquare.piece.team):
                                        knightAttacks = knightAttackPieces((finalSquare.row, finalSquare.col), (finalSquare.row, finalSquare.col))
                                        if(len(knightAttacks) == 0):
                                            break
                                        chosenAttack = knightAttacks[random.randint(0, len(knightAttacks) - 1)]
                                        attackSquare = board[chosenAttack[0]][chosenAttack[1]]
                                        knightAttack(finalSquare)
                                        if attack(screen, finalSquare.piece.type.value, attackSquare.piece.type.value, True):
                                            if attackSquare.piece.type is Type.BISHOP:
                                                # We decrement the counter to ensure the actions done by a human are limited based on the number of commanders we have
                                                removeCommander(attackSquare.piece.team)
                                                remove_team(attackSquare.piece.team)
                                            elif (attackSquare.piece.type is Type.KING) and (
                                                    attackSquare.piece.team is Team.BLUE):
                                                return GameState.Loss
                                            else:
                                                remove_piece(attackSquare.piece)
                                            # append to captured pieces
                                            player_captured_pieces.append(attackSquare.piece)
                                            # remove from commander array
                                            # Recoloring must be done after remove piece or that function gets killed
                                            attackSquare.piece.team = Team.BLUE
                                            ReturnPieceSprite(attackSquare.piece)
                                            end_commander_turn(attackSquare.piece.team)

                                            finalSquare.piece.pos = [attackSquare.row, attackSquare.col]
                                            move_piece(finalSquare, attackSquare)
                                            remove_highlights()
                                        else:
                                            remove_highlights()

                            elif(board[finalMove[0]][finalMove[1]].color is BLACK):
                                if(attack(screen, board[pieceSq[0]][pieceSq[1]].piece.type.value, board[finalMove[0]][finalMove[1]].piece.type.value)):
                                    if board[finalMove[0]][finalMove[1]].piece.type is Type.BISHOP:
                                        # We decrement the counter to ensure the actions done by a human are limited based on the number of commanders we have
                                        removeCommander(board[finalMove[0]][finalMove[1]].piece.team)
                                        remove_team(board[finalMove[0]][finalMove[1]].piece.team)
                                    elif (board[finalMove[0]][finalMove[1]].piece.type is Type.KING) and (
                                            board[finalMove[0]][finalMove[1]].piece.team is Team.BLUE):
                                        return GameState.Loss
                                    else:
                                        remove_piece(board[finalMove[0]][finalMove[1]].piece)
                                    # append to captured pieces
                                    player_captured_pieces.append(board[finalMove[0]][finalMove[1]].piece)
                                    # remove from commander array
                                    # Recoloring must be done after remove piece or that function gets killed
                                    board[finalMove[0]][finalMove[1]].piece.team = Team.BLUE
                                    ReturnPieceSprite(board[finalMove[0]][finalMove[1]].piece)
                                    end_commander_turn(board[finalMove[0]][finalMove[1]].piece.team)

                                    if (board[pieceSq[0]][pieceSq[1]].piece.type is not Type.ROOK):
                                        board[pieceSq[0]][pieceSq[1]].piece.pos = [finalMove[0], finalMove[1]]
                                        move_piece(board[pieceSq[0]][pieceSq[1]], board[finalMove[0]][finalMove[1]])
                                        end_commander_turn(board[finalMove[0]][finalMove[1]].piece.team)
                                    else:
                                        end_commander_turn(board[pieceSq[0]][pieceSq[1]].piece.team)
                                    action_count -= 1
                                    remove_highlights()
                                else:
                                    end_commander_turn(board[pieceSq[0]][pieceSq[1]].piece.team)
                                    action_count -= 1
                                    current_square = None
                                    remove_highlights()
                    if action_count <= 0:
                        turnChange()
                        reset_turn()"""