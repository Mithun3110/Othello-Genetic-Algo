import pygame
import time
from game.board import Board
from game.renderer import Renderer
from ai.genetic_ai import GeneticAI
from utils.constants import *

pygame.init()
screen = pygame.display.set_mode((480, 480))
pygame.display.set_caption("Othello: AI vs AI")

NUM_GENERATIONS = 5
GAMES_PER_GENERATION = 5

ai_white = GeneticAI()
ai_black = GeneticAI()

white_win_history = []
black_win_history = []

for generation in range(NUM_GENERATIONS):
    print(f"Generation {generation + 1}")
    white_wins = [0] * ai_white.population_size
    black_wins = [0] * ai_black.population_size

    for game_idx in range(GAMES_PER_GENERATION):
        board = Board()
        r = Renderer(screen)
        current_turn = BLACK

        while not board.is_full():
            screen.fill((0, 128, 0))
            r.draw_board(board)
            pygame.display.flip()

            valid_moves = board.get_valid_moves(current_turn)
            if valid_moves:
                if current_turn == BLACK:
                    move = ai_black.select_move(board, BLACK)
                else:
                    move = ai_white.select_move(board, WHITE)

                if move:
                    row, col = move
                    board.place_coin(row, col, current_turn)
                    screen.fill((0, 128, 0))
                    r.draw_board(board)
                    pygame.display.flip()
                    time.sleep(0.05)

            current_turn = -current_turn

        white_count, black_count = board.count_discs()
        print(f"Game {game_idx + 1}: WHITE={white_count} BLACK={black_count}")

        if white_count > black_count:
            white_wins[0] += 1
        elif black_count > white_count:
            black_wins[0] += 1

    ai_white.evolve(white_wins)
    ai_black.evolve(black_wins)

    white_win_history.append(white_wins[0])
    black_win_history.append(black_wins[0])

    print(f"White wins: {white_wins[0]}, Black wins: {black_wins[0]}\n")

# Show evolution log
print("=== Evolution Progress ===")
for gen in range(NUM_GENERATIONS):
    print(f"Gen {gen + 1}: White Wins = {white_win_history[gen]}, Black Wins = {black_win_history[gen]}")

# Play a final visual game between best evolved AIs
print("Training complete. Playing final visual game...")

final_board = Board()
r = Renderer(screen)
final_turn = BLACK

while not final_board.is_full():
    screen.fill((0, 128, 0))
    r.draw_board(final_board)
    pygame.display.flip()
    time.sleep(0.3)

    valid_moves = final_board.get_valid_moves(final_turn)
    if valid_moves:
        if final_turn == BLACK:
            move = ai_black.select_move(final_board, BLACK)
        else:
            move = ai_white.select_move(final_board, WHITE)

        if move:
            final_board.place_coin(move[0], move[1], final_turn)

    final_turn = -final_turn

# Final score display
white_final, black_final = final_board.count_discs()
print(f"\n=== Final Game Score ===")
print(f"WHITE: {white_final}, BLACK: {black_final}")
time.sleep(3)
pygame.quit()
