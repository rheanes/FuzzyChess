from board import *
from pieces import *
import random
#Team, Type, orange_commander, red_commander, yellow_commander

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

class AI:
    def __init__(self):
        pass
    """
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
    """

    def decision(self):
        row, col = (random.randint(0, 8), random.randint(0, 8))
        #captured_commander = check_commanders()
        for commander in ai_commanders:
            commander.make_decision(board[row][col])

