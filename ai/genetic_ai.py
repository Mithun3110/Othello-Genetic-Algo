from ai.genome import Genome
from ai.evaluator import Evaluator
import random
import copy

class GeneticAI:
    def __init__(self):
        self.population_size = 10
        self.population = [Genome() for _ in range(self.population_size)]
        self.evaluator = Evaluator()

    def select_move(self, board, color, genome=None):
        best_move = None
        best_score = float('-inf')
        genome = genome or self.population[0]

        for move in board.get_valid_moves(color):
            test_board = copy.deepcopy(board)
            test_board.place_coin(move[0], move[1], color)
            score = self.evaluator.evaluate(test_board, genome, color)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

    def evolve(self):
        self.population.sort(key=lambda g: g.fitness, reverse=True)
        parents = self.population[:2]

        new_population = [parents[0], parents[1]]
        while len(new_population) < self.population_size:
            p1, p2 = random.sample(parents, 2)
            child = Genome.empty()
            for key in child.genes:
                avg = (p1.genes[key] + p2.genes[key]) / 2
                mutation = random.uniform(-0.1, 0.1)
                child.genes[key] = max(-1.0, min(1.0), avg + mutation)
            new_population.append(child)

        self.population = new_population
