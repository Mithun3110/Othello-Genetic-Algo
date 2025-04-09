from utils.constants import *

DIRECTIONS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1),  (1, 0), (1, 1)
]

class Board:
    def __init__(self):
        self.grid = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.grid[3][3], self.grid[3][4] = WHITE, BLACK
        self.grid[4][3], self.grid[4][4] = BLACK, WHITE

    def is_on_board(self, r, c):
        return 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE

    def is_valid_move(self, row, col, color):
        if self.grid[row][col] != EMPTY:
            return False
        opp_color = -color
        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            if self.is_on_board(r, c) and self.grid[r][c] == opp_color:
                while self.is_on_board(r, c) and self.grid[r][c] == opp_color:
                    r += dr
                    c += dc
                if self.is_on_board(r, c) and self.grid[r][c] == color:
                    return True
        return False

    def place_coin(self, row, col, color):
        opp_color = -color
        to_flip = []
        for dr, dc in DIRECTIONS:
            r, c = row + dr, col + dc
            if not self.is_on_board(r, c) or self.grid[r][c] != opp_color:
                continue
            line = []
            while self.is_on_board(r, c) and self.grid[r][c] == opp_color:
                line.append((r, c))
                r += dr
                c += dc
            if self.is_on_board(r, c) and self.grid[r][c] == color:
                to_flip.extend(line)
        if to_flip:
            self.grid[row][col] = color
            for r, c in to_flip:
                self.grid[r][c] = color
            return True
        return False

    def get_valid_moves(self, color):
        return [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.is_valid_move(r, c, color)]

    def is_full(self):
        return all(cell != EMPTY for row in self.grid for cell in row)

    def count_discs(self):
        white = sum(cell == WHITE for row in self.grid for cell in row)
        black = sum(cell == BLACK for row in self.grid for cell in row)
        return white, black