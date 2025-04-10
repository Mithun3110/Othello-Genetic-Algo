import sys
import time
import numpy as np
import random
import pygame
import pickle

from genes import Genes
from genetic_algo import *
from validation import *

BLACK = 1    
WHITE = -1
EMPTY = 0


try:
    with open("best_genes.pkl", "rb") as f:
        best_genes = pickle.load(f)
    print("Loaded best genes from best_genes.pkl.")
except Exception as e:
    print("Error loading best genes:", e)
    sys.exit(1)


# ---------------------- Pygame Setup ---------------------- #
pygame.init()

# Board dimensions
ROWS, COLS = 8, 8
CELL_SIZE = 60
MARGIN = 20
WIDTH = COLS * CELL_SIZE + 2 * MARGIN
HEIGHT = ROWS * CELL_SIZE + 2 * MARGIN

# Colors
GREEN = (34, 139, 34)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
GRAY = (128, 128, 128)
BACKGROUND_COLOR = (0, 100, 0)

# Create the display window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Othello - Human (White) vs AI (Black)")

# Font for messages
font = pygame.font.SysFont(None, 36)

# ---------------------- Board Initialization ---------------------- #
def init_board():
    board = np.zeros((8, 8), dtype=int)
    # Standard Othello starting pieces
    board[3, 3] = board[4, 4] = WHITE
    board[3, 4] = board[4, 3] = BLACK
    return board

board = init_board()

# ---------------------- Drawing Functions ---------------------- #
def draw_board(screen, board):
    screen.fill(BACKGROUND_COLOR)
    
    # Draw grid background (green felt)
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(MARGIN + col * CELL_SIZE,
                               MARGIN + row * CELL_SIZE,
                               CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREEN, rect)
            pygame.draw.rect(screen, BLACK_COLOR, rect, 2)
    
    # Draw pieces
    for row in range(ROWS):
        for col in range(COLS):
            center = (MARGIN + col * CELL_SIZE + CELL_SIZE // 2,
                      MARGIN + row * CELL_SIZE + CELL_SIZE // 2)
            radius = CELL_SIZE // 2 - 4
            if board[row, col] == BLACK:
                pygame.draw.circle(screen, BLACK_COLOR, center, radius)
            elif board[row, col] == WHITE:
                pygame.draw.circle(screen, WHITE_COLOR, center, radius)
    pygame.display.flip()

def draw_message(text):
    # Render a message at the bottom of the window
    message = font.render(text, True, GRAY, BACKGROUND_COLOR)
    message_rect = message.get_rect(center=(WIDTH//2, HEIGHT - MARGIN//2))
    screen.blit(message, message_rect)
    pygame.display.flip()

# ---------------------- Game Over Check ---------------------- #
def game_over(board):
    moves_black = get_valid_moves(board, BLACK)
    moves_white = get_valid_moves(board, WHITE)
    return (not moves_black) and (not moves_white)

def get_winner(board):
    black_count = (board == BLACK).sum()
    white_count = (board == WHITE).sum()
    if black_count > white_count:
        return "Black (AI)"
    elif white_count > black_count:
        return "White (You)"
    else:
        return "Tie"

# ---------------------- Main Game Loop ---------------------- #
def main():
    clock = pygame.time.Clock()
    user_turn = True  # Human plays as White; AI plays as Black.
    running = True

    while running:
        draw_board(screen, board)
        
        if game_over(board):
            winner = get_winner(board)
            draw_message(f"Game Over! Winner: {winner}")
            # Pause for 5 seconds and exit
            pygame.display.flip()
            time.sleep(5)
            running = False
            continue
        
        if user_turn:
            draw_message("Your Turn (White)")
            # Wait for mouse click from user for a valid move.
            move_made = False
            while not move_made and running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        break
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_x, mouse_y = event.pos
                        # Determine board coordinates
                        col = (mouse_x - MARGIN) // CELL_SIZE
                        row = (mouse_y - MARGIN) // CELL_SIZE
                        if 0 <= row < ROWS and 0 <= col < COLS:
                            if is_valid_move_board(board, row, col, WHITE):
                                make_move_board(board, row, col, WHITE)
                                move_made = True
                                user_turn = False
                                break
                clock.tick(30)
        else:
            draw_message("AI's Turn (Black)")
            pygame.display.flip()
            # Brief pause to simulate thinking
            time.sleep(1)
            moves = get_valid_moves(board, BLACK)
            if moves:
                move = gene_agent_move(best_genes, board, BLACK)
                if move is not None:
                    make_move_board(board, move[0], move[1], BLACK)
            user_turn = True

        # Process quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        clock.tick(30)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
