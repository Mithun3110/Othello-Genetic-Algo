# Othello-Genetic-Algo

Algoritm
    - Board.py {Dsiplaying the base board and update it for every move}
    - validation.py {Checking for invalid moves and calculating rewards }
    - Moves.py { listing functions of all possible moves}
    - Genetic_algorhtm.py { Where the main algo goes with mutation}

Backend
    - Flask

Frontend 
    - HTML
    - CSS


RUELS
    - Adjacent cell where it can flip must be white
    - Every move must be alternate
    - If a player has no moves the turn is passed to the next player
    - The game ends when the whole board is filled or when one player has exhausted all their coins.
    - Each player has 30 coins each.
    - Totaly 64 coins where there are 4 on the board 2 white and 2 black
        D4 (White) | E4 (Black)
        D5 (Black) | E5 (White)
