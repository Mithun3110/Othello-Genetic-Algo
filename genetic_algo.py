import numpy as np
import random
import pickle
from genes import Genes
from validation import *
from fitness_function import *

BLACK = 1
WHITE = -1
EMPTY = 0



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
