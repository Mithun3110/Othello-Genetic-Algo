from utils.constants import *

class GameState:
    def __init__(self, board):
        self.board = board
        self.current_turn = BLACK
        self.coins = {BLACK: 30, WHITE: 30}

    def switch_turn(self):
        self.current_turn = WHITE if self.current_turn == BLACK else BLACK

    def has_moves(self, color):
        return bool(self.board.get_valid_moves(color))

    def is_game_over(self):
        return self.board.is_full() or self.coins[WHITE] == 0 or self.coins[BLACK] == 0