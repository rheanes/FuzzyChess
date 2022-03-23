from common import *
from pieces import *


#----------------BOARD CREATING AND SQUATE CLASS ------------
class Square:
    def __init__(self, piece):
        super().__init__()
        self.row = 0
        self.col = 0
        # self.x_pos = self.row * (WIDTH // 8)
        # self.y_pos = self.col * (WIDTH // 8)
        self.color = (255, 255, 255)
        self.piece = piece


board = [[Square(None) for _ in range(8)] for _ in range(8)]


#assign the proper troops to each commander
def default_troops():
    orange_commander.troops = [op1, op2, op3, ok, ob]
    red_commander.troops = [rr1, rr2, rp1, rp2, rq, rK]
    yellow_commander.troops = [yp1, yp2, yp3, yk, yb]
    blue_commander.troops = [br1, br2, bp1, bp2, bq, bK]
    green_commander.troops = [gp1, gp2, gp3, gk, gb]
    purple_commander.troops = [pp1, pp2, pp3, pk, pb]
    return

def default_colors():
    for p in red_commander.troops:
        p.team = Team.RED
    for p in yellow_commander.troops:
        p.team = Team.YELLOW
    for p in blue_commander.troops:
        p.team = Team.BLUE
    for p in green_commander.troops:
        p.team = Team.GREEN
    for p in purple_commander.troops:
        p.team = Team.PURPLE

#Change all sprites to default color
#This is executed right after default_colors, so all Piece.Team is correct.
def default_sprites():
    for c in player_commanders:
        for t in c.troops:
            if t.type == Type.PAWN:
                t.switch_sprite(color_matrix_pawn[t.team])
            elif t.type == Type.ROOK:
                t.switch_sprite(color_matrix_rook[t.team])
            elif t.type == Type.KNIGHT:
                t.switch_sprite(color_matrix_knight[t.team])
            elif t.type == Type.QUEEN:
                t.switch_sprite(color_matrix_queen[t.team])
    for c in ai_commanders:
        for t in c.troops:
            if t.type == Type.PAWN:
                t.switch_sprite(color_matrix_pawn[t.team])
            elif t.type == Type.ROOK:
                t.switch_sprite(color_matrix_rook[t.team])
            elif t.type == Type.KNIGHT:
                t.switch_sprite(color_matrix_knight[t.team])
            elif t.type == Type.QUEEN:
                t.switch_sprite(color_matrix_queen[t.team])
    return
#if troop.type == Type.PAWN:
# creates the board

def create_board():
    default_troops()
    default_colors()
    default_sprites()
    board[0] = [Square(rr1),
                Square(ok),
                Square(ob),
                Square(rq),
                Square(rK),
                Square(yb),
                Square(yk),
                Square(rr2)]

    board[7] = [Square(br1),
                Square(gk),
                Square(gb),
                Square(bq),
                Square(bK),
                Square(pb),
                Square(pk),
                Square(br2)]

    
    board[1][0] = Square(op1)
    board[1][1] = Square(op2)
    board[1][2] = Square(op3)
    board[6][0] = Square(gp1)
    board[6][1] = Square(gp2)
    board[6][2] = Square(gp3)
        
    board[1][3] = Square(rp1)
    board[1][4] = Square(rp2)
    board[6][3] = Square(bp1)
    board[6][4] = Square(bp2)

    board[1][5] = Square(yp1)
    board[1][6] = Square(yp2)
    board[1][7] = Square(yp3)
    board[6][5] = Square(pp1)
    board[6][6] = Square(pp2)
    board[6][7] = Square(pp3)
#adding colors to squares
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col].color = GREY

            board[row][col].row = row
            board[row][col].col = col
            """
            board[row][col].x_pos = col * (WIDTH // 8)
            board[row][col].y_pos = row * (WIDTH // 8)
            """

def clear_board():
    for row in range(8):
        for col in range(8):
            board[row][col] = Square(None)
    # adding colors to squares
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col].color = GREY

            board[row][col].row = row
            board[row][col].col = col
            """
            board[row][col].x_pos = col * (WIDTH // 8)
            board[row][col].y_pos = row * (WIDTH // 8)
            """

    # new changes
    # TODO add in queen, and rooks.
def remove_team(team):
    old_troops = []
    if team == team.YELLOW:
        print("removing yellow team")
        for troop in yellow_commander.troops:
            troop.team = Team.RED
            if troop.type == Type.PAWN:
                print('pawn')
                troop.switch_sprite(color_matrix_pawn[Team.RED])
            elif troop.type == Type.BISHOP:
                print('bishop')
                troop.switch_sprite(color_matrix_pawn[Team.RED])
            elif troop.type == Type.KNIGHT:
                print('knight')
                troop.switch_sprite(color_matrix_knight[Team.RED])
            elif troop.type == Type.ROOK:
                print('rook')
                troop.switch_sprite(color_matrix_rook[Team.RED])
            elif troop.type == Type.QUEEN:
                print('queen')
                troop.switch_sprite(color_matrix_queen[Team.RED])
            else:
                pass
        red_commander.troops.append(yellow_commander.troops)

    elif team == team.ORANGE:
        print("removing orange team")
        for troop in orange_commander.troops:
            troop.team = Team.RED
            if troop.type == Type.PAWN:
                troop.switch_sprite(color_matrix_pawn[Team.RED])
            elif troop.type == Type.BISHOP:
                troop.switch_sprite(color_matrix_pawn[Team.RED])
            elif troop.type == Type.KNIGHT:
                troop.switch_sprite(color_matrix_knight[Team.RED])
            else:
                pass
        red_commander.troops.append(orange_commander.troops)

    elif team == team.GREEN:
        print("removing green team")
        for troop in green_commander.troops:
            troop.team = Team.BLUE
            if troop.type == Type.PAWN:
                troop.switch_sprite(color_matrix_pawn[Team.BLUE])
            elif troop.type == Type.BISHOP:
                troop.switch_sprite(color_matrix_pawn[Team.BLUE])
            elif troop.type == Type.KNIGHT:
                troop.switch_sprite(color_matrix_knight[Team.BLUE])
            else:
                pass
        blue_commander.troops.append(green_commander.troops)

    elif team == team.PURPLE:
        print("removing purple team")
        for troop in purple_commander.troops:
            troop.team = Team.BLUE
            if troop.type == Type.PAWN:
                troop.switch_sprite(color_matrix_pawn[Team.BLUE])
            elif troop.type == Type.BISHOP:
                troop.switch_sprite(color_matrix_pawn[Team.BLUE])
            elif troop.type == Type.KNIGHT:
                troop.switch_sprite(color_matrix_knight[Team.BLUE])
            else:
                pass
        blue_commander.troops.append(purple_commander.troops)

    #_----------_SQUARE UTILITY-------------

def find_square_coordinates(position: tuple[int, int]):
    interval = GAME_WIDTH / 8
    x, y = position
    row = y // interval
    col = x // interval
    return int(row), int(col)

def move_piece(curr_pos: Square, new_pos: Square):
    board[new_pos.row][new_pos.col].piece = board[curr_pos.row][curr_pos.col].piece
    board[curr_pos.row][curr_pos.col].piece = None
    #print('pieced moved')

#--------------__SQUARE HIGHLIGHTING AND UNHIGHLIGHTING------------------

# highlight possible moves
# add 'type: Action' for type of action
def highlight_moves(positions: tuple[int, int], team: Team):
    for row, col in positions:
        if board[row][col].color == BLUE:
            pass
        else:
            if board[row][col].piece is None:
                board[row][col].color = BLUE
            elif board[row][col].piece is not None:
                if board[row][col].piece.team in enemies[team]:
                    board[row][col].color = BLACK
                else:
                    pass
            else:
                pass

            """
            if type is Action.MOVE:
                board[row][col].color = BLUE
            elif type is Action.ATTACK:
                board[row][col].color = RED
            """
    #print('finished highlighting')

def remove_highlights():
    for row in range(8):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col].color = GREY
            else:
                board[row][col].color = WHITE
    #print('removed highlights')


#------------------_PATHFINDING STUFF-------------

# Takes an input piece, and determines the maximum movement it can make. This is done through a recursive BFS
# that goes as far as the piece has movement.
# Implement a BFS algorithm to check spots around the square, and the spots around the
# accompanying squares up to the length of which the Rook can move.
# Essentially, from your position, check the coords (x,y), and then their potential partners
# up to the maximum movement. If any of the spaces found within the BFS are unoccupied, then
# we will add it to the list we are making. Afterwards, we append the list to the positions
#############################################################################################
#                                  POSITIONS TO CHECK PER SPACE                             #
#############################################################################################
#                         (pos - 1, pos + 1) | (pos, pos + 1) | (pos + 1, pos + 1)          #
#                         (pos - 1, pos)     |  CURR_POS      | (pos + 1, pos)              #
#                         (pos - 1, pos - 1) | (pos, pos - 1) | (pos + 1, pos - 1)          #
#############################################################################################
def maxMovement(maxSpeed: int, iterations: int, position: tuple[int, int], startPos: tuple[int, int], piece: int, positions=None):

    if positions is None:
        positions = []
    currRow = position[0]
    currCol = position[1]

    if (currRow < 0) or (currCol < 0):
        return

    if (currRow > 7) or (currCol > 7):
        return

    if iterations > maxSpeed:
        return

    if (board[currRow][currCol].piece is not None) and (position != startPos):
        if iterations <= 1:
            positions.append(position)
        if (piece != 4):
            return positions

        elif piece == 4:
            if iterations == 1:
                if currCol+1 <= 7:
                    if (board[currRow][currCol+1].piece is not None):
                        newPosition = (currRow, currCol + 1)
                        if newPosition not in positions:
                            positions.append(newPosition)

                if currRow + 1 <= 7 and currCol + 1 <= 7:
                    if (board[currRow+1][currCol+1].piece is not None):
                        newPosition = (currRow + 1, currCol + 1)
                        if newPosition not in positions:
                            positions.append(newPosition)

                if currRow+1 <= 7:
                    if (board[currRow+1][currCol].piece is not None):
                        newPosition = (currRow + 1, currCol)
                        if newPosition not in positions:
                            positions.append(newPosition)

                if currRow + 1 <= 7 and currCol - 1 >= 0:
                    if (board[currRow+1][currCol-1].piece is not None):
                        newPosition = (currRow + 1, currCol - 1)
                        if newPosition not in positions:
                            positions.append(newPosition)

                if currCol-1 >= 0:
                    if (board[currRow][currCol-1].piece is not None):
                        newPosition = (currRow, currCol - 1)
                        if newPosition not in positions:
                            positions.append(newPosition)

                if currCol-1 >= 0 and currRow-1 >= 0:
                    if(board[currRow-1][currCol-1].piece is not None):
                        newPosition = (currRow - 1, currCol - 1)
                        if newPosition not in positions:
                            positions.append(newPosition)

                if(currRow - 1) >= 0:
                    if (board[currRow - 1][currCol].piece is not None):
                        newPosition = (currRow - 1, currCol)
                        if newPosition not in positions:
                            positions.append(newPosition)

                if(currRow - 1) >= 0 and currCol+1 <= 7:
                    if (board[currRow - 1][currCol + 1].piece is not None):
                        newPosition = (currRow - 1, currCol + 1)
                        if newPosition not in positions:
                            positions.append(newPosition)
                return positions
            elif iterations == 2:
                positions.append(position)
                return positions
            return positions
        return positions

    if (board[currRow][currCol].piece is not None) and (position != startPos):
        return positions

    #Checks to the Right square
    maxMovement(maxSpeed, iterations + 1, (currRow, currCol + 1), startPos, piece, positions)
    #Checks to the Down-Right square
    maxMovement(maxSpeed, iterations + 1, (currRow + 1, currCol + 1), startPos, piece, positions)
    #Checks to the Down square
    maxMovement(maxSpeed, iterations + 1, (currRow + 1, currCol), startPos, piece, positions)
    #Checks to the Down-Left square
    maxMovement(maxSpeed, iterations + 1, (currRow + 1, currCol - 1), startPos, piece, positions)
    #Checks to the Left square
    maxMovement(maxSpeed, iterations + 1, (currRow, currCol - 1), startPos, piece, positions)
    #Checks to the Up-Left square
    maxMovement(maxSpeed, iterations + 1, (currRow - 1, currCol - 1), startPos, piece, positions)
    #Checks to the Up Square
    maxMovement(maxSpeed, iterations + 1, (currRow - 1, currCol), startPos, piece, positions)
    #Checks to the Up-Right square
    maxMovement(maxSpeed, iterations + 1, (currRow - 1, currCol + 1), startPos, piece, positions)

    if position in positions:
        return positions
    elif board[currRow][currCol].piece is None:
        positions.append(position)
    return positions

#Is only called when the knight is attacking after moving. It highlights *enemy* pieces around the knight
#Functions almost the same as the pathfinding
def knightAttackPieces(position: tuple[int, int], startPos: tuple[int, int], positions = None):
    if positions is None:
        positions = []

    currRow = position[0]
    currCol = position[1]

    if (currRow < 0) or (currCol < 0):
        return

    if (currRow > 7) or (currCol > 7):
        return

    if(board[currRow][currCol].piece is not None) and position != startPos:
        positions.append(position)
        return positions
    if(board[currRow][currCol].piece is None):
        return

    knightAttackPieces((currRow - 1, currCol - 1), startPos, positions)
    knightAttackPieces((currRow - 1, currCol), startPos, positions)
    knightAttackPieces((currRow - 1, currCol + 1), startPos, positions)
    knightAttackPieces((currRow, currCol + 1), startPos, positions)
    knightAttackPieces((currRow + 1, currCol + 1), startPos, positions)
    knightAttackPieces((currRow + 1, currCol), startPos, positions)
    knightAttackPieces((currRow + 1, currCol - 1), startPos, positions)
    knightAttackPieces((currRow, currCol - 1), startPos, positions)

    return positions
