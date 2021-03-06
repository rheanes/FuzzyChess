import pieces
from common import *
from pieces import *
from pieces import enemies
import pickle
from copy import deepcopy
#----------------BOARD CREATING AND SQUARE CLASS ------------
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
bonePile = [[Square(None) for _ in range(8)] for _ in range(4)]

#performs deep copy of piece for copy_board, This implementation is necessary since 
# the image attribute in pieces is a Surface object which can't be copied normally with deep copy
def copy_piece(piece): 
    c_piece = Piece(None, None, None, None, False)
    for name, attr in piece.__dict__.items():
        if hasattr(attr, 'copy') and callable(getattr(attr, 'copy')):
            c_piece.__dict__[name] = attr.copy()
        else:
            c_piece.__dict__[name] = deepcopy(attr)
        
    return c_piece 
#creates an empty board and populates it with copies of the pieces from the original board
#TODO: Might have to reset/and or delete this board after each completed call of search
def copy_board(board):
    copy_board = [[Square(None) for _ in range(8)] for _ in range(8)]
    for row in range(8):
        for col in range(8):
            copy_board[row][col].row = row
            copy_board[row][col].col = col
            if board[row][col].piece is not None:
                copy_board[row][col] = Square(copy_piece(board[row][col].piece))
    return copy_board

#assign the proper troops to each commander
def default_troops():
    orange_commander.troops = [op1, op2, op3, ok, ob]
    red_commander.troops = [rr1, rr2, rp1, rp2, rq, rK]
    yellow_commander.troops = [yp1, yp2, yp3, yk, yb]
    blue_commander.troops = [br1, br2, bp1, bp2, bq, bK]
    green_commander.troops = [gp1, gp2, gp3, gk, gb]
    purple_commander.troops = [pp1, pp2, pp3, pk, pb]
    return

#assigns the proper color to everything in each commander's troops
def default_colors():
    for p in red_commander.troops:
        p.team = Team.RED
        p.delegated = False
    for p in yellow_commander.troops:
        p.team = Team.YELLOW
        p.delegated = False
    for p in blue_commander.troops:
        p.team = Team.BLUE
        p.delegated = False
    for p in green_commander.troops:
        p.team = Team.GREEN
        p.delegated = False
    for p in purple_commander.troops:
        p.team = Team.PURPLE
        p.delegated = False
    for p in orange_commander.troops:
        p.team = Team.ORANGE
        p.delegated = False

#Change all sprites to default color
#This is executed right after default_colors, so all Piece.Team is correct.
def default_sprites():
    for c in player_commanders:
        for t in c.troops:
            ReturnPieceSprite(t)
    for c in ai_commanders:
        for t in c.troops:
            ReturnPieceSprite(t)


    return

#takes in a piece and returns the sprite that is the same as the color
def ReturnPieceSprite(t):
    if t is not None:
        #If it's not delegated do this
        if not t.delegated:
            if t.type == Type.PAWN:
                t.switch_sprite(color_matrix_pawn[t.team])
            elif t.type == Type.ROOK:
                t.switch_sprite(color_matrix_rook[t.team])
            elif t.type == Type.KNIGHT:
                t.switch_sprite(color_matrix_knight[t.team])
            elif t.type == Type.QUEEN:
                t.switch_sprite(color_matrix_queen[t.team])
            elif t.type == Type.BISHOP:
                t.switch_sprite(color_matrix_bishop[t.team])
            elif t.type == Type.KING:
                t.switch_sprite(color_matrix_king[t.team])
        else:
            if t.type == Type.PAWN:
                t.switch_sprite(del_matrix_pawn[t.team])
            elif t.type == Type.ROOK:
                t.switch_sprite(del_matrix_rook[t.team])
            elif t.type == Type.KNIGHT:
                t.switch_sprite(del_matrix_knight[t.team])
            elif t.type == Type.QUEEN:
                t.switch_sprite(del_matrix_queen[t.team])

def create_board():
    print(len(ai_commanders))
    ReCommand()
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
    #Sets pos values in the initial set up
    for row in range(8):
        for col in range(8):
            if board[row][col].piece is not None:
                board[row][col].piece.pos = [row, col]

#Create the bone pile and clears the captured pieces
def createBonepile():
    ai_captured_pieces.clear()
    player_captured_pieces.clear()
    bonePile[0] = [Square(None), Square(None), Square(None), Square(None), Square(None), Square(None), Square(None), Square(None)]
    bonePile[1] = [Square(None), Square(None), Square(None), Square(None), Square(None), Square(None), Square(None), Square(None)]
    bonePile[2] = [Square(None), Square(None), Square(None), Square(None), Square(None), Square(None), Square(None), Square(None)]
    bonePile[3] = [Square(None), Square(None), Square(None), Square(None), Square(None), Square(None), Square(None), Square(None)]
    for row in range(4):
        for col in range(8):
            if row == 0 or row == 1:
                bonePile[row][col].color = DARK_BLUE
            else:
                bonePile[row][col].color = RED

            bonePile[row][col].row = row
            bonePile[row][col].col = col

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

def clearBonepile():
    for row in range(4):
        for col in range(8):
            bonePile[row][col] = Square(None)

    #Resets colors
    for row in range(4):
        for col in range(8):
            if (row + col) % 2 == 1:
                board[row][col].color = GREY

            board[row][col].row = row
            board[row][col].col = col
    # new changes


#removes all the pieces from the team that is passed in and appends them to the king.
#this is called when a bishop is captured.
def remove_team(team):
    if team == Team.YELLOW:
        for troop in yellow_commander.troops:
            if troop.type is Type.BISHOP:
                continue
            troop.team = Team.RED
            red_commander.troops.append(troop)
            if troop.type == Type.PAWN:
                troop.switch_sprite(color_matrix_pawn[Team.RED])
            elif troop.type == Type.KNIGHT:
                troop.switch_sprite(color_matrix_knight[Team.RED])
            elif troop.type == Type.ROOK:
                troop.switch_sprite(color_matrix_rook[Team.RED])
            elif troop.type == Type.QUEEN:
                troop.switch_sprite(color_matrix_queen[Team.RED])
            else:
                pass
        yellow_commander.troops.clear()

    elif team == Team.ORANGE:
        print("removing orange team")
        for troop in orange_commander.troops:
            if troop.type is Type.BISHOP:
                continue
            print(troop.type)
            troop.team = Team.RED
            red_commander.troops.append(troop)

            if troop.type == Type.PAWN:
                troop.switch_sprite(color_matrix_pawn[Team.RED])
            elif troop.type == Type.KNIGHT:
                troop.switch_sprite(color_matrix_knight[Team.RED])
            elif troop.type == Type.ROOK:
                troop.switch_sprite(color_matrix_rook[Team.RED])
            elif troop.type == Type.QUEEN:
                troop.switch_sprite(color_matrix_queen[Team.RED])
            else:
                pass
        orange_commander.troops.clear()

    elif team == Team.GREEN:
        for troop in green_commander.troops:
            if troop.type is Type.BISHOP:
                continue
            troop.team = Team.BLUE
            blue_commander.troops.append(troop)
            if troop.type == Type.PAWN:
                troop.switch_sprite(color_matrix_pawn[Team.BLUE])
            elif troop.type == Type.KNIGHT:
                troop.switch_sprite(color_matrix_knight[Team.BLUE])
            elif troop.type == Type.ROOK:
                troop.switch_sprite(color_matrix_rook[Team.BLUE])
            elif troop.type == Type.QUEEN:
                troop.switch_sprite(color_matrix_queen[Team.BLUE])
            else:
                pass
        green_commander.troops.clear()
    elif team == Team.PURPLE:
        for troop in purple_commander.troops:
            if troop.type is Type.BISHOP:
                continue
            troop.team = Team.BLUE
            blue_commander.troops.append(troop)
            if troop.type == Type.PAWN:
                troop.switch_sprite(color_matrix_pawn[Team.BLUE])
            elif troop.type == Type.KNIGHT:
                troop.switch_sprite(color_matrix_knight[Team.BLUE])
            elif troop.type == Type.ROOK:
                troop.switch_sprite(color_matrix_rook[Team.BLUE])
            elif troop.type == Type.QUEEN:
                troop.switch_sprite(color_matrix_queen[Team.BLUE])
            else:
                pass
        purple_commander.troops.clear()

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
    board[new_pos.row][new_pos.col].piece.pos = [new_pos.row, new_pos.col]
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

def highlight_move(position, team: Team):
    row, col = position
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
    myTeam = board[startPos[0]][startPos[1]].piece.team

    #Return conditions
    if (currRow < 0) or (currCol < 0):
        return

    if (currRow > 7) or (currCol > 7):
        return

    if iterations > maxSpeed:
        return

    if (board[currRow][currCol].piece is not None) and (position != startPos):
        if iterations <= 1:
            if position not in positions and board[currRow][currCol].piece.team in enemies[myTeam]:
                positions.append(position)
        if (piece != 4):
            return positions

        #Case of the rook trying to find adjacent pieces. It checks in a one square radius about the piece that was found.
        elif piece == 4:

            #In the event the Rook has found it's first piece, then we check the 1-square radius about the piece found for
            #more enemy pieces.
            if iterations == 1:
                if currCol+1 <= 7:
                    if (board[currRow][currCol+1].piece is not None):
                        newPosition = (currRow, currCol + 1)
                        if newPosition not in positions and board[currRow][currCol+1].piece.team in enemies[myTeam]:
                            positions.append(newPosition)

                if currRow + 1 <= 7 and currCol + 1 <= 7:
                    if (board[currRow+1][currCol+1].piece is not None):
                        newPosition = (currRow + 1, currCol + 1)
                        if newPosition not in positions and board[currRow+1][currCol+1].piece.team in enemies[myTeam]:
                            positions.append(newPosition)

                if currRow+1 <= 7:
                    if (board[currRow+1][currCol].piece is not None):
                        newPosition = (currRow + 1, currCol)
                        if newPosition not in positions and board[currRow+1][currCol].piece.team in enemies[myTeam]:
                            positions.append(newPosition)

                if currRow + 1 <= 7 and currCol - 1 >= 0:
                    if (board[currRow+1][currCol-1].piece is not None):
                        newPosition = (currRow + 1, currCol - 1)
                        if newPosition not in positions and board[currRow+1][currCol-1].piece.team in enemies[myTeam]:
                            positions.append(newPosition)

                if currCol-1 >= 0:
                    if (board[currRow][currCol-1].piece is not None):
                        newPosition = (currRow, currCol - 1)
                        if newPosition not in positions and board[currRow][currCol-1].piece.team in enemies[myTeam]:
                            positions.append(newPosition)

                if currCol-1 >= 0 and currRow-1 >= 0:
                    if(board[currRow-1][currCol-1].piece is not None):
                        newPosition = (currRow - 1, currCol - 1)
                        if newPosition not in positions and board[currRow-1][currCol-1].piece.team in enemies[myTeam]:
                            positions.append(newPosition)

                if(currRow - 1) >= 0:
                    if (board[currRow - 1][currCol].piece is not None):
                        newPosition = (currRow - 1, currCol)
                        if newPosition not in positions and board[currRow - 1][currCol].piece.team in enemies[myTeam]:
                            positions.append(newPosition)

                if(currRow - 1) >= 0 and currCol+1 <= 7:
                    if (board[currRow - 1][currCol + 1].piece is not None):
                        newPosition = (currRow - 1, currCol + 1)
                        if newPosition not in positions and board[currRow - 1][currCol + 1].piece.team in enemies[myTeam]:
                            positions.append(newPosition)
                return positions
            elif iterations == 2:
                if position not in positions and board[currRow][currCol].piece.team in enemies[myTeam]:
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

    myTeam = board[startPos[0]][startPos[1]].piece.team

    if (currRow < 0) or (currCol < 0):
        return

    if (currRow > 7) or (currCol > 7):
        return

    if(board[currRow][currCol].piece is not None) and position != startPos:
        if position not in positions and board[currRow][currCol].piece.team in enemies[myTeam]:
            positions.append(position)
        return positions
    if(board[currRow][currCol].piece is None):
        return positions

    knightAttackPieces((currRow - 1, currCol - 1), startPos, positions)
    knightAttackPieces((currRow - 1, currCol), startPos, positions)
    knightAttackPieces((currRow - 1, currCol + 1), startPos, positions)
    knightAttackPieces((currRow, currCol + 1), startPos, positions)
    knightAttackPieces((currRow + 1, currCol + 1), startPos, positions)
    knightAttackPieces((currRow + 1, currCol), startPos, positions)
    knightAttackPieces((currRow + 1, currCol - 1), startPos, positions)
    knightAttackPieces((currRow, currCol - 1), startPos, positions)

    return positions

#Variant of the floodfill which ignores pieces. Allows commanders to move freely up to their alotted spaces (1 space each)
def commAuthMovement(maxSpeed: int, iterations: int, position: tuple[int, int], startPos: tuple[int, int], piece: int, positions=None):

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
        return positions

    #Checks to the Right square
    commAuthMovement(maxSpeed, iterations + 1, (currRow, currCol + 1), startPos, piece, positions)
    #Checks to the Down-Right square
    commAuthMovement(maxSpeed, iterations + 1, (currRow + 1, currCol + 1), startPos, piece, positions)
    #Checks to the Down square
    commAuthMovement(maxSpeed, iterations + 1, (currRow + 1, currCol), startPos, piece, positions)
    #Checks to the Down-Left square
    commAuthMovement(maxSpeed, iterations + 1, (currRow + 1, currCol - 1), startPos, piece, positions)
    #Checks to the Left square
    commAuthMovement(maxSpeed, iterations + 1, (currRow, currCol - 1), startPos, piece, positions)
    #Checks to the Up-Left square
    commAuthMovement(maxSpeed, iterations + 1, (currRow - 1, currCol - 1), startPos, piece, positions)
    #Checks to the Up Square
    commAuthMovement(maxSpeed, iterations + 1, (currRow - 1, currCol), startPos, piece, positions)
    #Checks to the Up-Right square
    commAuthMovement(maxSpeed, iterations + 1, (currRow - 1, currCol + 1), startPos, piece, positions)

    if position in positions:
        return positions
    elif board[currRow][currCol].piece is None:
        positions.append(position)
    return positions

#----------_PAWN MOVES HERE--------------
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

def pawn_moves_top(position: tuple[int, int]): # team on the top
    row, col = position
    myTeam = board[row][col].piece.team
    positions = []
    for i in range(3):
        curr_col = i + col - 1
        curr_row = row + 1
        if on_board((curr_col, curr_row)):
            if board[curr_row][curr_col].piece is not None and board[curr_row][curr_col].piece.team in enemies[myTeam]:
                # print('row', curr_row, 'col', curr_col)
                positions.append((curr_row, curr_col))
            elif board[curr_row][curr_col].piece is None:
                positions.append((curr_row, curr_col))

    return positions

#----------START LOAD AND SAVE PROCESSING HERE---------------

#This removes all the sprites from the pieces, because they cant be pickled.
#It then pickles the board and adds the sprites back, so game can resume.
def SaveGame(state):
    for row in range(8):
        for col in range(8):
            if board[row][col].piece:
                board[row][col].piece.image = None

    for p in player_captured_pieces:
        p.image = None
    for p in ai_captured_pieces:
        p.image = None
    SaveBoard(state)
    #sets default sprites for all pieces in commander arrays.
    default_sprites()
    return

#a class for saving the game
class saveStruct:
    def __init__(self):
        #board
        self.brd = board
        #player commanders
        self.blc = blue_commander
        self.grc = green_commander
        self.prc = purple_commander
        #ai commanders
        self.rdc = red_commander
        self.orc = orange_commander
        self.ylc = yellow_commander
        #player captured pieces
        self.aicp = pieces.ai_captured_pieces
        #ai captured pieces
        self.plcp = pieces.player_captured_pieces
        #bonepile
        self.bnpl = bonePile

#Does the actual saving of the board.
def SaveBoard(state):
    currentGame = saveStruct()
    if state == 1:
        with open('Save1.pickle', 'wb') as f:
            pickle.dump(currentGame, f)
            return
    if state == 2:
        with open('Save2.pickle', 'wb') as f:
            pickle.dump(currentGame, f)
            return
    if state == 3:
        with open('Save3.pickle', 'wb') as f:
            pickle.dump(currentGame, f)
            return

#Loads the save file into the board.
#Then re-sets up the game with setBoard()
def LoadGame(state):
    if state == 1:
        with open('Save1.pickle', 'rb') as f:
            item = pickle.load(f)
    if state == 2:
        with open('Save2.pickle', 'rb') as f:
            item = pickle.load(f)
    if state == 3:
        with open('Save3.pickle', 'rb') as f:
            item = pickle.load(f)
    setBoard(item)
    return

def setBoard(item):
    bord = item.brd
    bnpl = item.bnpl
    #set the commanders to what they were last game.
    pieces.blue_commander.update_commander(item.blc)
    pieces.green_commander.update_commander(item.grc)
    pieces.purple_commander.update_commander(item.prc)
    pieces.red_commander.update_commander(item.rdc)
    pieces.orange_commander.update_commander(item.orc)
    pieces.yellow_commander.update_commander(item.ylc)
    #clear ai_commanders and player_commanders
    ai_commanders.clear()
    player_commanders.clear()
    #set ai captured pieces arrays.
    for p in item.aicp:
        ai_captured_pieces.append(p)
    for p in ai_captured_pieces:
        ReturnPieceSprite(p)
    #set player captured pieces array and restore sprites
    for p in item.plcp:
        player_captured_pieces.append(p)
    for p in player_captured_pieces:
        ReturnPieceSprite(p)

    #add back sprites to the pieces.
    for row in range(8):
        for col in range(8):
            #set each square of the board equal to the saved version
            board[row][col] = bord[row][col]
            #addes sprites back to the pieces
            if board[row][col].piece:
                #reloads the piece color back into the game
                ReturnPieceSprite(board[row][col].piece)
                #if the bishop eexists, append it back to commander arrays.
                if (board[row][col].piece.type == Type.BISHOP) or (board[row][col].piece.type == Type.KING):
                    BishopHandler(board[row][col].piece.team)
    # restore the bone pile
    for row in range(4):
        for col in range(8):
            bonePile[row][col] = bnpl[row][col]
            if bonePile[row][col].piece:
                ReturnPieceSprite(board[row][col].piece)
    return


def BishopHandler(team):
    if team == Team.BLUE:
        player_commanders.append(blue_commander)
    if team == Team.GREEN:
        player_commanders.append(green_commander)
    if team == Team.PURPLE:
        player_commanders.append(purple_commander)
    if team == Team.RED:
        ai_commanders.append(red_commander)
    if team == Team.ORANGE:
        ai_commanders.append(orange_commander)
    if team == Team.YELLOW:
        ai_commanders.append(yellow_commander)





