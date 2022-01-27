from common import *

class Square:
    def __init__(self):
        self.row = 0
        self.col = 0
        self.x_pos = self.row * (WIDTH // 8)
        self.y_pos = self.col * (WIDTH // 8)
        self.color = WHITE
        self.piece = None


board = [[ Square for _ in range(8)] for _ in range(8)]
