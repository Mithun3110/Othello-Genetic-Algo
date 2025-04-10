import numpy as np
import random
import pickle
from genes import Genes
from validation import *

BLACK = 1
WHITE = -1
EMPTY = 0

def evaluate_fitness(genes, board, player):
    def count_edges(board, player_char):
        count = 0
        size = len(board)
        for i in range(1, size - 1):
            if board[0][i] == player_char: count += 1
            if board[size - 1][i] == player_char: count += 1
            if board[i][0] == player_char: count += 1
            if board[i][size - 1] == player_char: count += 1
        return count

    def count_corners(board, player_char):
        size = len(board)
        return sum(1 for (i, j) in [(0, 0), (0, size - 1), (size - 1, 0), (size - 1, size - 1)]
                   if board[i][j] == player_char)

    def count_centres(board, player_char):
        count = 0
        size = len(board)
        for i in range(size // 2 - 2, size // 2 + 2):
            for j in range(size // 2 - 2, size // 2 + 2):
                if board[i][j] == player_char:
                    count += 1
        return count

    def count_diagonals(board, player_char):
        count = 0
        size = len(board)
        for i in range(size):
            if board[i][i] == player_char: count += 1
            if board[i][size - 1 - i] == player_char: count += 1
        return count

    def count_stability(board, player_char):
        return sum(row.count(player_char) for row in board)

    def count_coin_difference(board, player_char):
        opponent_char = 'B' if player_char == 'W' else 'W'
        player_count = sum(row.count(player_char) for row in board)
        opponent_count = sum(row.count(opponent_char) for row in board)
        return player_count - opponent_count

    feature_counts = {
        'edges': count_edges(board, 'B'),
        'corners': count_corners(board, 'B'),
        'centres': count_centres(board, 'B'),
        'diagonals': count_diagonals(board, 'B'),
        'stability': count_stability(board, 'B'),
        'coin_difference': count_coin_difference(board, 'B')
    }
    fitness = (
        genes.edges_w * feature_counts['edges'] +
        genes.corners_w * feature_counts['corners'] +
        genes.centres_w * feature_counts['centres'] +
        genes.diagonals_w * feature_counts['diagonals'] +
        genes.stability_w * feature_counts['stability'] +
        genes.coin_diff_w * feature_counts['coin_difference']
    )
    return fitness

def crossover(parent1, parent2):
    child = Genes(
        (parent1.edges_w + parent2.edges_w) / 2,
        (parent1.corners_w + parent2.corners_w) / 2,
        (parent1.centres_w + parent2.centres_w) / 2,
        (parent1.diagonals_w + parent2.diagonals_w) / 2,
        (parent1.stability_w + parent2.stability_w) / 2,
        (parent1.coin_diff_w + parent2.coin_diff_w) / 2
    )
    return child

def mutate(genes, mutation_rate=0.3, mutation_strength=0.1):
    if random.random() < mutation_rate:
        genes.edges_w += random.uniform(-mutation_strength, mutation_strength)
    if random.random() < mutation_rate:
        genes.corners_w += random.uniform(-mutation_strength, mutation_strength)
    if random.random() < mutation_rate:
        genes.centres_w += random.uniform(-mutation_strength, mutation_strength)
    if random.random() < mutation_rate:
        genes.diagonals_w += random.uniform(-mutation_strength, mutation_strength)
    if random.random() < mutation_rate:
        genes.stability_w += random.uniform(-mutation_strength, mutation_strength)
    if random.random() < mutation_rate:
        genes.coin_diff_w += random.uniform(-mutation_strength, mutation_strength)


def genetic_algorithm(num_generations=50):
    population_size = 20
    population = []

    
    for _ in range(population_size):
        individual = Genes(0, 0, 0, 0, 0, 0)
        individual.create_random()
        population.append(individual)

    for generation in range(num_generations):
        evaluated_population = [(ind, simulate_games_for_fitness(ind, num_games=5)) for ind in population]
        evaluated_population.sort(key=lambda x: x[1], reverse=True)
        best_fitness = evaluated_population[0][1]
        print(f"Generation {generation}: Best Fitness = {best_fitness}")
        elite = [evaluated_population[0][0], evaluated_population[1][0]]
        reproduction_pool = [ind for ind, _ in evaluated_population[2:]]
        mid_index = len(reproduction_pool) // 2
        group1 = reproduction_pool[:mid_index]
        group2 = reproduction_pool[mid_index:]
        offspring = []
        for parent1, parent2 in zip(group1, group2):
            child = crossover(parent1, parent2)
            mutate(child)
            offspring.append(child)

        population = elite + offspring
        while len(population) < population_size:
            new_ind = Genes(0, 0, 0, 0, 0, 0)
            new_ind.create_random()
            population.append(new_ind)

    return population

if __name__ == "__main__":
    final_population = genetic_algorithm(50)
    best_genes = final_population[0]
    final_reward = simulate_game(best_genes)
    print("Final game result (coin difference, Black - White):", final_reward)

    with open("best_genes.pkl", "wb") as f:
        pickle.dump(best_genes, f)
    print("Best genes saved to best_genes.pkl.")
