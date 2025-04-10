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