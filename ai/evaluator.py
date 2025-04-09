from utils.constants import *

class Evaluator:
    def evaluate(self, board, genome, color):
        score = 0
        opp_color = -color
        my_count, opp_count = 0, 0
        my_stable, opp_stable = 0, 0

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                val = board.grid[r][c]
                if val == color:
                    my_count += 1

                    # Corners
                    if (r, c) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                        score += genome.genes["corners"]
                    # Edges
                    elif r in [0, 7] or c in [0, 7]:
                        score += genome.genes["edges"]
                    # Centres (non-edge, non-corner)
                    elif 2 <= r <= 5 and 2 <= c <= 5:
                        score += genome.genes["centres"]
                    # Diagonals
                    if r == c or r + c == BOARD_SIZE - 1:
                        score += genome.genes["diagonals"]
                    # Stability (very basic heuristic — corner pieces are stable)
                    if (r, c) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                        my_stable += 1

                elif val == opp_color:
                    opp_count += 1
                    if (r, c) in [(0, 0), (0, 7), (7, 0), (7, 7)]:
                        opp_stable += 1

        score += genome.genes["coin_diff"] * (my_count - opp_count)
        score += genome.genes["stability"] * (my_stable - opp_stable)

        return score
    
