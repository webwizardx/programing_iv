"""A tic-tac-toe game built with Python and Tkinter."""
from itertools import cycle
import tkinter as tk
from tkinter import font
from typing import List, NamedTuple


class Player(NamedTuple):
    label: str
    color: str
    score: int
    is_human: bool = True


class Move(NamedTuple):
    row: int
    col: int
    label: str = ""


BOARD_SIZE = 3


class TicTacToeGame:
    def __init__(self, board_size=BOARD_SIZE, is_debug=False, is_human=True):
        self.score_table = {}
        self._default_players = (Player(label="X", color="blue", score=-10),
                                 Player(label="O", color="green", score=10, is_human=False))
        self.board_size = board_size
        self.winner_combo = []
        self._current_moves = []
        self._has_winner = False
        self._winning_combos = []
        self._is_debug = is_debug
        self.set_players(is_human=is_human)
        self._setup_board()
        self._setup_score_table(self._default_players)

    def set_players(self, is_human=True):
        if is_human:
            self._players = cycle(self._default_players)
            self.current_player = next(self._players)
        else:
            self._players = cycle(self._default_players[::-1])
            self.current_player = next(self._players)

    def _setup_board(self):
        self._current_moves = [
            [Move(row, col) for col in range(self.board_size)]
            for row in range(self.board_size)
        ]
        self._winning_combos = self._get_winning_combos()

    def _setup_score_table(self, players: List[Player]):
        self.score_table = {player.label: player.score for player in players}

    def _get_winning_combos(self):
        rows = [
            [(move.row, move.col) for move in row]
            for row in self._current_moves
        ]
        columns = [list(col) for col in zip(*rows)]
        first_diagonal = [row[i] for i, row in enumerate(rows)]
        second_diagonal = [col[j] for j, col in enumerate(reversed(columns))]
        return rows + columns + [first_diagonal, second_diagonal]

    def is_valid_move(self, move: Move):
        """Return True if move is valid, and False otherwise."""
        row, col = move.row, move.col
        move_was_not_played = self._current_moves[row][col].label == ""
        no_winner = not self._has_winner
        return no_winner and move_was_not_played

    def process_move(self, move: Move):
        """Process the current move and check if it's a win."""
        row, col = move.row, move.col
        self._current_moves[row][col] = move
        combo = self._check_winning()
        if combo:
            self._has_winner = True
            self.winner_combo = combo

    def _process_computer_move(self):
        bestScore = float('-inf')
        bestMove = None
        for row in self._current_moves:
            for move in row:
                if move.label == '':
                    self._current_moves[move.row][move.col] = Move(
                        move.row, move.col, 'O')
                    self.logger(f'PARENT -> x: {move.row}, y: {move.col}')
                    score = self._minimax()
                    self._current_moves[move.row][move.col] = Move(
                        move.row, move.col, '')
                    if score > bestScore:
                        bestScore = score
                        bestMove = move

        self._current_moves[bestMove.row][bestMove.col] = Move(
            bestMove.row, bestMove.col, 'O')
        combo = self._check_winning()
        if combo:
            self._has_winner = True
            self.winner_combo = combo
        return bestMove

    def _minimax(self, depth=0, alpha=float('-inf'), beta=float('inf'), is_maximizing=False):
        if self._check_winning(self._current_moves):
            if is_maximizing:
                temp = self.score_table['X'] + depth
                self.logger(
                    f'Depth: {depth}, score: {temp}, isMaximizing: {is_maximizing}')
                return self.score_table['X'] + depth
            else:
                temp = self.score_table['O'] - depth
                self.logger(
                    f'Depth: {depth}, score: {temp}, isMaximizing: {is_maximizing}')
                return self.score_table['O'] - depth
        elif self.is_tied(self._current_moves):
            self.logger(
                f'Depth: {depth}, score: {0}, Tied')
            return 0
        depth += 1

        if is_maximizing:
            bestScore = float('-inf')
            for row in self._current_moves:
                for move in row:
                    if move.label == '':
                        self._current_moves[move.row][move.col] = Move(
                            move.row, move.col, 'O')
                        self.logger(
                            f'IS_MAXIMAZING -> x: {move.row}, y: {move.col}')
                        score = self._minimax(depth, alpha, beta, False)
                        self._current_moves[move.row][move.col] = Move(
                            move.row, move.col, '')
                        bestScore = max(score, bestScore)
                        alpha = max(alpha, score)
                        if beta <= alpha:
                            return bestScore
            return bestScore
        else:
            bestScore = float('inf')
            for row in self._current_moves:
                for move in row:
                    if move.label == '':
                        self._current_moves[move.row][move.col] = Move(
                            move.row, move.col, 'X')
                        self.logger(
                            f'NOT_IS_MAXIMAZING -> x: {move.row}, y: {move.col}')
                        score = self._minimax(depth, alpha, beta, True)
                        self._current_moves[move.row][move.col] = Move(
                            move.row, move.col, '')
                        bestScore = min(score, bestScore)
                        beta = min(beta, score)
                        if beta <= alpha:
                            return bestScore
            return bestScore

    def has_winner(self):
        """Return True if the game has a winner, and False otherwise."""
        return self._has_winner

    def is_tied(self, current_moves: List[List[Move]] = None):
        """Return True if the game is tied, and False otherwise."""
        no_winner = not self._has_winner
        current_moves = current_moves or self._current_moves
        played_moves = (
            move.label for row in current_moves for move in row
        )
        return no_winner and all(played_moves)

    def _check_winning(self, current_moves: List[List[Move]] = None):
        current_moves = current_moves or self._current_moves
        for combo in self._winning_combos:
            results = set(current_moves[n][m].label for n, m in combo)
            is_win = (len(results) == 1) and ("" not in results)
            if is_win:
                return combo
        return

    def toggle_player(self):
        """Return a toggled player."""
        self.current_player = next(self._players)

    def reset_game(self):
        """Reset the game state to play again."""
        for row, row_content in enumerate(self._current_moves):
            for col, _ in enumerate(row_content):
                row_content[col] = Move(row, col)
        self._has_winner = False
        self.winner_combo = []

    def new_game_player(self):
        self.set_players()
        self.reset_game()

    def new_game_computer(self):
        self.set_players(is_human=False)
        self.reset_game()

    def logger(self, data):
        if self._is_debug:
            print(data)


class TicTacToeBoard(tk.Tk):
    def __init__(self, game: TicTacToeGame):
        super().__init__()
        self.title("Tic-Tac-Toe Game")
        self._cells = {}
        self._inverted_cells = {}
        self._game = game
        self._create_menu()
        self._create_board_display()
        self._create_board_grid()

    def _create_menu(self):
        menu_bar = tk.Menu(master=self)
        self.config(menu=menu_bar)
        file_menu = tk.Menu(master=menu_bar)
        file_menu.add_command(label="New Game (Human first)",
                              command=lambda: self.reset_board(True))
        file_menu.add_separator()
        file_menu.add_command(
            label="New Game (Computer first)", command=lambda: self.reset_board(False))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=quit)
        menu_bar.add_cascade(label="File", menu=file_menu)

    def _create_board_display(self):
        display_frame = tk.Frame(master=self)
        display_frame.pack(fill=tk.X)
        self.display = tk.Label(
            master=display_frame,
            text="Ready?",
            font=font.Font(size=28, weight="bold"),
        )
        self.display.pack()

    def _create_board_grid(self):
        grid_frame = tk.Frame(master=self)
        grid_frame.pack()
        for row in range(self._game.board_size):
            self.rowconfigure(row, weight=1, minsize=50)
            self.columnconfigure(row, weight=1, minsize=75)
            for col in range(self._game.board_size):
                button = tk.Button(
                    master=grid_frame,
                    text="",
                    font=font.Font(size=36, weight="bold"),
                    fg="black",
                    width=3,
                    height=2,
                    highlightbackground="lightblue",
                )
                position = (row, col)
                self._cells[button] = position
                self._inverted_cells[position] = button
                button.bind("<ButtonPress-1>", self.play)
                button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")

    def play(self, event):
        """Handle a player's move."""
        clicked_btn = event.widget
        row, col = self._cells[clicked_btn]
        move = Move(row, col, self._game.current_player.label)
        if self._game.is_valid_move(move):
            self._update_button(clicked_btn)
            self._game.process_move(move)
            if self._game.is_tied():
                self._update_display(msg="Tied game!", color="red")
            elif self._game.has_winner():
                self._highlight_cells()
                msg = f'Player "{self._game.current_player.label}" won!'
                color = self._game.current_player.color
                self._update_display(msg, color)
            else:
                self._game.toggle_player()
                msg = f"{self._game.current_player.label}'s turn"
                self._update_display(msg)
                if not self._game.current_player.is_human:
                    self._computer_play()

    def _computer_play(self):
        move = self._game._process_computer_move()
        button = self._inverted_cells[(move.row, move.col)]
        self._update_button(button)
        if self._game.is_tied():
            self._update_display(msg="Tied game!", color="red")
        elif self._game.has_winner():
            self._highlight_cells()
            msg = f'Player "{self._game.current_player.label}" won!'
            color = self._game.current_player.color
            self._update_display(msg, color)
        else:
            self._game.toggle_player()
            msg = f"{self._game.current_player.label}'s turn"
            self._update_display(msg)

    def _update_button(self, clicked_btn, label: str = None, color: str = None):
        label = label or self._game.current_player.label
        color = color or self._game.current_player.color
        clicked_btn.config(text=label)
        clicked_btn.config(fg=color)

    def _update_display(self, msg, color="black"):
        self.display["text"] = msg
        self.display["fg"] = color

    def _highlight_cells(self):
        for button, coordinates in self._cells.items():
            if coordinates in self._game.winner_combo:
                button.config(highlightbackground="red")

    def reset_board(self, is_human: bool):
        """Reset the game's board to play again."""
        if is_human:
            self._game.new_game_player()
        else:
            self._game.new_game_computer()
        self._update_display(msg="Ready?")
        for button in self._cells.keys():
            button.config(highlightbackground="lightblue")
            button.config(text="")
            button.config(fg="black")
        if not self._game.current_player.is_human:
            self._computer_play()

    def set_test_board(self):
        colors = {
            'O': 'green',
            'X': 'blue'
        }
        """ board = [
            [Move(0, 0, ''), Move(0, 1, 'X'), Move(0, 2, '')],
            [Move(1, 0, ''), Move(1, 1, ''), Move(1, 2, 'X')],
            [Move(2, 0, 'O'), Move(2, 1, 'O'), Move(2, 2, 'X')]
        ] """
        """ board = [
            [Move(0, 0, 'O'), Move(0, 1, 'O'), Move(0, 2, 'X')],
            [Move(1, 0, 'X'), Move(1, 1, ''), Move(1, 2, '')],
            [Move(2, 0, ''), Move(2, 1, 'O'), Move(2, 2, 'X')]
        ] """
        board = [
            [Move(0, 0, 'X'), Move(0, 1, 'O'), Move(0, 2, 'X')],
            [Move(1, 0, ''), Move(1, 1, 'O'), Move(1, 2, '')],
            [Move(2, 0, 'O'), Move(2, 1, 'X'), Move(2, 2, 'X')]
        ]
        self._game._current_moves = board
        for row in range(self._game.board_size):
            for move in board[row]:
                if move.label != '':
                    button = self._inverted_cells[(move.row, move.col)]
                    self._update_button(
                        button, label=move.label, color=colors[move.label])
        if not self._game.current_player.is_human:
            self._computer_play()


def main():
    """Create the game's board and run its main loop."""
    game = TicTacToeGame()
    board = TicTacToeBoard(game)
    board.mainloop()


if __name__ == "__main__":
    main()
