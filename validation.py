import numpy as np
import random
from genetic_algo import evaluate_fitness  # Direct import of the function

# Constants for piece values
BLACK = 1
WHITE = -1
EMPTY = 0


def board_to_char(board):
    """Convert numerical board to character representation."""
    char_board = []
    for i in range(8):
        row = []
        for j in range(8):
            if board[i][j] == BLACK:
                row.append('B')
            elif board[i][j] == WHITE:
                row.append('W')
            else:
                row.append('.')
        char_board.append(row)
    return char_board


def is_valid_move_board(board, row, col, player):
    """Check if a move is valid on the board."""
    # Check boundaries and if the cell is empty
    if row < 0 or row >= 8 or col < 0 or col >= 8 or board[row][col] != EMPTY:
        return False

    opponent = WHITE if player == BLACK else BLACK

    # Check all 8 directions
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        # If adjacent cell has opponent's piece, explore further in that direction
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            # Continue in that direction
            r += dr
            c += dc
            while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
                r += dr
                c += dc
            # If we found our piece, then the move is valid
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                return True

    return False


def make_move_board(board, row, col, player):
    """Make a move on the board and flip appropriate pieces."""
    if not is_valid_move_board(board, row, col, player):
        return False

    board[row][col] = player
    opponent = WHITE if player == BLACK else BLACK

    # Check all 8 directions
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        to_flip = []

        # Collect pieces to flip in this direction
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            to_flip.append((r, c))
            r += dr
            c += dc

        # If we found our piece, flip all collected pieces
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            for fr, fc in to_flip:
                board[fr][fc] = player

    return True


def get_valid_moves(board, player):
    """Get all valid moves for a player on the current board."""
    moves = []
    for i in range(8):
        for j in range(8):
            if is_valid_move_board(board, i, j, player):
                moves.append((i, j))
    return moves


def gene_agent_move(genes, board, player):
    """Determine the best move for the genetic algorithm agent."""
    moves = get_valid_moves(board, player)
    if not moves:
        return None

    best_move = None
    best_score = float('-inf')

    for move in moves:
        # Create a copy to avoid modifying the original board
        board_copy = np.copy(board)
        make_move_board(board_copy, move[0], move[1], player)

        # Convert to character representation for evaluation
        char_board = board_to_char(board_copy)

        # Evaluate the board position using the genetic algorithm weights
        # Fixed: Use directly imported evaluate_fitness instead of GA.evaluate_fitness
        score = evaluate_fitness(genes, char_board, 'B' if player == BLACK else 'W')

        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def simulate_game(genes):
    """Simulate a full game to evaluate the fitness of a gene set."""
    # Initialize the board with standard Othello starting position
    board = np.zeros((8, 8), dtype=int)
    board[3, 3] = board[4, 4] = WHITE
    board[3, 4] = board[4, 3] = BLACK
    current_player = BLACK

    while True:
        moves_black = get_valid_moves(board, BLACK)
        moves_white = get_valid_moves(board, WHITE)

        # Game over if no valid moves for either player
        if not moves_black and not moves_white:
            break

        if current_player == BLACK:
            if moves_black:
                move = gene_agent_move(genes, board, BLACK)
                if move is not None:  # Fixed: Check for None instead of assuming a valid move
                    make_move_board(board, move[0], move[1], BLACK)
            # Switch players even if there are no valid moves
        else:  # WHITE's turn
            if moves_white:
                # Random opponent for testing
                move = random.choice(moves_white)
                make_move_board(board, move[0], move[1], WHITE)

        # Switch players
        current_player = WHITE if current_player == BLACK else BLACK

    # Count pieces to determine the outcome
    black_count = np.sum(board == BLACK)
    white_count = np.sum(board == WHITE)
    return black_count - white_count


def simulate_games_for_fitness(genes, num_games=10):
    """Run multiple games to get a more reliable fitness score."""
    total_reward = 0
    for _ in range(num_games):  # Fixed: syntax error with asterisks
        reward = simulate_game(genes)
        total_reward += reward
    return total_reward / num_games