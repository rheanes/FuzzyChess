from common import *
#from GameFunctions import *
from GameScene import *
import random
from copy import deepcopy
#Team, Type, orange_commander, red_commander, yellow_commander

'''
# for ai, scans entire board for enemies
def board_scan(targets, leader, board):
    for square in board:
        # scan enemies
        if square.piece is not None:
            if enemies[square.piece.team] is Team.RED or \
                    enemies[square.piece.team] is Team.ORANGE or \
                    enemies[square.piece.team] is Team.YELLOW:
                square[:].piece.pos = (square.row, square.col)
                targets.append(square[:].piece)

            if square.piece.team is leader.team:
                square[:].piece.pos = ()
    return targets
'''

"""
def find_troop_position(self, board):
    for square in board:
        if square.piece.team is self.leader.
"""

"""
how to define move/attack?
needs to check if an action is valid (maybe already defined?)
maybe encapsulate action as an object? (action class) -> 
stores piece that is doing action, position that it is moving to. Doing so allows for a list of moves to be stored

"""

copied_board = copy_board(board)

def assign_piece_pos():
    for row in range(8):
        for col in range(8):
            if board[row][col].piece is not None:
                board[row][col].piece.pos = (row, col)

class Move:
    def __init__(self, piece, start_position: tuple[int, int], end_position: tuple[int, int]) -> None:
        self.piece = piece
        self.start_position = start_position
        self.end_position = end_position
        pass

# for easy mode
class AiAction:
    def __init__(self, troop=None, decision=None, square=None, team=None):
        self.decision = decision
        self.troop = troop
        self.square = square
        self.team = team

# returns numerical evaluation of a particular position that a piece wishes to move to
def evaluation(piece, position, board):
    total_value = 0
    row, col = position[0], position[1]
    # reference piece table values based on piece type
    if (board[row][col].piece is None) or (board[row][col].piece in enemies[piece.team]):
        if piece.type == Type.PAWN:
            total_value += pawn_pos_table[row][col]
        elif piece.type == Type.ROOK:
            total_value += rook_pos_table[row][col]
        elif piece.type == Type.BISHOP:
            total_value += bishop_pos_table[row][col]
        elif piece.type == Type.KNIGHT:
            total_value += knight_pos_table[row][col]
        elif piece.type == Type.QUEEN:
            total_value += queen_pos_table[row][col]
        elif piece.type == Type.KING:
            total_value += king_pos_table[row][col]
    # if a particular position to move to has an enemy piece, add the enemy pieces' value to the evaluation times the chance of successful capture
    if (board[row][col].piece is not None) and (board[row][col].piece.team in enemies[piece.team]):
        enemy = board[row][col].piece
        if piece.type == Type.PAWN:
            total_value += (enemy.value * pawn_atk_chnc[enemy.type])
        elif piece.type == Type.KING:
            total_value += (enemy.value * king_atk_chnc[enemy.type])
        elif piece.type == Type.QUEEN:
            total_value += (enemy.value * queen_atk_chnc[enemy.type])
        elif piece.type == Type.BISHOP:
            total_value += (enemy.value * bishop_atk_chnc[enemy.type])
        elif piece.type == Type.KNIGHT:
            total_value += (enemy.value * knight_atk_chnc[enemy.type])
        elif piece.type == Type.ROOK:
            total_value += (enemy.value * rook_atk_chnc[enemy.type])
    return total_value


"""
Alpha beta search needs to acquire all possible moves from current board state for the ai side
needs to do same process for enemy side during minimizing step(board_scan might be able to get a 
list of enemy pieces)

We can consider each board state as a node and the opposing player's responses to that move to be the 
children of our move. We then repeat the process until we reach max depth of the search.

how do we represent board state as a node?
1. Encapsulate each move as an object storing the piece to move and the coordinates it is moving to
2. have a backend representation of the board and moving pieces on that board, and then matching 
that move on the board when the best move is found.

need to generate list of moves
"""
def available_moves(piece):
    if (piece.team == Team.YELLOW or (piece.team == Team.RED) or piece.team == Team.ORANGE):
        if piece.type == Type.PAWN:
            return pawn_moves_top(piece.pos, piece.team)
        elif (piece.type == Type.KING) or (piece.type == Type.QUEEN):
            return maxMovement(3, 0, piece.pos, piece.pos, piece.type.value, piece.team)
        elif piece.type == Type.ROOK:
            return maxMovement(2, 0, piece.pos, piece.pos, piece.type.value, piece.team)
        elif piece.type == Type.BISHOP:
            return maxMovement(2, 0, piece.pos, piece.pos, piece.type.value, piece.team)
        elif piece.type == Type.KNIGHT:
            return maxMovement(4, 0, piece.pos, piece.pos, piece.type.value, piece.team)
    

def generate_moves(comm):
    moves = []
    for troop in comm.troops:
        for row, col in available_moves(troop):
            moves.append(Move(troop, troop.pos, (row, col)))
        
    return moves

def copy_board(board):
    return deepcopy(board)

copied_board = copy_board(board)

def move_copy_piece(curr_pos: Square, new_pos: Square):
    copied_board[new_pos.row][new_pos.col].piece = copied_board[curr_pos.row][curr_pos.col].piece
    copied_board[curr_pos.row][curr_pos.col].piece = None




    

"""
moves = [[piece, (row, col)]]
generating enemy moves -> access enemy commanders troops
call potential_piece_moves and store possible moves from that function
[green_commander.troops[0]] , (row, col)]
"""
# alpha-beta search
def search(comm, alpha, beta, maxPlayer, depth, board):
    # returns static evaluation of best move found
    score = 0
    if depth == 0:
        score = evaluation(best_move.piece, best_move.end_position, board)
        return best_move ,score
    best_move = None


    # if it is the maximizing player(ai)
    if maxPlayer:
        max_score = -inf
        moves = []
        for c in ai_commanders:
            moves.extend(generate_moves(c))
        # search through all moves available for that corp
        for m in moves:
            move_copy_piece(m.start_position, m.end_position)
            curr_score = search(c, alpha, beta, False, depth - 1, board) * -1

            # if the current move is better than the current highest score, replace it
            if curr_score > max_score:
                max_score = curr_score
                best_move = moves[m]

            # if the highest score is higher than beta, break out of the loop and return the value at that position?
            if max_score >= beta:
                break
            alpha = max(alpha, max_score)
        return best_move, max_score
    else:
        # inverse process for opposing(human) player
        min_score = inf
        moves = []
        for c in player_commanders:
            moves.extend(generate_moves(c))
        for m in moves:
            curr_score = search(c, alpha, beta, True, depth - 1, board)

            if curr_score < min_score:
                min_score = curr_score
                best_move = moves[m]

            if min_score <= alpha:
                break
            beta = min(beta, min_score)
        return min_score


###############################################
# Modes: Easy, Medium, and Hard
###############################################
'''
@base strategy: commanders should be in close proximity of troops, however king should have queen be in proximity

def base_strategy(self):
    pass

'''

'''
def find_potential_piece_moves(self):
    for row in range(8):
        for col in range(8):
            if board[row][col].color is BLUE or \
                board[row][col].color is BLACK:
'''

# for ai, scans entire board for enemies
def board_scan_moves(piece):
    targets = []

    for square in board:
        # scan enemies
        '''
        if square is not None:
        if enemies[square.piece.team] is Team.RED or \
            enemies[square.piece.team] is Team.ORANGE or \
                enemies[square.piece.team] is Team.YELLOW:
            square[:].piece.pos = (square.row, square.col)
            targets.append(square[:].piece)

        if square.piece.team is self.leader.team:
            square[:].piece.pos = ()
        '''
        if square[:].color is BLUE:
            targets.append(AiAction(piece, Action.MOVE, (square.row, square.col)))

    return targets

def board_scan_attacks(piece):
    targets = []

    for square in board:
        # scan enemies
        '''
        if square is not None:
        if enemies[square.piece.team] is Team.RED or \
            enemies[square.piece.team] is Team.ORANGE or \
                enemies[square.piece.team] is Team.YELLOW:
            square[:].piece.pos = (square.row, square.col)
            targets.append(square[:].piece)

        if square.piece.team is self.leader.team:
            square[:].piece.pos = ()
        '''
        if square[:].color is BLACK:
            targets.append(AiAction(piece ,Action.ATTACK, (square.row, square.col)))

    return targets

'''
@strategy: 
    Order of move:
        1) Pawns
        2) Knight
        3) Bishop
     
'''
def easy_mode(comm): # troop will either move or attack
    # adds lead to action scene in desperation
    #if len(comm.troops) < 2:
     #   comm.leader.troops.append(comm.leader)

    
    #assign_piece_pos
    ####################################
    # Scan each troop for nearby enemies or moves
    ####################################
    troop_actions = []
    #bishop_actions = []
    for troop in comm.troops:
        
        potential_piece_moves(board[troop.pos[0]][troop.pos[1]])
        troop_actions.extend(board_scan_attacks(troop))
        troop_actions.extend(board_scan_moves(troop))
        


    ##############################
    # Get troop's actions
    ##############################
    potential_piece_moves(board[troop.pos[0]][troop.pos[1]])

    troop_moves = []

    troop_actions = []

    if comm.leader.type is Type.KING:
        if not troop.delegated:
            troop_actions.append(Action.DELEGATE)
        else:
            troop_actions.append(Action.RECALL)

    ##############################
    # Get troop's squares
    ##############################
    if comm.knight_special_move:
        knightAttack(Square(troop))
        troop_moves = [Action.ATTACK]

        for row in range(8):
            for col in range(8):
                if board[row][col].color is BLACK:
                    troop_moves.append(AiAction(Action.ATTACK, board[row][col]))
                    troop_moves.append(Action.ATTACK)
    else:
        for row in range(8):
            for col in range(8):
                if board[row][col].color is BLUE:
                    if troop.type is Type.KNIGHT and adjacent_enemies(troop.pos, troop.team) and \
                            not comm.knight_special_move:
                        comm.knight_special_move = True

                    # global decision
                    # decision = Action.MOVE
                    troop_moves.append(AiAction(Action.MOVE, board[row][col]))
                    troop_actions.append(Action.MOVE)
                elif board[row][col].color is BLACK:
                    troop_moves.append(AiAction(Action.ATTACK, board[row][col]))
                    troop_actions.append(Action.ATTACK)

    ################################
    # Randomly choose troop's action
    ################################
    # randomly choose action
    if len(troop_actions) == 1:
        decision = troop_actions[0]
    else: decision = random.choice(troop_actions)

    team = None

    # if decision is Delegation
    if decision is Action.DELEGATE:
        if comm is orange_commander and ok not in orange_commander.troops:
            team = Team.ORANGE
        elif comm is yellow_commander and yk not in yellow_commander.troops:
            team = Team.YELLOW

    remove_highlights()

    # randomly choose square
    if len(troop_moves):
        next_square = random.choice(troop_moves)

    return decision, troop, next_square, team


'''
@strategy: 
    bishop: randomly choose which troop will move or attack based on evaluation of present (use evaluation matrix)
    king: randomly choose which troop will move, attack, delegated, or recalled based on evaluation of present
'''
'''
def medium_mode(comm):
    troop = None
    next_square = None

    for troop in comm.troops:
        for pos in positions:
            self.targets.append(troop[:].detect_targets(board, (pos[0], pos[1]), board[pos[0]][pos[1]].piece.team))

    # get all enemies
    self.targets.append(self.board_scan(board))

    return troop, next_square
'''
'''
@strategy: 
    bishop: randomly choose which troop will move or attack based on evaluation of present and future (probabilities)
    king: randomly choose which troop will move, attack, delegated, or recalled based on evaluation of present and future
'''

pawns = [False, False, False]

def hard_mode(comm):
    # append leader to troop when half lost
    if len(comm.troops) < 2:
        comm.troops.append(comm.leader)

    ai_action = AiAction()

    # Pawn's Action
    for troop in comm.troops:
        global pawns
        if troop.type is Type.PAWN:
            potential_piece_moves(Square(troop))


    # Knight's Action
    for troop in comm.troops:
        if troop.type is Type.

    potential_piece_moves()
    # Bishop's Action



    return ai_action


def make_decision(comm, mode=DecisionMode.EASY):
    # get remaining troops
    comm.troops = list(set(comm.troops) - set(player_captured_pieces))

    troop = None
    next_square = tuple()
    # choose decision mode
    if mode is DecisionMode.EASY:
        troop, next_square = easy_mode(comm)
    elif mode is DecisionMode.MEDIUM:
        troop, next_square = medium_mode(comm)
    elif mode is DecisionMode.HARD:
        troop, next_square = hard_mode(comm)
    #elif mode is DecisionMode.EXTRA_HARD:
    #    troop, next_square = extra_hard_mode()

    return troop, next_square


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

    def set_piece_pos(self):
        for row in range(8):
            for col in range(8):
                board[row][col].piece.pos(row, col)

    def decision(self, commander, mode=DecisionMode.EASY):
        # row, col = (random.randint(0, 8), random.randint(0, 8))
        # captured_commander = check_commanders()
        for commander in ai_commanders:
            self.set_piece_pos()
            chosen_square, pos = commander.make_decision(board, mode)
            potential_piece_moves(chosen_square)
            for square in board:
                if square.color is BLACK and \
                        square[:].piece.team is enemies[square.piece.team]:
                    chosen_row, chosen_col = chosen_square.row, chosen_square.col
                    if attackMatrix(board[pos[0]][pos[1]].piece.type, board[chosen_row][chosen_col]):
                        # temp = board[chosen_row][chosen_col]
                        board[chosen_row][chosen_col].piece = board[pos[0]][pos[1]].piece
                        remove_highlights()
                        return
