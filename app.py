from flask import Flask, render_template, request, jsonify
from deploy import init_board, game_over, get_winner
from validation import get_valid_moves, is_valid_move_board, make_move_board
from genetic_algo import gene_agent_move
from constants import WHITE, BLACK
import pickle
import numpy as np
import time


app = Flask(__name__)

# Load best genes
try:
    with open("best_genes.pkl", "rb") as f:
        best_genes = pickle.load(f)
    print("Loaded best genes.")
except Exception as e:
    print("Could not load genes:", e)
    best_genes = None

# Global game state
board = init_board()
current_turn = WHITE  # Human plays white

@app.route('/')
def index():
    valid = get_valid_moves(board, current_turn)
    return render_template('index.html',
                           board=board.tolist(),
                           turn=current_turn,
                           valid_moves=[[i, j] for (i, j) in valid])

@app.route('/move', methods=['POST'])
def move():
    global board, current_turn

    data = request.get_json()
    row, col = int(data['row']), int(data['col'])
    

    if current_turn == WHITE and is_valid_move_board(board, row, col, WHITE):
        make_move_board(board, row, col, WHITE)
        current_turn = BLACK

        # AI move
        if not game_over(board):
            moves = get_valid_moves(board, BLACK)
            if moves:
                ai_move = gene_agent_move(best_genes, board, BLACK)
                if ai_move:
                    make_move_board(board, ai_move[0], ai_move[1], BLACK)
            current_turn = WHITE

    result = {
        "board": board.tolist(),
        "turn": current_turn,
        "game_over": game_over(board),
        "winner": get_winner(board) if game_over(board) else None
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
