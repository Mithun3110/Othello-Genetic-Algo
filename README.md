# Othello AI with Genetic Algorithm

This project implements an Othello (Reversi) game with an AI opponent that uses genetic algorithms to determine its moves. The AI evolves through simulated gameplay to discover effective strategies without being explicitly programmed with Othello tactics.

## Overview

Othello is a classic board game played on an 8×8 board where players (Black and White) take turns placing pieces with the goal of having the majority of pieces on the board at the end of the game. This implementation features:

- A playable Othello game with Pygame interface
- An AI opponent trained using genetic algorithms
- Full game rule implementation with valid move detection

## Files

- `deploy.py`: Main game file with Pygame UI and game loop
- `genes.py`: Defines the genetic representation of the AI
- `genetic_algo.py`: Contains the genetic algorithm implementation
- `validation.py`: Handles game rules and move validation
- `best_genes.pkl`: Saved weights from genetic algorithm training

## How to Play

1. Run `python deploy.py` to start the game
2. You play as White, the AI plays as Black
3. Click on a valid move location to place your piece
4. Valid moves will flip opponent pieces as per Othello rules
5. The game ends when neither player can make a move
6. The player with the most pieces wins

## AI Implementation

The AI uses a genetic algorithm that evaluates board positions based on several features:

- **Corners**: Control of corner positions (very valuable in Othello)
- **Edges**: Control of edge positions
- **Centers**: Control of center positions
- **Diagonals**: Control of diagonal positions
- **Stability**: How secure the pieces are
- **Piece Count**: Difference in the number of pieces

Each feature has a weight that determines its importance in the AI's decision-making. These weights evolve through the genetic algorithm process to optimize the AI's play.

## Genetic Algorithm Process

The training process (not run during gameplay) involves:

1. Creating a population of random gene sets (weights)
2. Evaluating each set by simulating multiple games
3. Selecting the best performers
4. Creating new gene sets through:
   - Crossover: Combining traits from successful "parents"
   - Mutation: Adding small random changes to maintain diversity
5. Repeating for multiple generations

The result is an AI that "evolves" to play Othello effectively.

## Requirements

- Python 3.6+
- NumPy
- Pygame
- Pickle (included in Python standard library)

## Installation

```bash
# Clone the repository


# Install dependencies
pip install numpy pygame