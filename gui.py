"""Tkinter GUI for the Tic-Tac-Toe AI project.

Run this file with: python gui.py
The existing console game remains available through main.py.
"""

import tkinter as tk
from contextlib import redirect_stdout
from io import StringIO
from tkinter import messagebox, ttk

from main import (
    check_winner,
    computer_move_easy,
    computer_move_medium,
    computer_move_hard,
)


class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe AI")
        self.root.configure(bg="#f3f5f9")
        self.root.resizable(False, False)

        self.mode_var = tk.StringVar(value="Player vs Computer")
        self.difficulty_var = tk.StringVar(value="Hard")
        self.player_x_var = tk.StringVar(value="Player X")
        self.player_o_var = tk.StringVar(value="Computer")

        self.player_names = {"X": "Player X", "O": "Computer"}
        self.scores = {"X": 0, "O": 0, "draws": 0}
        self.board = self.empty_board()
        self.check = set()
        self.current_player = "X"
        self.game_over = False
        self.ai_job = None
        self.board_buttons = []

        self.configure_styles()
        self.build_ui()
        self.on_mode_change()
        self.start_new_session(show_message=False)

    @staticmethod
    def empty_board():
        return [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background="#f3f5f9")
        style.configure(
            "TLabelframe",
            background="#f3f5f9",
            bordercolor="#d7deea",
        )
        style.configure(
            "TLabelframe.Label",
            background="#f3f5f9",
            foreground="#263247",
            font=("Segoe UI", 10, "bold"),
        )
        style.configure(
            "TLabel",
            background="#f3f5f9",
            foreground="#263247",
            font=("Segoe UI", 10),
        )
        style.configure("Title.TLabel", font=("Segoe UI", 23, "bold"), foreground="#17243b")
        style.configure("Subtitle.TLabel", font=("Segoe UI", 10), foreground="#667085")
        style.configure("Status.TLabel", font=("Segoe UI", 11, "bold"), foreground="#2456a6")
        style.configure("Winner.TLabel", font=("Segoe UI", 11, "bold"), foreground="#16804a")
        style.configure("Score.TLabel", font=("Segoe UI", 10, "bold"), foreground="#263247")
        style.configure("TButton", font=("Segoe UI", 10), padding=(10, 7))

    def build_ui(self):
        outer = ttk.Frame(self.root, padding=(22, 18, 22, 20))
        outer.grid(row=0, column=0)

        ttk.Label(outer, text="TIC-TAC-TOE AI", style="Title.TLabel").grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(
            outer,
            text="Play a friend or challenge the computer.",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(2, 14))

        setup = ttk.LabelFrame(outer, text="Game setup", padding=12)
        setup.grid(row=2, column=0, sticky="ew", pady=(0, 14))
        setup.columnconfigure(1, weight=1)
        setup.columnconfigure(3, weight=1)

        ttk.Label(setup, text="Game mode").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=5)
        self.mode_combo = ttk.Combobox(
            setup,
            textvariable=self.mode_var,
            values=("Player vs Player", "Player vs Computer"),
            state="readonly",
            width=20,
        )
        self.mode_combo.grid(row=0, column=1, sticky="ew", padx=(0, 12), pady=5)
        self.mode_combo.bind("<<ComboboxSelected>>", self.on_mode_change)

        ttk.Label(setup, text="Difficulty").grid(row=0, column=2, sticky="w", padx=(0, 8), pady=5)
        self.difficulty_combo = ttk.Combobox(
            setup,
            textvariable=self.difficulty_var,
            values=("Easy", "Medium", "Hard"),
            state="readonly",
            width=12,
        )
        self.difficulty_combo.grid(row=0, column=3, sticky="ew", pady=5)

        ttk.Label(setup, text="Player X name").grid(row=1, column=0, sticky="w", padx=(0, 8), pady=5)
        ttk.Entry(setup, textvariable=self.player_x_var, width=20).grid(
            row=1, column=1, sticky="ew", padx=(0, 12), pady=5
        )

        ttk.Label(setup, text="Player O name").grid(row=1, column=2, sticky="w", padx=(0, 8), pady=5)
        self.player_o_entry = ttk.Entry(setup, textvariable=self.player_o_var, width=16)
        self.player_o_entry.grid(row=1, column=3, sticky="ew", pady=5)

        ttk.Button(setup, text="Start New Session", command=self.start_new_session).grid(
            row=2, column=0, columnspan=4, sticky="ew", pady=(10, 0)
        )

        self.status_label = ttk.Label(outer, text="", style="Status.TLabel", anchor="center")
        self.status_label.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        board_frame = tk.Frame(outer, bg="#d8dfeb", padx=5, pady=5)
        board_frame.grid(row=4, column=0, pady=(0, 14))
        for row in range(3):
            board_frame.rowconfigure(row, weight=1, minsize=96)
            board_frame.columnconfigure(row, weight=1, minsize=112)
            button_row = []
            for column in range(3):
                position = row * 3 + column + 1
                button = tk.Button(
                    board_frame,
                    text="",
                    font=("Segoe UI", 28, "bold"),
                    width=4,
                    height=1,
                    bg="#ffffff",
                    fg="#263247",
                    activebackground="#eaf0fb",
                    activeforeground="#17243b",
                    disabledforeground="#263247",
                    relief="flat",
                    bd=0,
                    cursor="hand2",
                    command=lambda move=position: self.play_move(move),
                )
                button.grid(row=row, column=column, sticky="nsew", padx=4, pady=4)
                button_row.append(button)
            self.board_buttons.append(button_row)

        scores_frame = ttk.LabelFrame(outer, text="Session score", padding=(12, 8))
        scores_frame.grid(row=5, column=0, sticky="ew", pady=(0, 14))
        for column in range(3):
            scores_frame.columnconfigure(column, weight=1)
        self.score_x_label = ttk.Label(scores_frame, text="X: 0", style="Score.TLabel", anchor="center")
        self.score_x_label.grid(row=0, column=0, sticky="ew", padx=4)
        self.score_o_label = ttk.Label(scores_frame, text="O: 0", style="Score.TLabel", anchor="center")
        self.score_o_label.grid(row=0, column=1, sticky="ew", padx=4)
        self.score_draws_label = ttk.Label(scores_frame, text="Draws: 0", style="Score.TLabel", anchor="center")
        self.score_draws_label.grid(row=0, column=2, sticky="ew", padx=4)

        controls = ttk.Frame(outer)
        controls.grid(row=6, column=0, sticky="ew")
        for column in range(2):
            controls.columnconfigure(column, weight=1)
        ttk.Button(controls, text="Restart Round", command=self.restart_round).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(controls, text="Quit", command=self.root.destroy).grid(
            row=0, column=1, sticky="ew", padx=(6, 0)
        )

    def on_mode_change(self, _event=None):
        if self.mode_var.get() == "Player vs Computer":
            if self.player_o_var.get().strip() in ("", "Player O", "Computer"):
                self.player_o_var.set("Computer")
            self.player_o_entry.configure(state="disabled")
            self.difficulty_combo.configure(state="readonly")
        else:
            if self.player_o_var.get().strip() == "Computer":
                self.player_o_var.set("Player O")
            self.player_o_entry.configure(state="normal")
            self.difficulty_combo.configure(state="disabled")

    def start_new_session(self, show_message=True):
        name_x = self.player_x_var.get().strip()
        if not name_x:
            messagebox.showerror("Missing name", "Please enter a name for Player X.", parent=self.root)
            return

        mode = self.mode_var.get()
        if mode == "Player vs Player":
            name_o = self.player_o_var.get().strip()
            if not name_o:
                messagebox.showerror("Missing name", "Please enter a name for Player O.", parent=self.root)
                return
            self.player_names = {"X": name_x, "O": name_o}
        else:
            self.player_names = {"X": name_x, "O": "Computer"}

        self.scores = {"X": 0, "O": 0, "draws": 0}
        self.restart_round()
        self.update_scoreboard()
        if show_message:
            self.status_label.configure(text="New session started.", style="Status.TLabel")
            self.root.after(900, self.update_status)

    def restart_round(self):
        if self.ai_job is not None:
            self.root.after_cancel(self.ai_job)
            self.ai_job = None

        self.board = self.empty_board()
        self.check = set()
        self.current_player = "X"
        self.game_over = False
        self.refresh_board()
        self.update_scoreboard()
        self.update_status()

    def play_move(self, position):
        if self.game_over or position in self.check:
            return
        if self.mode_var.get() == "Player vs Computer" and self.current_player == "O":
            return

        row, column = divmod(position - 1, 3)
        self.board[row][column] = self.current_player
        self.check.add(position)
        self.refresh_board()

        if self.finish_if_game_over(self.current_player):
            return

        self.current_player = "O" if self.current_player == "X" else "X"

        if self.mode_var.get() == "Player vs Computer" and self.current_player == "O":
            self.status_label.configure(text="Computer is thinking…", style="Status.TLabel")
            self.ai_job = self.root.after(400, self.computer_turn)
            self.refresh_board()
        else:
            self.update_status()
            self.refresh_board()

    def computer_turn(self):
        self.ai_job = None
        if self.game_over or self.current_player != "O":
            return

        difficulty = self.difficulty_var.get()

        # These project functions make the move themselves; they do not return a position.
        # Remember the occupied positions so the GUI can identify the computer's new move.
        positions_before = self.check.copy()

        # Suppress the AI functions' console messages while the GUI is running.
        # Their board/check updates still happen normally.
        with redirect_stdout(StringIO()):
            if difficulty == "Easy":
                computer_move_easy(self.board, self.check)
            elif difficulty == "Medium":
                computer_move_medium(self.board, self.check)
            else:
                computer_move_hard(self.board, self.check)

        new_positions = self.check - positions_before
        if not new_positions:
            messagebox.showerror(
                "Computer move error",
                "The computer move function did not add a position to the check set.",
                parent=self.root,
            )
            self.update_status()
            self.refresh_board()
            return

        position = next(iter(new_positions))
        self.refresh_board()

        if self.finish_if_game_over("O"):
            return

        self.current_player = "X"
        self.status_label.configure(
            text=f"Computer chose position {position}.",
            style="Status.TLabel",
        )
        self.refresh_board()
        self.root.after(1000, self.update_status)

    def finish_if_game_over(self, player):
        if check_winner(self.board, player):
            self.scores[player] += 1
            self.game_over = True
            self.update_scoreboard()
            self.status_label.configure(
                text=f"{self.player_names[player]} ({player}) wins!",
                style="Winner.TLabel",
            )
            self.refresh_board()
            return True

        if len(self.check) == 9:
            self.scores["draws"] += 1
            self.game_over = True
            self.update_scoreboard()
            self.status_label.configure(text="It's a draw!", style="Status.TLabel")
            self.refresh_board()
            return True

        return False

    def refresh_board(self):
        computer_thinking = self.mode_var.get() == "Player vs Computer" and self.current_player == "O"
        for row in range(3):
            for column in range(3):
                button = self.board_buttons[row][column]
                symbol = self.board[row][column]
                button.configure(text="" if symbol == " " else symbol)

                if symbol == "X":
                    button.configure(fg="#2463b5", disabledforeground="#2463b5")
                elif symbol == "O":
                    button.configure(fg="#d14a45", disabledforeground="#d14a45")
                else:
                    button.configure(fg="#263247", disabledforeground="#263247")

                position = row * 3 + column + 1
                disabled = self.game_over or position in self.check or computer_thinking or self.ai_job is not None
                button.configure(state="disabled" if disabled else "normal")

    def update_status(self):
        if self.game_over:
            return
        name = self.player_names[self.current_player]
        self.status_label.configure(
            text=f"{name}'s turn ({self.current_player})",
            style="Status.TLabel",
        )

    def update_scoreboard(self):
        self.score_x_label.configure(text=f"{self.player_names['X']} (X): {self.scores['X']}")
        self.score_o_label.configure(text=f"{self.player_names['O']} (O): {self.scores['O']}")
        self.score_draws_label.configure(text=f"Draws: {self.scores['draws']}")


def main():
    root = tk.Tk()
    TicTacToeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
