import pygame
import sys
from common import *
from board import *
import random
from guielements import *

attackMatrix = [[4, 4, 4, 4, 5, 0],
                [4, 4, 4, 4, 5, 2],
                [5, 5, 4, 5, 5, 3],
                [5, 5, 5, 5, 5, 2],
                [4, 4, 5, 4, 5, 5],
                [6, 6, 5, 6, 6, 4]]



def string_color(team):
    if team == team.BLUE:
        return 'Blue'
    if team == team.GREEN:
        return 'Green'
    if team == team.PURPLE:
        return 'Purple'
    if team == team.RED:
        return 'Red'
    if team == team.ORANGE:
        return 'Orange'
    if team == team.YELLOW:
        return 'Yellow'

def piece_type(type):
    if type == Type.PAWN:
        return 'pawn'
    if type == Type.ROOK:
        return 'rook'
    if type == Type.KNIGHT:
        return 'knight'
    if type == Type.QUEEN:
        return 'queen'
    if type == Type.BISHOP:
        return 'bishop'
    if type == Type.KING:
        return 'king'

# ------------------------------ACTUAL DICE ROLL --------------------- #
def attackAnimation(screen, atk, deff, roll):
    dieImage1 = pygame.image.load('./Images/dieFace1.png')
    dieImage2 = pygame.image.load('./Images/dieFace2.png')
    dieImage3 = pygame.image.load('./Images/dieFace3.png')
    dieImage4 = pygame.image.load('./Images/dieFace4.png')
    dieImage5 = pygame.image.load('./Images/dieFace5.png')
    dieImage6 = pygame.image.load('./Images/dieFace6.png')
    dieImages = [dieImage1, dieImage2, dieImage3, dieImage4, dieImage5, dieImage6]
    cycles = 3
    dieImage = dieImages[roll - 1]
    #orange knight attacking blue king
    atk_piece =  str(string_color(atk.team))+ ' ' + str(piece_type(atk.type))
    def_piece =  str(string_color(deff.team)) +' '+ str(piece_type(deff.type))
    print(atk_piece, 'attacking', def_piece)
    Top_Text = font.render(atk_piece, True, BACKGROUND)
    Middle_Text = font.render('attacking', True, BACKGROUND)
    Botttom_Text = font.render(def_piece, True, BACKGROUND)
    while True:
        mouse_down = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_down = True
            elif event.type == pygame.QUIT:
                pygame.quit()
                exit()
        okButton = button(pos=(875, 500),
                         font_size=65,
                         txt_col=BLACK,
                         bg_col=buttoncolor,
                         text="ok",
                         bg_hover=buttonhover,
                         action=GameState.Play)

        pygame.draw.rect(screen, BLACK, pygame.Rect(675, 175, 400, 400))
        screen.blit(Top_Text, (700, 175))
        screen.blit(Middle_Text,(700, 225))
        screen.blit(Botttom_Text, (700, 275))
        while cycles > 0:
            for i in dieImages:
                screen.blit(i, (825, 365))
                pygame.display.flip()
                pygame.time.delay(100)
            cycles = cycles - 1
        screen.blit(dieImage, (825, 365))
        ui_action = okButton.moused_over(pygame.mouse.get_pos(), mouse_down)
        if ui_action is not None:
            return ui_action
        okButton.draw(screen)

        pygame.display.flip()

def attackRoll(screen, atk, deff):
    minRoll = 1
    maxRoll = 6
    roll = random.randint(minRoll, maxRoll)
    attackAnimation(screen, atk, deff, roll)
    return roll


# Attack action. This is called whenever a piece wants to claim another piece.
# It takes the values of the attacker and defender, and references the attackMatrix
# for it's given roll. If it rolls at least the number in that matrix, then the piece
# should claim it. Thus we return true. If we don't, then we return false. We have
# an optional parameter (hasMoved) as well in the event a knight is the attacker.
# The knight tells the attack function it has moved, and gets a bonus to its move.

def attack(screen, atk, deff, hasMoved: bool = False) -> bool:
    #atk and deff are pieces passed in we need to have to actual pieces
    attacker = atk.type.value
    defender = deff.type.value
    num = attackRoll(screen, atk, deff)
    if hasMoved:
        if num + 1 >= attackMatrix[attacker][defender]:
            return True
        else:
            return False

    else:
        if num >= attackMatrix[attacker][defender]:
            return True
        else:
            return False
'''
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
'''

# Only called after a Knight moves. Is used to highlight enemies in the general area
def knightAttack(square: Square):
    highlight_moves(knightAttackPieces((square.row, square.col), (square.row, square.col)), square.piece.team)

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