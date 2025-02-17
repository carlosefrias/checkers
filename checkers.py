import pygame
import random

# Constants
EMPTY = 0
HUMAN = 1
COMPUTER = 2
HUMAN_KING = 3
COMPUTER_KING = 4
BOARD_SIZE = 8

# Directions for moves
DIRECTIONS = {
    HUMAN: [(-1, -1), (-1, 1)],
    COMPUTER: [(1, -1), (1, 1)],
    HUMAN_KING: [(-1, -1), (-1, 1), (1, -1), (1, 1)],
    COMPUTER_KING: [(-1, -1), (-1, 1), (1, -1), (1, 1)]
}

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
HIGHLIGHT_COLOR = (0, 255, 0)

# Initialize pygame
pygame.init()
WINDOW_SIZE = 600
SQUARE_SIZE = WINDOW_SIZE // BOARD_SIZE
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption('Checkers')

def create_board():
    """Initialize the checkers board."""
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    for row in range(3):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                board[row][col] = COMPUTER
    for row in range(5, 8):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                board[row][col] = HUMAN
    return board

def draw_board(board, selected=None, possible_moves=[]):
    """Draw the board and pieces."""
    screen.fill(BLACK)
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if (row + col) % 2 == 1:
                pygame.draw.rect(screen, GREY, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if selected and (row, col) == selected:
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            if (row, col) in possible_moves:
                pygame.draw.rect(screen, HIGHLIGHT_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            piece = board[row][col]
            if piece != EMPTY:
                color = RED if piece in [HUMAN, HUMAN_KING] else BLUE
                pygame.draw.circle(screen, color, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 10)
                if piece in [HUMAN_KING, COMPUTER_KING]:
                    pygame.draw.circle(screen, WHITE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 20)

def get_square_under_mouse():
    """Get the board square under the mouse cursor."""
    mouse_pos = pygame.mouse.get_pos()
    x, y = mouse_pos
    row, col = y // SQUARE_SIZE, x // SQUARE_SIZE
    return row, col

def is_valid_move(board, start, end, player):
    """Check if a move is valid."""
    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]

    if piece not in [HUMAN, COMPUTER, HUMAN_KING, COMPUTER_KING]:
        return False

    if player == HUMAN and piece not in [HUMAN, HUMAN_KING]:
        return False
    if player == COMPUTER and piece not in [COMPUTER, COMPUTER_KING]:
        return False

    if end_row < 0 or end_row >= BOARD_SIZE or end_col < 0 or end_col >= BOARD_SIZE:
        return False

    if board[end_row][end_col] != EMPTY:
        return False

    row_diff = end_row - start_row
    col_diff = end_col - start_col

    if (row_diff, col_diff) not in DIRECTIONS[piece]:
        return False

    return True

def is_valid_jump(board, start, end, player):
    """Check if a jump move is valid."""
    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]

    if piece not in [HUMAN, COMPUTER, HUMAN_KING, COMPUTER_KING]:
        return False

    if player == HUMAN and piece not in [HUMAN, HUMAN_KING]:
        return False
    if player == COMPUTER and piece not in [COMPUTER, COMPUTER_KING]:
        return False

    if end_row < 0 or end_row >= BOARD_SIZE or end_col < 0 or end_col >= BOARD_SIZE:
        return False

    if board[end_row][end_col] != EMPTY:
        return False

    row_diff = end_row - start_row
    col_diff = end_col - start_col

    if (row_diff, col_diff) not in [(2 * dr, 2 * dc) for dr, dc in DIRECTIONS[piece]]:
        return False

    mid_row, mid_col = start_row + row_diff // 2, start_col + col_diff // 2
    mid_piece = board[mid_row][mid_col]

    if player == HUMAN and mid_piece not in [COMPUTER, COMPUTER_KING]:
        return False
    if player == COMPUTER and mid_piece not in [HUMAN, HUMAN_KING]:
        return False

    return True

def get_possible_moves(board, player):
    """Get all possible moves for a player."""
    possible_jumps = get_all_possible_jumps(board, player)
    if possible_jumps:
        return possible_jumps
    moves = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] in [HUMAN, HUMAN_KING] if player == HUMAN else [COMPUTER, COMPUTER_KING]:
                if board[row][col] == 0:
                    continue
                for direction in DIRECTIONS[board[row][col]]:
                    new_row, new_col = row + direction[0], col + direction[1]
                    if is_valid_move(board, (row, col), (new_row, new_col), player):
                        moves.append(((row, col), (new_row, new_col)))
                    jump_row, jump_col = row + 2 * direction[0], col + 2 * direction[1]
                    if is_valid_jump(board, (row, col), (jump_row, jump_col), player):
                        moves.append(((row, col), (jump_row, jump_col)))
    return moves

def get_possible_jumps(board, start, player):
    """Get all possible jumps for a piece."""
    jumps = []
    row, col = start
    # import pdb; pdb.set_trace()
    piece = board[row][col]
    if piece == 0:
        return jumps
    for direction in DIRECTIONS[piece]:
        jump_row, jump_col = row + 2 * direction[0], col + 2 * direction[1]
        if is_valid_jump(board, start, (jump_row, jump_col), player):
            jumps.append((jump_row, jump_col))
    return jumps

def get_all_possible_jumps(board, player):
    """Get all possible jumps for a player."""
    jumps = []
    for row in range(BOARD_SIZE):
        for col in range(BOARD_SIZE):
            if board[row][col] in [HUMAN, HUMAN_KING] if player == HUMAN else [COMPUTER, COMPUTER_KING]:
                jumps.extend([((row, col), jump) for jump in get_possible_jumps(board, (row, col), player)])
    return jumps

def make_move(board, start, end, player):
    """Make a move on the board."""
    start_row, start_col = start
    end_row, end_col = end
    piece = board[start_row][start_col]

    board[start_row][start_col] = EMPTY
    board[end_row][end_col] = piece

    # Check if the piece should be crowned
    if player == HUMAN and end_row == 0:
        board[end_row][end_col] = HUMAN_KING
    if player == COMPUTER and end_row == BOARD_SIZE - 1:
        board[end_row][end_col] = COMPUTER_KING

    # Check if a piece was captured
    if abs(end_row - start_row) == 2:
        mid_row, mid_col = (start_row + end_row) // 2, (start_col + end_col) // 2
        board[mid_row][mid_col] = EMPTY

    # Check for additional jumps
    if abs(end_row - start_row) == 2:
        additional_jumps = get_possible_jumps(board, (end_row, end_col), player)
        if additional_jumps:
            return (end_row, end_col), additional_jumps
    return None, []

def evaluate_board(board):
    """Evaluate the board and return a score."""
    human_score = sum(row.count(HUMAN) + 2 * row.count(HUMAN_KING) for row in board)
    computer_score = sum(row.count(COMPUTER) + 2 * row.count(COMPUTER_KING) for row in board)
    return computer_score - human_score

def minimax(board, depth, alpha, beta, maximizing_player):
    """Minimax algorithm with alpha-beta pruning."""
    winner = check_winner(board)
    if winner == COMPUTER:
        return float('inf'), None
    if winner == HUMAN:
        return float('-inf'), None
    if depth == 0:
        return evaluate_board(board), None

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        moves = get_all_possible_jumps(board, COMPUTER) or get_possible_moves(board, COMPUTER)
        for move in moves:
            new_board = [row[:] for row in board]
            make_move(new_board, move[0], move[1], COMPUTER)
            eval, _ = minimax(new_board, depth - 1, alpha, beta, False)
            if eval > max_eval:
                max_eval = eval
                best_move = move
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        moves = get_all_possible_jumps(board, HUMAN) or get_possible_moves(board, HUMAN)
        for move in moves:
            new_board = [row[:] for row in board]
            make_move(new_board, move[0], move[1], HUMAN)
            eval, _ = minimax(new_board, depth - 1, alpha, beta, True)
            if eval < min_eval:
                min_eval = eval
                best_move = move
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move

def computer_move(board):
    """Make the best move for the computer using minimax algorithm."""
    _, best_move = minimax(board, 7, float('-inf'), float('inf'), True)
    if best_move:
        make_move(board, best_move[0], best_move[1], COMPUTER)
    else:
        possible_jumps = get_all_possible_jumps(board, COMPUTER)
        possible_moves = get_possible_moves(board, COMPUTER)
        if possible_jumps:
            move = random.choice(possible_jumps)
            make_move(board, move[0], move[1], COMPUTER)
        elif possible_moves:
            move = random.choice(possible_moves)
            make_move(board, move[0], move[1], COMPUTER)
        else:
            print("Computer has no possible moves.")

def human_move(board):
    """Get and make a move for the human player."""
    selected = None
    possible_moves = []
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_square_under_mouse()
                if selected:
                    if (row, col) in possible_moves:
                        next_move, additional_jumps = make_move(board, selected, (row, col), HUMAN)
                        if additional_jumps:
                            selected = next_move
                            possible_moves = additional_jumps
                        else:
                            return
                    else:
                        selected = None
                        possible_moves = []
                elif board[row][col] in [HUMAN, HUMAN_KING]:
                    selected = (row, col)
                    possible_moves = [move[1] for move in get_possible_moves(board, HUMAN) if move[0] == selected]
        draw_board(board, selected, possible_moves)
        pygame.display.flip()

def check_winner(board):
    """Check if there is a winner."""
    human_pieces = sum(row.count(HUMAN) + row.count(HUMAN_KING) for row in board)
    computer_pieces = sum(row.count(COMPUTER) + row.count(COMPUTER_KING) for row in board)

    if human_pieces == 0:
        return COMPUTER
    if computer_pieces == 0:
        return HUMAN
    if (get_all_possible_jumps(board, HUMAN) or get_possible_moves(board, HUMAN)) == []:
        return COMPUTER
    if (get_all_possible_jumps(board, COMPUTER) or get_possible_moves(board, COMPUTER)) == []:
        return HUMAN
    return None

def play_game():
    """Main function to play the game."""
    board = create_board()
    current_player = HUMAN

    while True:
        draw_board(board)
        pygame.display.flip()
        winner = check_winner(board)
        if winner is not None:
            print("Human wins!" if winner == HUMAN else "Computer wins!")
            pygame.quit()
            exit()

        if current_player == HUMAN:
            if get_all_possible_jumps(board, HUMAN):
                human_move(board)
                if(get_all_possible_jumps(board, HUMAN)):
                    current_player = HUMAN
                else:
                    current_player = COMPUTER
            else:
                human_move(board)
                current_player = COMPUTER
        else:            
            if get_all_possible_jumps(board, COMPUTER):
                computer_move(board)
                if(get_all_possible_jumps(board, COMPUTER)):
                    current_player = COMPUTER
                else:
                    current_player = HUMAN            
            else:
                computer_move(board)
                current_player = HUMAN

if __name__ == "__main__":
    play_game()