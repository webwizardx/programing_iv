# Tic Tac Toe Game with Minimax Algorithm

This is a Python implementation of the classic tic tac toe game, featuring an unbeatable AI player that uses the minimax algorithm to determine the best possible move.

## How to Play

    1. Clone the repository to your local machine.
    2. Open your terminal and navigate to this folder.
    3. Run python main.py to start the game.
    4. Have fun :D!

## How it Works

### Game Board

The game board is represented as a 3x3 matrix, with each cell being one of three possible values: 'X', 'O', or an empty space ' '.
Minimax Algorithm

The minimax algorithm is used to determine the best possible move for the AI player. The algorithm works by recursively exploring all possible game states from the current state, assigning a score to each state, and choosing the move that leads to the highest score for the AI player and the lowest score for the human player.
Alpha-Beta Pruning

In order to speed up the minimax algorithm, alpha-beta pruning is implemented to reduce the number of unnecessary game states explored. Alpha-beta pruning works by discarding game states that are guaranteed to be worse than previously explored states.

