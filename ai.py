class Commander:
    def __init__(self, troops, targets) -> None:
        self.troops = troops
        self.targets = targets
        self.authority = False

    #def select

    def heuristic(self, troops, targets):
        return None

    def minmax(self, win_pos, depth, alpha, beta, maximizing):
        if depth == 0 or win_pos:
            
            return None

"""
AI class objects represents each commander
Each commander needs to know their living troops
Also needs to know all targets in range of troops

"""


class King(Commander):
    def __init__(self):
        super().__init__()
        self.delegate_action = True

    def delegate(self, piece):
        if self.delgate_action == True:
            if piece.delegated == True:
                piece.delegated = False
            else:
                piece.delegated = True


"""
King commander must be able to delegate and undelegate pieces
"""

if __name__ == '__main__':
    p = []
    e = []
    k = King(p, e)





