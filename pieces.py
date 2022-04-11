from cmath import inf
import enum
import pygame
import random
#from board import board
"""
    ATTENTION: Fix the piece moves to return all highlighted squares
"""
#called during evaluation for each piece. represents positions on board and rewards/punishes ai for moving pieces in certain positions
pawn_pos_table = [[-5, 0, 0, 0, 0, 0, 0, -5],
                  [-10, -20, -10, -15, -5, -10, -20, -10],
                  [15, 15, 5, 10, 5, 5, 15, 15],
                  [10, 10, 0, 0, -5, 0, 10, 10],
                  [10, 10, 0, 0, -5, 0, 10, 10],
                  [10, 10, 0, 0, -5, 0, 10, 10],
                  [-5, -5, -5, -5, -5, -5, -5, -5],
                  [0, 0, 0, 0, 0, 0, 0, 0]]

rook_pos_table = [[-15, -15, -15, -15, -15, -15, -15, -15],
                  [15, 15, 10, 10, 5, 10, 15, 15],
                  [10, 10, 5, 5, 5, 3, 10, 10],
                  [8, 8, 8, 8, 8, 8, 8, 8],
                  [8, 8, 8, 8, 8, 8, 8, 8],
                  [10, 10, 5, 5, 5, 3, 10, 10],
                  [15, 15, 10, 10, 5, 10, 15, 15],
                  [-15, -15, -15, -15, -15, -15, -15, -15]]
                  
bishop_pos_table = [[5, 15, 20, 20, 15, 20, 15, 5],
                  [0, 10, 15, 15, 10, 15, 10, 0],
                  [-5, 5, 8, 8, 8, 3, 5, -5],
                  [-15, -15, -15, -15, -15, -15, -15, -15],
                  [-15, -15, -15, -15, -15, -15, -15, -15],
                  [-5, 5, 8, 8, 8, 3, 5, -5],
                  [0, 10, 15, 15, 10, 15, 10, 0],
                  [5, 15, 20, 20, 15, 20, 15, 5]]

knight_pos_table = [[-20, -20, -20, -20, -20, -20, -20, -20],
                  [-20, -15, -10, -5, -5, -10, -15, -20],
                  [-10, 10, 15, 20, 20, 15, 10, -10],
                  [-10, 10, 15, 25, 25, 15, 10, -10],
                  [-10, 10, 15, 25, 25, 15, 10, -10],
                  [-10, 5, 15, 20, 20, 15, 5, -10],
                  [-20, -15, -10, -5, -5, -10, -15, -20],
                  [-20, -20, -20, -20, -20, -20, -20, -20]]

queen_pos_table = [[-20, -20, -20, -20, -20, -20, -20, -20],
                  [-20, -15, -10, -5, -5, -10, -15, -20],
                  [-10, 5, 10, 15, 15, 10, 5, -10],
                  [-10, 10, 15, 25, 25, 15, 10, -10],
                  [-10, 10, 15, 25, 25, 15, 10, -10],
                  [-10, 5, 10, 15, 15, 10, 5, -10],
                  [-20, -15, -10, -5, -5, -10, -15, -20],
                  [-20, -20, -20, -20, -20, -20, -20, -20]]

king_pos_table = [[5, 15, 20, 25, 25, 20, 15, 5],
                  [0, 10, 15, 25, 25, 15, 10, 0],
                  [-5, 5, 8, 8, 8, 3, 5, -5],
                  [-15, -15, -15, -15, -15, -15, -15, -15],
                  [-15, -15, -15, -15, -15, -15, -15, -15],
                  [-5, 5, 8, 8, 8, 3, 5, -5],
                  [0, 10, 15, 25, 25, 15, 10, 0],
                  [5, 15, 20, 25, 25, 20, 15, 5]]
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


class Action(enum.Enum):
    MOVE = 0
    ATTACK = 1

class Value(enum.Enum):
    KING = 2000
    QUEEN = 200
    BISHOP = 400
    KNIGHT = 200
    ROOK = 200
    PAWN = 50

enemies = {
    Team.BLUE : [Team.RED, Team.ORANGE, Team.YELLOW],
    Team.GREEN : [Team.RED, Team.ORANGE, Team.YELLOW],
    Team.PURPLE : [Team.RED, Team.ORANGE, Team.YELLOW],
    Team.RED : [Team.BLUE, Team.GREEN, Team.PURPLE],
    Team.ORANGE : [Team.BLUE, Team.GREEN, Team.PURPLE],
    Team.YELLOW : [Team.BLUE, Team.GREEN, Team.PURPLE]
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

    # for ai, scans entire board for enemies
    def board_scan(self, board):
        for square in board:
            # scan enemies
            if square.piece is not None:
                if enemies[square.piece.team] is Team.RED or \
                    enemies[square.piece.team] is Team.ORANGE or \
                        enemies[square.piece.team] is Team.YELLOW:
                    square[:].piece.pos = (square.row, square.col)
                    self.targets.append(square[:].piece)

                if square.piece.team is self.leader.team:
                    square[:].piece.pos = ()
        return self.targets
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
    """"""
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
    """
    for each moveable square in range for each piece, evaluate those squares (terminal nodes for alpha beta, prunes if that branch has not promising results)
    """
    #alpha-beta search
    def search(self, moves, alpha, beta, maxPlayer, depth, board):
        score = 0
        best_move = moves[0]
        if depth == 0:
            score = self.evaluation(best_move[0], best_move[1], board)
            return score

        if maxPlayer:
            best_score = -inf
            curr_eval = random.randint(0, 100)

    #TODO: This function calls search function. 
    # the commander shoudl chec
    def make_decision(self, board, positions):
        # get troops enemies
        for troop in self.troops:
            for pos in positions:
                self.targets.append(troop[:].detect_targets(board, (pos[0], pos[1]), board[pos[0]][pos[1]].piece.team))

        # get all enemies
        self.targets.append(self.board_scan(board))
        
        # get troop position
        for troop in self.troops:
            print("hi")






"""
Each commander needs to know their living troops
Also needs to know all targets in range of troops
Needs to keep track of authority or action it posseses
"""


class King(Commander):
    def __init__(self, troops, leader):
        Commander.__init__(self, troops, leader)
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
orange_pieces = []
red_pieces = []
yellow_pieces = []
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

#----------_PAWN MOVES HERE--------------

def pawn_moves_top(position: tuple[int, int]): # team on the top
    row, col = position

    positions = []
    for i in range(3):
        curr_col = i + col - 1
        curr_row = row + 1
        if on_board((curr_col, curr_row)):
            # print('row', curr_row, 'col', curr_col)
            positions.append((curr_row, curr_col))

    return positions


# check pawn moves seperatly from other pieces. If space free then x to move.
# otherwise, the piece in front of it is targetable.
def pawn_moves_bottom(position: tuple[int, int]): # team on the bottom
    row, col = position

    positions = []
    for i in range(3):
        curr_col = i + col - 1
        curr_row = row - 1
        if on_board((curr_col, curr_row)):
            # print('row', curr_row, 'col', curr_col)
            positions.append((curr_row, curr_col))

    return positions

