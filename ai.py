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
# commented following code
'''
def enemy_material_count():
    count = 0

    for square in board:
        if square.piece.team in enemy[Team.BLUE]
'''

# rewards ai for moving its pieces to squares that have adjacent allied pieces
def adjacent_allies(pos: tuple[int, int]):
    row, col = pos
    val = 0
    end_pos_list = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                    (row, col - 1), (row, col), (row, col + 1),
                    (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]

    for p in end_pos_list:
        if on_board(p):
            if board[p[0]][p[1]].piece is not None and board[p[0]][p[1]] in enemies[Team.BLUE]:
                val += 10

                p_type = board[p[0]][p[1]].piece.type

                # value based on value of piece
                if p_type is Type.QUEEN:
                    val += 15
                elif p_type is Type.BISHOP:
                    val += 10
                elif p_type is Type.KNIGHT:
                    val += 15
                elif p_type is Type.ROOK:
                    val += 6
                elif p_type is Type.PAWN:
                    val += 2

    return val

def adjacent_king(pos: tuple[int, int]):
    row, col = pos
    end_pos_list = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                    (row, col - 1), (row, col), (row, col + 1),
                    (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]

    for p in end_pos_list:
        if(on_board(p)):
            if board[p[0]][p[1]].piece is not None and board[p[0]][p[1]].piece.type is Type.KING and board[p[0]][p[1]].piece.team in enemies[Team.RED]:
                return True
    return False

def adjacent_enemies(pos: tuple[int, int]):
    row, col = pos
    val = 0
    end_pos_list = [(row - 1, col - 1), (row - 1, col), (row - 1, col + 1),
                    (row, col - 1), (row, col), (row, col + 1),
                    (row + 1, col - 1), (row + 1, col), (row + 1, col + 1)]
    #end_pos_list = [
    #    (row - 2, col - 2),(row - 2, col - 1), (row - 2, col), (row - 2, col + 1), (row - 2, col + 2),
    #    (row-1, col-2),(row-1, col-1), (row-1, col), (row-1, col+1),(row-1, col+2),
    #    (row, col-2),(row, col-1), (row, col), (row,col+1),(row,col+2),
    #    (row+1, col-2),(row+1, col-1), (row+1,col), (row+1, col+1),(row+1, col+2),
    #    (row + 2, col - 2), (row + 2, col - 1), (row + 2, col), (row + 2, col + 1), (row + 2, col + 2)
    #]

    for p in end_pos_list:
        if on_board(p):
            if board[p[0]][p[1]].piece is not None and board[p[0]][p[1]].piece.team in enemies[Team.RED]:
                val += 10
                p_type = board[p[0]][p[1]].piece.type

                # value based on value of piece
                if p_type is Type.QUEEN:
                    val -= 12
                elif p_type is Type.BISHOP:
                    val -= 10
                elif p_type is Type.KNIGHT:
                    val -= 8
                elif p_type is Type.ROOK:
                    val -= 6
                elif p_type is Type.PAWN:
                    val -= 2

    return val

'''

def delegate():
    

'''

'''
    Evaluation:
        
'''
# returns numerical evaluation of a particular position that a piece wishes to move to
def evaluation(piece,start_position, end_position, board):
    total_value = 0
    currRow, currCol = start_position[0], start_position[1]
    row, col = end_position[0], end_position[1]
    total_value += adjacent_allies(end_position) - adjacent_allies(start_position) - adjacent_enemies(end_position)

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
            if adjacent_enemies((row, col)):
                #Add some value if we can move and attack
                total_value += 100
                #if king is adjacent, add some large amount
                if adjacent_king((row, col)):
                    total_value += 50000
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
        curr_score = evaluation(m.piece, m.start_position, m.end_position, board)
        piece = m.piece
        if curr_score > max_score:
            best_move = m
            max_score = curr_score
        elif curr_score == max_score:
            if moveVal[m.piece.type] < moveVal[best_move.piece.type]:
                best_move = m
    if max_score > 0:
        return best_move
    else:
        return None

def generateRandomMove(comm):
    moves = generate_moves(comm, board)
    chosen_move = moves[random.randint(0, len(moves) - 1)]
    return chosen_move

