import sys

from common import *
from board import *
from pieces import *
import guielements as GUI

DEFAULT_IMAGE_SIZE = (GAME_WIDTH / 8, GAME_WIDTH / 8)
SQUARE_WIDTH = SQUARE_HEIGHT = GAME_WIDTH / 8
clock = pygame.time.Clock()

def update_display(screen):
    """ Draw board squares """
    for row in board:
        for square in row:
            x_pos = square.col * (GAME_WIDTH // 8)
            y_pos = square.row * (GAME_WIDTH // 8)
            # will draw squares with no piece
            pygame.draw.rect(screen, square.color, (x_pos, y_pos, GAME_WIDTH, HEIGHT))
            # if square.color == BLUE:
            # print('square color:', square.color)
            # print('finished drawing highlighted rectangles')
            # will draw squares with pieces
            # if starting_order[(square.row, square.col)]:
            # if :
            #    pass
            # if starting_order[(square.row, square.col)] is not None:
            if square.piece is not None:
                screen.blit(pygame.transform.scale(square.piece.image, DEFAULT_IMAGE_SIZE), (x_pos, y_pos))
                # screen.blit(pygame.transform.scale(starting_order[(square.row, square.col)], DEFAULT_IMAGE_SIZE), (square.x_pos, square.y_pos))
    """ Draw board lines """
    gap = GAME_WIDTH // 8
    for i in range(9):
        pygame.draw.line(screen, BLACK, (0, i * gap), (GAME_WIDTH, i * gap))
        for j in range(9):
            pygame.draw.line(screen, BLACK, (j * gap, 0), (j * gap, GAME_WIDTH))

    pygame.draw.rect(screen, BACKGROUND, (801, 0, WIDTH, HEIGHT))
    pygame.draw.rect(screen, BACKGROUND, (0, 801, WIDTH, HEIGHT))
    #print('testing')


def find_square_coordinates(position: tuple[int, int]):
    interval = GAME_WIDTH / 8
    x, y = position
    row = y // interval
    col = x // interval
    return int(row), int(col)


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
                    board[row][col].color = RED
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
    print('finished highlighting')


# take a piece and it's index to determine where the piece can move using functions that are defined for each piece.
def potential_piece_moves(square: Square):
    piece = square.piece
    if piece.type == Type.PAWN:
        if piece.team == Team.YELLOW or (piece.team == Team.RED):
            highlight_moves(pawn_moves_top((square.row, square.col)), square.piece.team)
        else:
            highlight_moves(pawn_moves_bottom((square.row, square.col)), square.piece.team)
    if (piece.type == Type.KING) or (piece.type == Type.QUEEN):
        highlight_moves(king_queen_moves((square.row, square.col)), square.piece.team)
    """
    elif piece.type == Type.ROOK:
        highlight_moves(rook_moves((square.row, square.col)))
    elif piece.type == Type.BISHOP:
        highlight_moves(bishop_moves((square.row, square.col)))
    elif piece.type == Type.QUEEN:
        highlight_moves(queen_moves((square.row, square.col)))
    """
    if piece.type == Type.KNIGHT:
        highlight_moves(knight_moves((square.row, square.col)), square.piece.team)


def move_piece(curr_pos: Square, new_pos: Square):
    board[new_pos.row][new_pos.col].piece = board[curr_pos.row][curr_pos.col].piece
    board[curr_pos.row][curr_pos.col].piece = None
    print('pieced moved')


#Comment out def playgame(): and uncomment if __name__ = '__main__' if you want to run
#basechessgame.py without ScreenGUI.py
#if __name__ == '__main__':
def playgame(screen):
    Home_Button = GUI.button(pos=(WIDTH-100, 100), font_size=25, txt_col=BLACK, bg_col=buttoncolor,
                         text="Return to Homescreen", bg_hover= buttonhover)
    buttons = [Home_Button]
    create_board()
    square_group = []
    current_square = None
    bottom_player_turn = True
    while True:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                #Adding button functionality for home button
                if Home_Button.selected:
                    return True
                pos = pygame.mouse.get_pos()
                #if you dont click on the game board
                if pos[0] >= GAME_WIDTH:
                    print("Clicked on right hand side of board")
                    chosen_square = None

                elif pos[1] >= GAME_WIDTH:
                    print("Clicked on bottom portion of board")
                    chosen_square = None

                #if you do click on the game board
                else:
                    row, col = find_square_coordinates(pos)
                    print('row ', row, ' col ', col)
                    chosen_square = board[row][col]

                # conditions for selected_square
                    if current_square is None:  # have piece selected
                        # positions = potential_piece_moves(board[row][col], (row, col))
                        if chosen_square.piece is None:
                            pass
                        else:
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
            else:
                pass

        update_display(screen)
        for b in buttons:
            b.draw(screen)
            b.moused_over(pygame.mouse.get_pos())
        pygame.display.flip()
        clock.tick(15)
