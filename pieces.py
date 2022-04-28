from cmath import inf
import enum
import pygame
import random
from common import *
#from GameFunctions import knightAttack
from moves import *

"""
    ATTENTION: Fix the piece moves to return all highlighted squares
"""
#called during evaluation for each piece. represents positions on board and rewards/punishes ai for moving pieces in certain positions

pawn_pos_table = [[0, 0, 0, 0, 0, 0, 0, 0],
                        [0, 0, 0, 10, 10, 10, 0, 0],
                        [4, 4, 4, 4, 4, 4, 4, 4],
                        [4, 4, 4, 4, 4, 4, 4, 4],
                        [4, 4, 4, 4, 4, 4, 4, 4],
                        [4, 4, 4, 4, 4, 4, 4, 4],
                        [-5, -5, -5, -5, -5, -5, -5, -5],
                        [-10, -10, -10, -10, -10, -10, -10, -10]]


rook_pos_table = [[0, 0, 0, 0, 0, 0, 0, 0],
                  [1, 5, 6, 4, 4, 6, 5, 1],
                  [1, 5, 10, 10, 10, 10, 5, 1],
                  [1, 5, 10, 10, 10, 10, 5, 1],
                  [1, 5, 9, 9, 9, 9, 5, 1],
                  [1, 5, 7, 7, 7, 7, 5, 1],
                  [1, 5, 5, 5, 5, 5, 5, 1],
                  [0, 0, 0, 0, 0, 0, 0, 0]]

bishop_pos_table = [[0, 0, 3, 10, 0, 10, 0, 0],
                  [2, 2, 2, 2, 2, 2, 2, 2],
                  [2, 2, 2, 2, 2, 2, 2, 2],
                  [2, 2, 2, 2, 2, 2, 2, 2],
                  [2, 2, 2, 2, 2, 2, 2, 2],
                  [2, 2, 2, 2, 2, 2, 2, 2],
                  [2, 2, 2, 2, 2, 2, 2, 2],
                  [2, 2, 2, 2, 2, 2, 2, 2]]

knight_pos_table = [[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 5, 5, 5, 5, 5, 5, 0],
                  [0, 5, 7, 7, 7, 7, 5, 0],
                  [0, 5, 7, 10, 10, 7, 5, 0],
                  [0, 5, 7, 10, 10, 7, 5, 0],
                  [0, 5, 7, 7, 7, 7, 5, 0],
                  [0, 5, 5, 5, 5, 5, 5, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]]

queen_pos_table = [[0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 5, 5, 5, 5, 5, 5, 0],
                  [0, 5, 7, 7, 7, 7, 5, 0],
                  [0, 5, 7, 10, 10, 7, 5, 0],
                  [0, 5, 7, 9, 9, 7, 5, 0],
                  [0, 5, 7, 7, 7, 7, 5, 0],
                  [0, 5, 5, 5, 5, 5, 5, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0]]

king_pos_table = [[1, 1, 1, 1, 10, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1],
                  [1, 1, 1, 1, 1, 1, 1, 1]]


class Action(enum.Enum):
    MOVE = 0
    ATTACK = 1
    DELEGATE = 2
    RECALL = 3
    PASS = 4

class CommanderMessage:
    def __init__(self, comm, message):
        self.commander = comm
        self.message = message

class PieceAction:
    def __init__(self, action: Action, square=None):
        self.action = action
        self.square = square

class Value(enum.Enum):
    KING = 1000000
    QUEEN = 300
    BISHOP = 800
    KNIGHT = 500
    ROOK = 200
    PAWN = 50

class DecisionMode(enum.Enum):
    EASY = 0
    MEDIUM = 1
    HARD = 2
    EXTRA_HARD = 3

class Team(enum.Enum):
    # Player AI
    YELLOW = 0
    RED = 1
    ORANGE = 2
    # Player Human
    PURPLE = 3
    BLUE = 4
    GREEN = 5


class Type(enum.Enum):
    KING = 0
    QUEEN = 1
    BISHOP = 2
    KNIGHT = 3
    ROOK = 4
    PAWN = 5

enemies = {
    Team.BLUE : [Team.RED, Team.ORANGE, Team.YELLOW],
    Team.GREEN : [Team.RED, Team.ORANGE, Team.YELLOW],
    Team.PURPLE : [Team.RED, Team.ORANGE, Team.YELLOW],
    Team.RED : [Team.BLUE, Team.GREEN, Team.PURPLE],
    Team.ORANGE : [Team.BLUE, Team.GREEN, Team.PURPLE],
    Team.YELLOW : [Team.BLUE, Team.GREEN, Team.PURPLE]
}

moveVal = {
        Type.KNIGHT:  10,
        Type.ROOK:   9,
        Type.QUEEN:   8,
        Type.PAWN:   3,
        Type.BISHOP:   4,
        Type.KING:   5,
}
#following dictionaries associate enemy piece type with the probability of successful capture for each piece type
pawn_atk_chnc = {Type.KING: 0.17,
                Type.QUEEN: 0.17,
                Type.KNIGHT: 0.17,
                Type.BISHOP: 0.33,
                Type.ROOK: 0.17,
                Type.PAWN: 0.5}

king_atk_chnc = {Type.KING: 0.5,
                Type.QUEEN: 0.5,
                Type.KNIGHT: 0.5,
                Type.BISHOP: 0.5,
                Type.ROOK: 0.33,
                Type.PAWN: 1.0}
queen_atk_chnc = {Type.KING: 0.5,
                Type.QUEEN: 0.5,
                Type.KNIGHT: 0.5,
                Type.BISHOP: 0.5,
                Type.ROOK: 0.33,
                Type.PAWN: 0.83}
#add 0.17 to chance when knight has moved before attacking
knight_atk_chnc = {Type.KING: 0.33,
                Type.QUEEN: 0.33,
                Type.KNIGHT: 0.33,
                Type.BISHOP: 0.33,
                Type.ROOK: 0.33,
                Type.PAWN: 0.83}

bishop_atk_chnc = {Type.KING: 0.33,
                Type.QUEEN: 0.33,
                Type.KNIGHT: 0.33,
                Type.BISHOP: 0.5,
                Type.ROOK: 0.33,
                Type.PAWN: 0.67}

rook_atk_chnc = {Type.KING: 0.5,
                Type.QUEEN: 0.5,
                Type.KNIGHT: 0.5,
                Type.BISHOP: 0.33,
                Type.ROOK: 0.33,
                Type.PAWN: 0.33}



#creates a chess piece class that shows:
#team, attackable, and color
class Piece:
    def __init__(self, team, type, image, value, delegated):
        super().__init__()
        self.team = team
        self.type = type
        self.action = None
        self.image = image
        self.value = value
        self.targets = []
        self.delegated = False
        self.pos = None

    def switch_sprite(self, new_img):
        self.image = pygame.image.load(new_img)

    # for ai, checks to see if there are enemies in the pieces attack range. If there are, add them to targets and return targets
    def detect_targets(self, board, positions: tuple[int, int], team: Team):
        for row, col in positions:
            if board[row][col].piece is not None:
                if board[row][col].piece.team in enemies[team]:
                    self.targets.append(board[row][col].piece)
                    print("hi")
        return self.targets

#-------------COMMANDER STUFF IS HERE ------------
# TODO:
#  1) check if troop are being attacked
#  2) is 1) is true then
class Commander:
    def __init__(self, troops, leader) -> None:
        self.leader = leader
        self.troops = troops
        self.targets = []
        self.authority = True
        self.action = True
        self.has_moved = False
        self.knight_special_move = False

    def update_commander(self, commander):
        self.leader = commander.leader
        self.troops = commander.troops
        self.targets = commander.targets
        self.authority = commander.authority
        self.action = commander.action
        self.has_moved = commander.action


    def see_pieces(self):
        for i in range(len(self.troops)):
            print(self.troops[i].type)


    def use_turn(self):
        self.action = False

    def commander_lost(self):
        if self.leader not in self.troops:
            self.authority = False

    """
    how to define move/attack?
    needs to check if an action is valid (maybe already defined?)
    maybe encapsulate action as an object? (action class) -> 
    stores piece that is doing action, position that it is moving to. Doing so allows for a list of moves to be stored
    """
    '''
    #returns numerical evaluation of a particular position that a piece wishes to move to
    def evaluation(self, piece, position, board):
        total_value = 0
        row, col = position[0], position[1]
        #reference piece table values based on piece type
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
        #if a particular position to move to has an enemy piece, add the enemy pieces' value to the evaluation times the chance of successful capture
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
    '''
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
    '''
    #alpha-beta search
    def search(self, moves, alpha, beta, maxPlayer, depth, board):
        #returns static evaluation of best move found
        score = 0
        best_move = None

        if depth == 0:
            score = self.evaluation(best_move[0], best_move[1], board)
            return score

        #if it is the maximizing player(ai)
        if maxPlayer:
            max_score = -inf

            #search through all moves available for that corp
            for m in moves:
                curr_score = self.search(m, alpha, beta, False, depth - 1, board) * -1

                #if the current move is better than the current highest score, replace it
                if curr_score > max_score:
                    max_score = curr_score
                    best_move = moves[m]

                #if the highest score is higher than beta, break out of the loop and return the value at that position?
                if max_score >= beta:
                    break
                alpha = max(alpha, max_score)
            return best_move, max_score
        else:
            #inverse process for opposing(human) player
            min_score = inf
            for m in moves:
                curr_score = self.search(m, alpha, beta, True, depth - 1, board)

                if curr_score < min_score:
                    min_score = curr_score
                    best_move = moves[m]

                if min_score <= alpha:
                    break
                beta = min(beta, min_score)
            return min_score
    '''
    ###############################################
    # Possible modes: Easy, Medium, and Hard
    ###############################################
    '''
    @base strategy: commanders should be in close proximity of troops, however king should have queen be in proximity

    def base_strategy(self):
        pass

    '''
    '''
    @strategy: 
        bishop: randomly choose which troop will move or attack
        king: randomly choose which troop will move, attack, delegated, or recalled
    '''
    '''
    def find_potential_piece_moves(self):
        for row in range(8):
            for col in range(8):
                if board[row][col].color is BLUE or \
                    board[row][col].color is BLACK:
    '''
    '''
    # TODO: finish and follow strategy and base strategy
    # TODO: When finished with medium consider recoding easy with defense strategy
    def easy_mode(self, board):
        # adds lead to action scene in desperation
        if len(self.troops) < 2:
            self.leader.troops.append(self.leader)

        #########################
        # Randomly choose a troop
        #########################
        if not self.knight_special_move:
            troop = random.choice(self.troops)

        decision = None

        ##############################
        # Get troop's actions
        ##############################
        potential_piece_moves(Square(troop))

        troop_moves = []

        troop_actions = [Action.PASS]

        if self.leader.type is Type.KING: # TODO: account for
            if not troop.delegated:
                troop_actions.append(Action.DELEGATE)
            else:
                troop_actions.append(Action.RECALL)

        ##############################
        # Get troop's squares
        ##############################
        if self.knight_special_move:
            knightAttack(Square(troop))
            troop_moves = [Action.ATTACK]

            for row in range(8):
                for col in range(8):
                    if board[row][col].color is BLACK:
                        troop_moves.append(PieceAction(Action.ATTACK, board[row][col]))
                        troop_moves.append(Action.ATTACK)
        else:
            for row in range(8):
                for col in range(8):
                    if board[row][col].color is BLUE:
                        if troop.type is Type.KNIGHT and adjacent_enemies(troop.pos, troop.team) and \
                                not self.knight_special_move:
                            self.knight_special_move = True

                        #global decision
                        #decision = Action.MOVE
                        troop_moves.append(PieceAction(Action.MOVE, board[row][col]))
                        troop_actions.append(Action.MOVE)
                    elif board[row][col].color is BLACK:
                        troop_moves.append(PieceAction(Action.ATTACK, board[row][col]))
                        troop_actions.append(Action.ATTACK)

        ################################
        # Randomly choose troop's action
        ################################
        # randomly choose action
        decision = random.choice(troop_actions)
        team = None

        # if decision is Delegation
        if decision.action is Action.DELEGATE: #TODO:
            if len(orange_commander.troops) < len(yellow_commander.troops):
                team = Team.ORANGE
            else:
                team = Team.YELLOW

        remove_highlights()

        # randomly choose square
        next_square = random.choice(troop_moves)

        return decision, troop, next_square, team
    '''
    '''
    @strategy: 
        bishop: randomly choose which troop will move or attack based on evaluation of present (use evaluation matrix)
        king: randomly choose which troop will move, attack, delegated, or recalled based on evaluation of present
    '''
    '''
    def medium_mode(self):
        troop = None
        next_square = None

        for troop in self.troops:
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
    '''
    def hard_mode(self):
        troop = None
        next_square = None
        return troop, next_square

    def make_decision(self, board, mode=DecisionMode.EASY):
        self.decisions = [] # stores decision, troop current pos, troop next pos
        # get remaining troops
        self.troops = list(set(self.troops) - set(player_captured_pieces))

        troop = None
        next_square = tuple()
        # choose decision mode
        if mode is DecisionMode.EASY:
            troop, next_square = self.easy_mode()
        elif mode is DecisionMode.MEDIUM:
            troop, next_square = self.medium_mode()
        elif mode is DecisionMode.HARD:
            troop, next_square = self.hard_mode()
        elif mode is DecisionMode.EXTRA_HARD:
            troop, next_square = self.extra_hard_mode()

        return troop, next_square
    '''

"""
Each commander needs to know their living troops
Also needs to know all targets in range of troops
Needs to keep track of authority or action it posseses
"""
class King(Commander):
    def __init__(self, troops, leader):
        Commander.__init__(self, troops, leader)
        self.message = None
        #self.delegate_action = True

    #sub refers to sub commander
    def delegate(self, piece, sub):
        # if the piece is not delegated
        if piece.delegated == False and piece is not self.leader and piece in self.troops:
            piece.delegated = True
            self.troops.remove(piece)
            sub.troops.append(piece)
        else:
            print("invalid target for delegation")
        #self.see_pieces

    def recall(self, piece, sub):
        # if the piece has already been delegated
        if piece.delegated == True and piece is not sub.leader and piece in sub.troops:
            piece.delegated = False
            sub.troops.remove(piece)
            self.troops.append(piece)
            #self.see_pieces
"""
King commander must be able to delegate and undelegate pieces
"""
'''
orange_pieces = [board[0][1].piece, board[0][2].piece, board[1][0].piece, board[1][1].piece, board[1][2].piece]
orange_commander = Commander(orange_pieces, board[0][2].piece)
red_pieces = [board[0][0].piece, board[0][7].piece, board[0][3].piece, board[0][4].piece, board[1][3].piece, board[1][4].piece]
red_commander = King(red_pieces, board[0][4].piece)
yellow_pieces = [board[0][5].piece, board[0][6].piece, board[1][5].piece, board[1][6].piece, board[1][7].piece]
yellow_commander = Commander(yellow_pieces, board[0][5].piece)
blue_pieces = [board[7][4].piece, board[7][3].piece, board[7][0].piece, board[7][7].piece, board[6][3].piece, board[6][4].piece]
blue_commander = King(yellow_pieces, board[7][4])
green_pieces = [board[7][1].piece, board[7][2].piece, board[6][0].piece, board[6][1].piece, board[6][2].piece]
green_commander = Commander(yellow_pieces, board[7][2].piece)
purple_pieces = [board[7][5].piece, board[7][6].piece, board[6][5].piece, board[6][6].piece, board[6][7].piece]
purple_commander = Commander(yellow_pieces, board[7][5].piece)
orange_commander.see_pieces()
'''

color_matrix_bishop = {Team.GREEN: './Images/green_bishop.png',
                       Team.PURPLE: './Images/purple_bishop.png',
                       Team.ORANGE: './Images/orange_bishop.png',
                       Team.YELLOW: './Images/yellow_bishop.png',
                       Team.RED: './Images/red_bishop.png',
                       Team.BLUE: './Images/blue_bishop.png'
}
color_matrix_king = {Team.BLUE: './Images/blue_king.png',
                     Team.RED: './Images/red_king.png'
}
color_matrix_pawn = {Team.BLUE: './Images/blue_pawn.png',
                     Team.GREEN: './Images/green_pawn.png',
                     Team.PURPLE: './Images/purple_pawn.png',
                     Team.RED: './Images/red_pawn.png',
                     Team.YELLOW: './Images/yellow_pawn.png',
                     Team.ORANGE: './Images/orange_pawn.png'}

color_matrix_knight = {Team.BLUE: './Images/blue_knight.png',
                       Team.GREEN: './Images/green_knight.png',
                       Team.PURPLE: './Images/purple_knight.png',
                       Team.RED: './Images/red_knight.png',
                       Team.YELLOW: './Images/yellow_knight.png',
                       Team.ORANGE: './Images/orange_knight.png'
                       }

color_matrix_queen = {Team.BLUE: './Images/blue_queen.png',
                      Team.GREEN: './Images/green_queen.png',
                      Team.PURPLE: './Images/purple_queen.png',
                      Team.RED: './Images/red_queen.png',
                      Team.YELLOW: './Images/yellow_queen.png',
                      Team.ORANGE: './Images/orange_queen.png'
                      }

color_matrix_rook = {Team.BLUE: './Images/blue_rook.png',
                     Team.GREEN: './Images/green_rook.png',
                     Team.PURPLE: './Images/purple_rook.png',
                     Team.RED: './Images/red_rook.png',
                     Team.ORANGE: './Images/orange_rook.png',
                     Team.YELLOW: './Images/yellow_rook.png'}

del_matrix_pawn = {Team.GREEN: './Images/green_pawn_d.png',
                     Team.PURPLE: './Images/purple_pawn_d.png',
                     Team.ORANGE: './Images/orange_pawn_d.png',
                     Team.YELLOW: './Images/yellow_pawn_d.png'}

del_matrix_knight = {Team.GREEN: './Images/green_knight_d.png',
                     Team.PURPLE: './Images/purple_knight_d.png',
                     Team.ORANGE: './Images/orange_knight_d.png',
                     Team.YELLOW: './Images/yellow_knight_d.png'}

del_matrix_rook = {Team.GREEN: './Images/green_rook_d.png',
                     Team.PURPLE: './Images/purple_rook_d.png',
                     Team.ORANGE: './Images/orange_rook_d.png',
                     Team.YELLOW: './Images/yellow_rook_d.png'}

del_matrix_queen = {Team.BLUE: './Images/blue_queen.png',
                      Team.GREEN: './Images/green_queen.png',
                      Team.PURPLE: './Images/purple_queen.png',
                      Team.RED: './Images/red_queen.png',
                      Team.YELLOW: './Images/yellow_queen.png',
                      Team.ORANGE: './Images/orange_queen.png'
                      }
"""
    Create instances of pieces.
    Only the original instances of pieces is required. 
    We will chaneg the colors of pieces upon delegation.
"""

coordinates = []

#declare all of the pieces here
rr1 = Piece(Team.RED, Type.ROOK, pygame.image.load('./Images/red_rook.png'), Value.ROOK, False)
ok = Piece(Team.ORANGE, Type.KNIGHT, pygame.image.load('./Images/orange_knight.png'), Value.KNIGHT, False)
ob = Piece(Team.ORANGE, Type.BISHOP, pygame.image.load('./Images/orange_bishop.png'), Value.BISHOP, False)
rK = Piece(Team.RED, Type.KING, pygame.image.load('./Images/red_king.png'), Value.KING, False)
rq = Piece(Team.RED, Type.QUEEN, pygame.image.load('./Images/red_queen.png'), Value.QUEEN, False)
yk = Piece(Team.YELLOW, Type.KNIGHT, pygame.image.load('./Images/yellow_knight.png'), Value.KNIGHT, False)
yb = Piece(Team.YELLOW, Type.BISHOP, pygame.image.load('./Images/yellow_bishop.png'), Value.BISHOP, False)
rr2 = Piece(Team.RED, Type.ROOK, pygame.image.load('./Images/red_rook.png'), Value.ROOK, False)

rp1 = Piece(Team.RED, Type.PAWN, pygame.image.load('./Images/red_pawn.png'), Value.PAWN, False)
rp2 = Piece(Team.RED, Type.PAWN, pygame.image.load('./Images/red_pawn.png'), Value.PAWN, False)
op1 = Piece(Team.ORANGE, Type.PAWN, pygame.image.load('./Images/orange_pawn.png'), Value.PAWN, False)
op2 = Piece(Team.ORANGE, Type.PAWN, pygame.image.load('./Images/orange_pawn.png'), Value.PAWN, False)
op3 = Piece(Team.ORANGE, Type.PAWN, pygame.image.load('./Images/orange_pawn.png'), Value.PAWN, False)
yp1 = Piece(Team.YELLOW, Type.PAWN, pygame.image.load('./Images/yellow_pawn.png'), Value.PAWN, False)
yp2 = Piece(Team.YELLOW, Type.PAWN, pygame.image.load('./Images/yellow_pawn.png'), Value.PAWN, False)
yp3 = Piece(Team.YELLOW, Type.PAWN, pygame.image.load('./Images/yellow_pawn.png'), Value.PAWN, False)

br1 = Piece(Team.BLUE, Type.ROOK, pygame.image.load('./Images/blue_rook.png'), Value.ROOK, False)
gk = Piece(Team.GREEN, Type.KNIGHT, pygame.image.load('./Images/green_knight.png'), Value.KNIGHT, False)
gb = Piece(Team.GREEN, Type.BISHOP, pygame.image.load('./Images/green_bishop.png'), Value.BISHOP, False)
bq = Piece(Team.BLUE, Type.QUEEN, pygame.image.load('./Images/blue_queen.png'), Value.QUEEN, False)
bK = Piece(Team.BLUE, Type.KING, pygame.image.load('./Images/blue_king.png'), Value.KING, False)
pb = Piece(Team.PURPLE, Type.BISHOP, pygame.image.load('./Images/purple_bishop.png'), Value.BISHOP, False)
pk = Piece(Team.PURPLE, Type.KNIGHT, pygame.image.load('./Images/purple_knight.png'), Value.KNIGHT, False)
br2 = Piece(Team.BLUE, Type.ROOK, pygame.image.load('./Images/blue_rook.png'), Value.ROOK, False)

bp1 = Piece(Team.BLUE, Type.PAWN, pygame.image.load('./Images/blue_pawn.png'), Value.PAWN, False)
bp2 = Piece(Team.BLUE, Type.PAWN, pygame.image.load('./Images/blue_pawn.png'), Value.PAWN, False)
gp1 = Piece(Team.GREEN, Type.PAWN, pygame.image.load('./Images/green_pawn.png'), Value.PAWN, False)
gp2 = Piece(Team.GREEN, Type.PAWN, pygame.image.load('./Images/green_pawn.png'), Value.PAWN, False)
gp3 = Piece(Team.GREEN, Type.PAWN, pygame.image.load('./Images/green_pawn.png'), Value.PAWN, False)
pp1 = Piece(Team.PURPLE, Type.PAWN, pygame.image.load('./Images/purple_pawn.png'), Value.PAWN, False)
pp2 = Piece(Team.PURPLE, Type.PAWN, pygame.image.load('./Images/purple_pawn.png'), Value.PAWN, False)
pp3 = Piece(Team.PURPLE, Type.PAWN, pygame.image.load('./Images/purple_pawn.png'), Value.PAWN, False)

#declare teams here
orange_pieces = [op1, op2, op3, ok]
red_pieces = [rp1, rp2, rr1, rr2, rq]
yellow_pieces = [yp1, yp2, yp3, yk]
blue_pieces = []
green_pieces = []
purple_pieces = []
player_delegated_pieces = []
ai_delegated_pieces = []
player_captured_pieces = []
ai_captured_pieces = []
#declare commanders here
orange_commander = Commander(orange_pieces, ob)
red_commander = King(red_pieces, rK)
yellow_commander = Commander(yellow_pieces, yb)
blue_commander = King(blue_pieces, bK)
green_commander = Commander(green_pieces, gb)
purple_commander = Commander(purple_pieces, pb)

player_commanders = [green_commander, blue_commander, purple_commander]
ai_commanders = [orange_commander, red_commander, yellow_commander]

def ReCommand():
    if orange_commander not in ai_commanders:
        ai_commanders.append(orange_commander)
    if yellow_commander not in ai_commanders:
        ai_commanders.append(yellow_commander)
    if green_commander not in player_commanders:
        player_commanders.append(green_commander)
    if purple_commander not in player_commanders:
        player_commanders.append(purple_commander)


# returns input if it is within the boundries on the board
def on_board(position: tuple[int, int]):
    x = position[0]
    y = position[1]
    """
    if -1 < position[0] < 8 and position[1] > -1 and position[-1] < 8:
        return True
    deployed_team
    """
    if (-1 < x < 8) and (-1 < y < 8):
        return True
    else:
        return False

def nextToAlly():


    return True