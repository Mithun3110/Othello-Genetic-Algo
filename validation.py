import numpy as np
import random
from fitness_function import *

# Constants for piece values
BLACK = 1
WHITE = -1
EMPTY = 0

def board_to_char(board):
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
    if row < 0 or row > 7 or col < 0 or col > 7 or board[row][col] != EMPTY:
        return False
    opponent = WHITE if player == BLACK else BLACK
    valid = False
    for dr, dc in [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),          (0, 1),
                   (1, -1),  (1, 0),  (1, 1)]:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                valid = True
                break
    return valid

def make_move_board(board, row, col, player):
    if not is_valid_move_board(board, row, col, player):
        return False
    board[row][col] = player
    opponent = WHITE if player == BLACK else BLACK
    for dr, dc in [(-1, -1), (-1, 0), (-1, 1),
                   (0, -1),          (0, 1),
                   (1, -1),  (1, 0),  (1, 1)]:
        r, c = row + dr, col + dc
        to_flip = []
        while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            to_flip.append((r, c))
            r += dr
            c += dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
            for (fr, fc) in to_flip:
                board[fr][fc] = player
    return True


def get_valid_moves(board, player):
    moves = []
    for i in range(8):
        for j in range(8):
            if is_valid_move_board(board, i, j, player):
                moves.append((i, j))
    return moves


def gene_agent_move(genes, board, player):
    moves = get_valid_moves(board, player)
    if not moves:
        return None

    best_move = None
    best_score = -float('inf')

    for move in moves:
        board_copy = board.copy()
        make_move_board(board_copy, move[0], move[1], player)
        char_board = board_to_char(board_copy)
        score = evaluate_fitness(genes, char_board, 'B')
        if score > best_score:
            best_score = score
            best_move = move

    return best_move


def simulate_game(genes):
    board = np.zeros((8, 8), dtype=int)
    board[3, 3] = board[4, 4] = WHITE
    board[3, 4] = board[4, 3] = BLACK
    current_player = BLACK

    while True:
        moves_black = get_valid_moves(board, BLACK)
        moves_white = get_valid_moves(board, WHITE)

        if not moves_black and not moves_white:
            break

        if current_player == BLACK:
            if moves_black:
                move = gene_agent_move(genes, board, BLACK)
                if move is None:
                    current_player = WHITE
                    continue
                make_move_board(board, move[0], move[1], BLACK)
        else:
            if moves_white:
                move = random.choice(moves_white)
                make_move_board(board, move[0], move[1], WHITE)

        current_player = WHITE if current_player == BLACK else BLACK

    black_count = (board == BLACK).sum()
    white_count = (board == WHITE).sum()
    return black_count - white_count

def simulate_games_for_fitness(genes, num_games=10):
    total_reward = 0
    for _ in range(num_games):
        reward = simulate_game(genes)
        total_reward += reward
    return total_reward / num_games