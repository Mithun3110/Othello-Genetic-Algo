import numpy as np
import random

# Constants for piece values
BLACK = 1
WHITE = -1
EMPTY = 0

# Create an 8x8 matrix filled with zeros (empty spaces)
board = np.zeros((8, 8), dtype=int)

# Initialize center pieces as per Othello rules
board[3][3] = board[4][4] = WHITE
board[3][4] = board[4][3] = BLACK


def print_score():
    black_count = np.count_nonzero(board == BLACK)
    white_count = np.count_nonzero(board == WHITE)
    print(f"Score - Black: {black_count}, White: {white_count}")


def print_board():
    print("  1 2 3 4 5 6 7 8")
    for i in range(8):
        print(i + 1, end=" ")
        for j in range(8):
            if board[i][j] == BLACK:
                print("B", end=" ")
            elif board[i][j] == WHITE:
                print("W", end=" ")
            else:
                print(".", end=" ")
        print()
    print_score()
    print()


def is_valid_move(row, col, player):
    if row < 0 or row > 7 or col < 0 or col > 7 or board[row][col] != EMPTY:
        return False

    opponent = WHITE if player == BLACK else BLACK
    valid = False

    for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
        r, c = row + dr, col + dc
        if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
            while 0 <= r < 8 and 0 <= c < 8 and board[r][c] == opponent:
                r += dr
                c += dc
            if 0 <= r < 8 and 0 <= c < 8 and board[r][c] == player:
                valid = True
                break

    return valid


def make_move(row, col, player):
    if not is_valid_move(row, col, player):
        return False

    board[row][col] = player
    opponent = WHITE if player == BLACK else BLACK

    for dr, dc in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
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


def bot_moves(player):
    valid_moves = []
    for i in range(8):
        for j in range(8):
            if is_valid_move(i, j, player):
                valid_moves.append((i, j))

    if valid_moves:
        row, col = random.choice(valid_moves)
        make_move(row, col, player)
        print(f"Bot placed {'Black' if player == BLACK else 'White'} at ({row + 1}, {col + 1})")
    else:
        print(f"Bot ({'Black' if player == BLACK else 'White'}) has no valid moves")


def player_moves(player):
    color = "Black" if player == BLACK else "White"
    valid_moves = [(i + 1, j + 1) for i in range(8) for j in range(8) if is_valid_move(i, j, player)]

    if not valid_moves:
        print(f"No valid moves for {color}. Passing turn.")
        return False

    print(f"Your valid moves as {color}: {valid_moves}")
    while True:
        try:
            row = int(input(f"Enter row (1-8) for {color}: ")) - 1
            col = int(input(f"Enter column (1-8) for {color}: ")) - 1
            if (row + 1, col + 1) in valid_moves:
                make_move(row, col, player)
                return True
            else:
                print("Invalid move. Try again.")
        except ValueError:
            print("Please enter numbers between 1 and 8.")


def game_loop():
    current_player = BLACK
    print("Othello Game - Black (B) vs White (W)")
    print("Black moves first")
    print_board()

    while True:
        if current_player == BLACK:
            bot_moves(BLACK)
        else:
            player_moves(WHITE)

        print_board()

        # Check if game is over
        black_moves = any(is_valid_move(i, j, BLACK) for i in range(8) for j in range(8))
        white_moves = any(is_valid_move(i, j, WHITE) for i in range(8) for j in range(8))

        if not black_moves and not white_moves:
            print("Game Over!")
            black_count = np.count_nonzero(board == BLACK)
            white_count = np.count_nonzero(board == WHITE)
            if black_count > white_count:
                print("Black wins!")
            elif white_count > black_count:
                print("White wins!")
            else:
                print("It's a tie!")
            break

        if current_player == BLACK and not black_moves:
            print("Black has no valid moves. Passing to White.")
        elif current_player == WHITE and not white_moves:
            print("White has no valid moves. Passing to Black.")

        current_player = WHITE if current_player == BLACK else BLACK


# Start the game
game_loop()