import enum

"""
    ATTENTION: Fix the piece moves to return all highlighted squares
"""

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
    KING = 20
    QUEEN = 18
    BISHOP = 15
    KNIGHT = 13
    ROOK = 10
    PAWN = 5

#creates a chess piece class that shows:
#team, attackable, and color
class Piece:
    def __init__(self, team, type, image, value):
        super().__init__()
        self.team = team
        self.type = type
        self.action = None
        self.image = image
        self.value = value
        self.delegated = False

enemies = {
    Team.BLUE : [Team.RED, Team.ORANGE, Team.YELLOW],
    Team.GREEN : [Team.RED, Team.ORANGE, Team.YELLOW],
    Team.PURPLE : [Team.RED, Team.ORANGE, Team.YELLOW],
    Team.RED : [Team.BLUE, Team.GREEN, Team.PURPLE],
    Team.ORANGE : [Team.BLUE, Team.GREEN, Team.PURPLE],
    Team.YELLOW : [Team.BLUE, Team.GREEN, Team.PURPLE]
}

"""
    Create instances of pieces.
    Only the original instances of pieces is required. 
    We will chaneg the colors of pieces upon delegation.
"""

coordinates = []

# returns input if it is within the boundries on the board
def on_board(position: tuple[int, int]):
    x, y = position
    """
    if -1 < position[0] < 8 and position[1] > -1 and position[-1] < 8:
        return True
    
    """
    if (-1 < x < 8) and (-1 < y < 8):
        return True
"""
    MOVES OF PIECES
"""


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

"""
     0       1       2       3       4       5       6       7
0   0,0     0,1     0,2      (0,3)    0,4     0,5     (0,6)     0,7
1   1,0    (1,1)   (1,2)     (1,3)   (1,4)   (1,5)     1,6     1,7
2   2,0    (2,1)   (2,2)     (2,3)   (2,4)   (2,5)     2,6     2,7
3   (3,0)  (3,1)   (3,2)      3,3    (3,4)    (3,5     3,6     3,7
4   4,0     4,1    (4,2)    (4,3)     (4,4)     4,5     4,6     4,7
5   5,0    (5,1)   (5,2    (5,3)     5,4     (5,5)     5,6     5,7
6   (6,0)     6,1     6,2    (6,3)     6,4     6,5     (6,6)     6,7
7   7,0     7,1     7,2     7,3     7,4     7,5     7,6     7,7
"""
