import pygame
from utils.constants import *

class Renderer:
    def __init__(self, screen):
        self.screen = screen
        self.cell_size = 60
        self.font = pygame.font.SysFont(None, 28)

    def draw_board(self, board):
        self.screen.fill((0, 128, 0))
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                pygame.draw.rect(self.screen, (0, 100, 0), (c*self.cell_size, r*self.cell_size, self.cell_size, self.cell_size), 1)
                if board.grid[r][c] == BLACK:
                    pygame.draw.circle(self.screen, (0,0,0), (c*self.cell_size+30, r*self.cell_size+30), 25)
                elif board.grid[r][c] == WHITE:
                    pygame.draw.circle(self.screen, (255,255,255), (c*self.cell_size+30, r*self.cell_size+30), 25)

    def display_message(self, message):
        text = self.font.render(message, True, (255, 255, 255))
        self.screen.blit(text, (10, 10))