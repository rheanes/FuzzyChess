import sys

from board import *
from pieces import *

DEFAULT_IMAGE_SIZE = (WIDTH / 8, WIDTH / 8)
SQUARE_WIDTH = SQUARE_HEIGHT = WIDTH / 8

# creates 800 by 800 Pixel window to play the game on
window = pygame.display.set_mode((WIDTH, WIDTH))
# Set caption for Window
pygame.display.set_caption("Chess")
clock = pygame.time.Clock()


def update_display():
    """
    starting_order = {(0, 0): pygame.image.load(rr.image),
                      (1, 0): pygame.image.load(on.image),
                      (2, 0): pygame.image.load(ob.image),
                      (3, 0): pygame.image.load(rq.image),
                      (4, 0): pygame.image.load(rk.image),
                      (5, 0): pygame.image.load(yb.image),
                      (6, 0): pygame.image.load(yn.image),
                      (7, 0): pygame.image.load(rr.image),
                      (0, 1): pygame.image.load(op.image),
                      (1, 1): pygame.image.load(op.image),
                      (2, 1): pygame.image.load(op.image),
                      (3, 1): pygame.image.load(rp.image),
                      (4, 1): pygame.image.load(rp.image),
                      (5, 1): pygame.image.load(yp.image),
                      (6, 1): pygame.image.load(yp.image),
                      (7, 1): pygame.image.load(yp.image),

                      (0, 2): None, (1, 2): None, (2, 2): None, (3, 2): None,
                      (4, 2): None, (5, 2): None, (6, 2): None, (7, 2): None,
                      (0, 3): None, (1, 3): None, (2, 3): None, (3, 3): None,
                      (4, 3): None, (5, 3): None, (6, 3): None, (7, 3): None,
                      (0, 4): None, (1, 4): None, (2, 4): None, (3, 4): None,
                      (4, 4): None, (5, 4): None, (6, 4): None, (7, 4): None,
                      (0, 5): None, (1, 5): None, (2, 5): None, (3, 5): None,
                      (4, 5): None, (5, 5): None, (6, 5): None, (7, 5): None,

                      (0, 6): pygame.image.load(gp.image),
                      (1, 6): pygame.image.load(gp.image),
                      (2, 6): pygame.image.load(gp.image),
                      (3, 6): pygame.image.load(bp.image),
                      (4, 6): pygame.image.load(bp.image),
                      (5, 6): pygame.image.load(pp.image),
                      (6, 6): pygame.image.load(pp.image),
                      (7, 6): pygame.image.load(pp.image),
                      (0, 7): pygame.image.load(br.image),
                      (1, 7): pygame.image.load(gn.image),
                      (2, 7): pygame.image.load(gb.image),
                      (3, 7): pygame.image.load(bq.image),
                      (4, 7): pygame.image.load(bk.image),
                      (5, 7): pygame.image.load(pb.image),
                      (6, 7): pygame.image.load(pn.image),
                      (7, 7): pygame.image.load(br.image)}
    """
    """ Draw board squares """
    for row in board:
        for square in row:
            x_pos = square.col * (WIDTH // 8)
            y_pos = square.row * (WIDTH // 8)
            # will draw squares with no piece
            pygame.draw.rect(window, square.color, (x_pos, y_pos, SQUARE_WIDTH, SQUARE_HEIGHT))
            # if square.color == BLUE:
            # print('square color:', square.color)
            # print('finished drawing highlighted rectangles')
            # will draw squares with pieces
            # if starting_order[(square.row, square.col)]:
            # if :
            #    pass
            # if starting_order[(square.row, square.col)] is not None:
            if square.piece is not None:
                window.blit(pygame.transform.scale(square.piece.image, DEFAULT_IMAGE_SIZE), (x_pos, y_pos))
                # window.blit(pygame.transform.scale(starting_order[(square.row, square.col)], DEFAULT_IMAGE_SIZE), (square.x_pos, square.y_pos))

    """ Draw board lines """
    gap = WIDTH // 8
    for i in range(8):
        pygame.draw.line(window, BLACK, (0, i * gap), (WIDTH, i * gap))
        for j in range(8):
            pygame.draw.line(window, BLACK, (j * gap, 0), (j * gap, WIDTH))
    pygame.display.update()
    clock.tick(15)


def find_square_coordinates(position: tuple[int, int]):
    interval = WIDTH / 8
    x, y = position
    row = y // interval
    col = x // interval
    return int(row), int(col)


# highlight possible moves
# add 'type: Action' for type of action
def highlight_moves(positions: tuple[int, int]):
    for row, col in positions:
        if board[row][col].color == BLUE:
            pass
        else:
            board[row][col].color = BLUE
            """
            if type is Action.MOVE:
                board[row][col].color = BLUE
            elif type is Action.ATTACK:
                board[row][col].color = RED
            """
    print('finished highlighting')


# take a piece and it's index to determine where the piece can move using functions that are defined for each piece.
def potential_piece_moves(square: Square):
    piece = square.piece
    if piece.type == Type.PAWN:
        if piece.team == Team.YELLOW or (piece.team == Team.RED):
            highlight_moves(pawn_moves_top((square.row, square.col)))
        else:
            highlight_moves(pawn_moves_bottom((square.row, square.col)))
    if (piece.type == Type.KING) or (piece.type == Type.QUEEN):
        highlight_moves(king_queen_moves((square.row, square.col)))
    """
    elif piece.type == Type.ROOK:
        highlight_moves(rook_moves((square.row, square.col)))
    elif piece.type == Type.BISHOP:
        highlight_moves(bishop_moves((square.row, square.col)))
    elif piece.type == Type.QUEEN:
        highlight_moves(queen_moves((square.row, square.col)))
    """
    if piece.type == Type.KNIGHT:
        highlight_moves(knight_moves((square.row, square.col)))


def move_piece(curr_pos: Square, new_pos: Square):
    board[new_pos.row][new_pos.col].piece = board[curr_pos.row][curr_pos.col].piece
    board[curr_pos.row][curr_pos.col].piece = None
    print('pieced moved')


if __name__ == '__main__':
    create_board()
    # button_group = Group()
    current_square = None
    bottom_player_turn = True
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = find_square_coordinates(pos)
                print('row ', row, ' col ', col)
                chosen_square = board[row][col]

                # conditions for selected_square
                if current_square is None:  # have piece selected
                    # positions = potential_piece_moves(board[row][col], (row, col))
                    current_square = chosen_square
                    potential_piece_moves(board[row][col])
                    """
                    for position in positions:
                        row, col = position
                        board[row][col].color = BLUE
                    """
                else:  # a piece is already selected
                    if chosen_square.piece is not None:
                        remove_highlights()
                        current_square = chosen_square
                        potential_piece_moves(board[row][col])
                    elif (board[row][col].color is WHITE) or (board[row][col].color is GREY):
                        remove_highlights()
                        current_square = None
                    elif board[row][col].color is BLUE:
                        if board[row][col].piece is not None:
                            remove_highlights()
                            move_piece(current_square, chosen_square)
                        else:
                            remove_highlights()
                            move_piece(current_square, chosen_square)
                    else:
                        pass
                # else:
                #    pass

            else:
                pass
        update_display()
