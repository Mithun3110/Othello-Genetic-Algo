import random
from genes import Genes


def count_edges(board, player):
    count = 0
    size = len(board)
    # Check all four edges, excluding corners to not count them twice
    for i in range(1, size-1):
        if board[0][i] == player: count += 1  # Top edge
        if board[size-1][i] == player: count += 1  # Bottom edge
        if board[i][0] == player: count += 1  # Left edge
        if board[i][size-1] == player: count += 1  # Right edge
    # Corners are counted separately
    return count

def count_corners(board, player):
    size = len(board)
    return sum(1 for (i, j) in [(0, 0), (0, size-1), (size-1, 0), (size-1, size-1)] if board[i][j] == player)

def count_centres(board, player):
    count = 0
    size = len(board)
    # Assuming the centre is the middle 4x4 if the board is 8x8
    for i in range(size//2 - 2, size//2 + 2):
        for j in range(size//2 - 2, size//2 + 2):
            if board[i][j] == player:
                count += 1
    return count

def count_diagonals(board, player):
    count = 0
    size = len(board)
    for i in range(size):
        if board[i][i] == player:  # Main diagonal
            count += 1
        if board[i][size-1-i] == player:  # Anti-diagonal
            count += 1
    return count

def count_stability(board, player):  # Simplified example for stability
    # This is just a placeholder for whatever your definition of stability might be
    return sum(row.count(player) for row in board)  # Counting all player coins

def count_coin_difference(board, player):
    opponent = 'B' if player == 'W' else 'W'
    player_count = sum(row.count(player) for row in board)
    opponent_count = sum(row.count(opponent) for row in board)
    return player_count - opponent_count




def evaluate_fitness(genes, board, player):
    """
    Calculate the fitness based on the number of coins for each gene trait,
    multiplied by the respective gene weight.
    """
    feature_counts = {
        'edges': count_edges(board, player),
        'corners': count_corners(board, player),
        'centres': count_centres(board, player),
        'diagonals': count_diagonals(board, player),
        'stability': count_stability(board, player),
        'coin_difference': count_coin_difference(board, player)
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
    """
    Perform a simple crossover between two Genes objects by averaging each weight.
    """
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
    """
    Mutate gene weights with a given mutation rate and mutation strength.
    Each gene weight is adjusted by a small random amount if it meets the mutation probability.
    """
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
    """
    Run the genetic algorithm:
      - Initialize a population of 20 individuals with random genes.
      - Evaluate their fitness.
      - Keep the top 2 as elite.
      - For the remaining 18, split into two groups for crossover and mutation.
      - Repeat for a specified number of generations.
    """
    population_size = 20
    population = []

    # Mock initial board (standard Othello start)
    board = [
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', 'W', 'B', '.', '.', '.'],
        ['.', '.', '.', 'B', 'W', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.'],
        ['.', '.', '.', '.', '.', '.', '.', '.']
    ]
    player = 'B'  # Assume we are evaluating fitness for Black

    # Initialize population with random genes
    for _ in range(population_size):
        individual = Genes(0, 0, 0, 0, 0, 0)
        individual.create_random()
        population.append(individual)
    
    for generation in range(num_generations):
        # Evaluate fitness for each individual
        evaluated_population = [(ind, evaluate_fitness(ind, board, player)) for ind in population]
        # Sort by fitness (highest first)
        evaluated_population.sort(key=lambda x: x[1], reverse=True)
        
        # Display best fitness in this generation
        best_fitness = evaluated_population[0][1]
        print(f"Generation {generation}: Best Fitness = {best_fitness:.2f}")
        
        # Elitism: keep the top 2 individuals
        elite = [evaluated_population[0][0], evaluated_population[1][0]]
        
        # Remaining individuals are used for reproduction (18 individuals)
        reproduction_pool = [ind for ind, _ in evaluated_population[2:]]
        
        # Split reproduction pool into two groups
        mid_index = len(reproduction_pool) // 2
        group1 = reproduction_pool[:mid_index]
        group2 = reproduction_pool[mid_index:]
        
        # Create offspring by performing crossover and mutation on each pair
        offspring = []
        for parent1, parent2 in zip(group1, group2):
            child = crossover(parent1, parent2)
            mutate(child)
            offspring.append(child)
        
        # New population consists of elite individuals + offspring.
        population = elite + offspring
        
        # If the new population is smaller than 20, fill with new random individuals.
        while len(population) < population_size:
            new_ind = Genes(0, 0, 0, 0, 0, 0)
            new_ind.create_random()
            population.append(new_ind)
    
    return population



if __name__ == "__main__":
    final_population = genetic_algorithm(num_generations=50)

