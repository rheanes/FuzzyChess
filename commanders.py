
import board as bd
class Commander:
    def __init__(self, troops,  leader) -> None:
        self.leader= leader
        self.troops = troops
        self.targets = []
        self.authority = True

    def see_pieces(self):
        for i in range(len(self.troops)):
            print(self.troops[i].type)
        

    def use_turn(self):
        self.authority = False


    

"""
Each commander needs to know their living troops
Also needs to know all targets in range of troops
Needs to keep track of authority or action it posseses
"""


class King(Commander):
    def __init__(self):
        super().__init__()
        #self.delegate_action = True

    #sub refers to sub commander
    def delegate(self, piece, sub):
        #if the piece has already been delegated
        if piece.delegated == True:
            piece.delegated = False
            sub.troops.remove(piece)
            self.troops.append(piece)
            self.use_turn()
        #if the piece is not delegated
        elif piece.delegated == False:
            piece.delegated = True
            self.troops.remove(piece)
            sub.troops.append(piece)
            self.use_turn()
    

"""
King commander must be able to delegate and undelegate pieces
"""

if __name__ == '__main__':
    
    
    """
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
"""