from common import *
#from GameFunctions import *
#from GameScene import *
import random
from board import * 
from pieces import *
#Team, Type, orange_commander, red_commander, yellow_commander


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
'''
def enemy_material_count():
    count = 0

    for square in board:
        if square.piece.team
'''

# rewards ai for moving its pieces to squares that have adjacent allied pieces
def adjacent_allies(pos: tuple[int, int]):
    row, col = pos
    val = 0
    end_pos_list = [(row-1, col - 1), (row-1, col), (row-1,col+1),
                    (row, col-1), (row, col), (row,col+1),
                    (row+1, col-1), (row+1,col), (row+1, col+1)]

    for p in end_pos_list:
        if on_board(p):
            if board[p[0]][p[1]].piece is not None and board[p[0]][p[1]] in enemies[Team.BLUE]:
                val += 10

                p_type = board[p[0]][p[1]].piece.type

                # value based on value of piece
                if p_type is Type.KNIGHT:
                    val += 500
                elif p_type is Type.BISHOP:
                    val += 800
                elif p_type is Type.ROOK:
                    val += 200
                elif p_type is Type.PAWN:
                    val += 50

    return val
'''
    Evaluation:
        
'''


# returns numerical evaluation of a particular position that a piece wishes to move to
def evaluation(piece,start_position, end_position, board):
    total_value = 0
    currRow, currCol = start_position[0], start_position[1]
    row, col = end_position[0], end_position[1]
    total_value += adjacent_allies(end_position) - adjacent_allies(start_position)

    #highlight_move(end_position, piece.team)
    # reference piece table values based on piece type
    if (board[row][col].piece is None) or (board[row][col].piece in enemies[piece.team]):
        if piece.type == Type.PAWN:
            total_value += pawn_pos_table[row][col] - pawn_pos_table[currRow][currCol]
        elif piece.type == Type.ROOK:
            total_value += rook_pos_table[row][col] - rook_pos_table[currRow][currCol]
        elif piece.type == Type.BISHOP:
            total_value += bishop_pos_table[row][col] - bishop_pos_table[currRow][currCol]
        elif piece.type == Type.KNIGHT:
            total_value += knight_pos_table[row][col] - knight_pos_table[currRow][currCol]
        elif piece.type == Type.QUEEN:
            total_value += queen_pos_table[row][col] - queen_pos_table[currRow][currCol]
        elif piece.type == Type.KING:
            total_value += king_pos_table[row][col] - rook_pos_table[currRow][currCol]
    
    # if a particular position to move to has an enemy piece, add the enemy pieces' value to the evaluation times the chance of successful capture
    if (board[row][col].piece is not None) and (board[row][col].piece.team in enemies[piece.team]):
        enemy = board[row][col].piece
        if piece.type == Type.PAWN:
            print('I see a pawn')
            total_value += (enemy.value.value * pawn_atk_chnc[enemy.type])
        elif piece.type == Type.KING:
            print('I see a king')
            total_value += (enemy.value.value * king_atk_chnc[enemy.type])
        elif piece.type == Type.QUEEN:
            print('I see the queen')
            total_value += (enemy.value.value * queen_atk_chnc[enemy.type])
        elif piece.type == Type.BISHOP:
            print('i see a bishop')
            total_value += (enemy.value.value * bishop_atk_chnc[enemy.type]) 
        elif piece.type == Type.KNIGHT:
            print('I see a knight')
            total_value += (enemy.value.value * knight_atk_chnc[enemy.type])
        elif piece.type == Type.ROOK:
            print('I see a rook')
            total_value += (enemy.value.value * rook_atk_chnc[enemy.type])
    #remove_highlights()
    return total_value




#for a given piece, returns all possible positions for the piece to traverse to
def available_moves(piece):
    if (piece.team == Team.YELLOW or (piece.team == Team.RED) or piece.team == Team.ORANGE):
        if piece.type == Type.PAWN:
            #return  pawn_moves_top(piece.pos)
            if pawn_moves_top is not None:
                return pawn_moves_top(piece.pos)
        elif (piece.type == Type.KING) or (piece.type == Type.QUEEN):
            if maxMovement(3, 0, piece.pos, piece.pos, piece.type.value) is not None:
                return maxMovement(3, 0, piece.pos, piece.pos, piece.type.value)
        elif piece.type == Type.ROOK:
            if maxMovement(2, 0, piece.pos, piece.pos, piece.type.value) is not None:
                return maxMovement(2, 0, piece.pos, piece.pos, piece.type.value)
        elif piece.type == Type.BISHOP:
            if maxMovement(2, 0, piece.pos, piece.pos, piece.type.value) is not None:
                return maxMovement(2, 0, piece.pos, piece.pos, piece.type.value)
        elif piece.type == Type.KNIGHT:
            if maxMovement(4, 0, piece.pos, piece.pos, piece.type.value) is not None:
                return maxMovement(4, 0, piece.pos, piece.pos, piece.type.value)

#generates a list of moves for each piece
def generate_moves(comm, board):
    moves = []
    for troop in comm.troops:
        temp_list = available_moves(troop)
        if temp_list is not None:
            for pos in available_moves(troop):
                #adds additional check so that moves are only appended if the position is an empty square or has an enemy piece
                
                moves.append(Move(troop, troop.pos, (pos[0], pos[1])))

        
    return moves




#moves pieces 
def move_copy_piece(curr_pos: Square, new_pos: Square, c_board):
    c_board[new_pos.row][new_pos.col].piece = c_board[curr_pos.row][curr_pos.col].piece
    c_board[curr_pos.row][curr_pos.col].piece = None
    
def greedy_search(comm):
    moves = generate_moves(comm, board)
    max_score = -100
    best_move = None
    for m in moves:
        curr_score = evaluation(m.piece,m.start_position ,m.end_position, board)
        piece = m.piece
        if curr_score > max_score:
            best_move = m
            max_score = curr_score
        elif curr_score == max_score:
            if moveVal[m.piece.type] < moveVal[best_move.piece.type]:
                best_move = m
    return best_move



# alpha-beta search
#def search_minimax(comm, alpha, beta, maxPlayer, depth, copied_board, best_move = None):
#    # returns static evaluation of best move found
#    score = 0
#
#    if depth == 0:
#        score = evaluation(best_move.piece, best_move.end_position, copied_board)
#        return best_move, score
#
#    # if it is the maximizing player(ai)
#    if maxPlayer == True:
#        max_score = -inf
#
#        moves = []
#        #generates moves for a given commander
#        moves.extend(generate_moves(comm, copied_board))
#        best_move = moves[0]
#        # search through all moves available for that corp
#        for m in moves:
#            #performs move on simulated board
#            move_copy_piece(copied_board[m.start_position[0]][m.start_position[1]], copied_board[m.end_position[0]][m.end_position[1]], copied_board)
#            #calls search on simulated board state
#            best_move, curr_score = search(comm, alpha, beta, False, depth - 1, copied_board, best_move)
#            curr_score *= -1
#            
#            # if the current move is better than the current highest score, replace it
#            if curr_score > max_score:
#                max_score = curr_score
#                best_move = m
             #undos move
#            move_copy_piece(copied_board[m.end_position[0]][m.end_position[1]], copied_board[m.start_position[0]][m.start_position[1]], copied_board)
#            # if the highest score is higher than beta, break out of the loop and return the value at that position?
#            if max_score >= beta:
#                break
#            alpha = max(alpha, max_score)
#
#            #print("Piece: " + str(best_move.piece.type) +"\n"+
#            #    "Start position: " + str(best_move.start_position) +"\n"+
#            #    "End position: " + str(best_move.end_position) +"\n"+
#            #    "Team: "+ str(best_move.piece.team) +"\n" +
#            #    "eval value: " + str(evaluation(best_move.piece, best_move.end_position, copied_board)) + "\n")
#
#        return best_move, max_score
#    elif maxPlayer == False:
#        # inverse process for opposing(human) player
#        min_score = inf
#        moves = []
#
#        for c in player_commanders:
#            moves.extend(generate_moves(c, copied_board))
#        #best_move = moves[0]
#        for m in moves:
#            move_copy_piece(copied_board[m.start_position[0]][m.start_position[1]], copied_board[m.end_position[0]][m.end_position[1]], copied_board)
#            best_move, curr_score = search(comm, alpha, beta, True, depth - 1, copied_board, best_move)
#            
#            if curr_score < min_score:
#                min_score = curr_score
#                best_move = m
#            move_copy_piece(copied_board[m.end_position[0]][m.end_position[1]], copied_board[m.start_position[0]][m.start_position[1]], copied_board)
#            if min_score <= alpha:
#               break
#
#            beta = min(beta, min_score)
#        return best_move, min_score
#
#
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
pawn_start_pos = [(1, 2), (1, 6)]

def message_king_rook(comm):
    red_commander.message = comm.leader.team

def has_knight(comm):
    lost_knight = True
    for troop in comm.troops:
        if troop.type is Type.KNIGHT:
            lost_knight = False

    return lost_knight

def has_only_queen():
    only_queen = True

    for troop in red_commander.troops:
        if troop.type is Type.PAWN:
            only_queen = False
        elif troop.type is Type.ROOK:
            only_queen = False

    return only_queen

# this comment is to do a draw commit

def hard_mode(comm):
    # append leader to troop when half lost
    ai_action = AiAction()


    if comm.leader.type is Type.BISHOP:
        if not has_knight(comm):
            message_king_rook(comm)
        elif len(comm.troops) < 2:
            comm.troops.append(comm.leader)

    elif comm.leader.type is Type.KING:
        if comm.message is not None:
            ai_action.team = red_commander.message
            ai_action.decision = Action.DELEGATE
            return ai_action
        elif has_only_queen():
            ai_action.decision = Action.RECALL
            return ai_action

    # Does action
    # search() Move(): piece, start, end
    chosen_move = search(comm, -inf, inf, True, 5, board) # should store (move, score)

    #moves_sorted = sorted(moves, key=lambda x : x[1])
    #chosen_move = moves_sorted[-1]
    piece = chosen_move[0].piece
    temp_row = chosen_move[0].end_position[0]
    temp_col = chosen_move[0].end_position[1]

    ai_action.troop = piece
    ai_action.square = Square(piece)

    if board[temp_row][temp_col].piece is None:
        ai_action.decision = Action.MOVE
    else:
        ai_action.decision = Action.ATTACK

    return ai_action


'''
    # Get all troop actions
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
'''

def make_decision(comm, mode=DecisionMode.HARD):
    # get remaining troops
    comm.troops = list(set(comm.troops) - set(player_captured_pieces))
    action = None
    # choose decision mode
    if mode is DecisionMode.EASY:
        troop, next_square = easy_mode(comm)
    #elif mode is DecisionMode.MEDIUM:
    #    troop, next_square = medium_mode(comm)
    elif mode is DecisionMode.HARD:
        action = hard_mode(comm)
    #elif mode is DecisionMode.EXTRA_HARD:
    #    troop, next_square = extra_hard_mode()

    troop = action.troop
    next_square = action.square
    decision = action.decision

    return decision, troop, next_square

'''
class AI:
    def __init__(self):

        pass
    
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
'''