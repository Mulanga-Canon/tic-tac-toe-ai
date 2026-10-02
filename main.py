import random


def check_winner(board, player):
    # check rows
    for row in board:
        if all(cell == player for cell in row):
            return True

    # check columns
    for column in range(3):
        if all(board[row][column] == player for row in range(3)):
            return True


    # check diagonals
    if all(board[i][i] == player for i in range(3)):
        return True

    if all(board[i][2-i] == player for i in range(3)):
        return True

    return False

def display_board(board):
    print()

    position = 1

    for i, row in enumerate(board):
        display_row = []

        for cell in row:
            if cell == " ":
                display_row.append(str(position))
            else:
                display_row.append(cell)

            position += 1

        print(" | ".join(display_row))

        if i < len(board) - 1:
            print("---------")


def make_move(board, check, player, player_names):
    while True:
        try:
            choice = int(input(f"{player_names[player]}, choose an empty position (1-9): "))
            if 1 <= choice <= 9 and choice not in check:
                check.add(choice)
                break

            print("Invalid choice. Choose an empty position from 1 to 9.")

        except ValueError:
            print("Please enter a number.")

    # Convert position to row and column
    row = (choice - 1) // 3
    column = (choice - 1) % 3

    # Place the player's symbol
    board[row][column] = player

def switch_player(player):
    return "O" if player == "X" else "X"


def check_game_over(board, check, player, scores, player_names):
    if check_winner(board, player):
        display_board(board)
        print(f"{player_names[player]} wins!")
        scores[player] += 1
        return True

    if len(check) == 9:
        display_board(board)
        print("It's a draw!")
        scores["draws"] += 1
        return True

    return False

def reset_game():
    board = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]

    check = set()
    current_player = "X"

    return board, check, current_player


def display_intro(player_names):
    print()
    print("================================")
    print("          TIC TAC TOE")
    print("================================")
    print()
    print(f"Player X: {player_names['X']}")
    print(f"Player O: {player_names['O']}")
    print()
    print("Choose a position by entering")
    print("a number from 1 to 9.")


def get_player_name(symbol):
    while True:
        name = input(f"Enter name for Player {symbol}: ").strip()

        if name:
            return name

        print("Name cannot be empty.")


def choose_game_mode():
    while True:
        choice = input(
            "\nChoose game mode:\n"
            "1. Player vs Player\n"
            "2. Player vs Computer\n"
            "\nEnter choice: "
        )

        if choice in ("1", "2"):
            return choice

        print("Please enter 1 or 2.")


def computer_move_medium(board, check):

    # 1. Try to win
    choice = find_winning_move(board, check, "O")

    # 2. Block X from winning
    if choice is None:
        choice = find_winning_move(board, check, "X")

    # 3. Otherwise choose randomly
    if choice is None:
        if 5 not in check:
            choice = 5
        else:
            corners = [1, 3, 7, 9]
            availiable_corners = [
                position for position in corners
                if position not in check
            ]

            if availiable_corners:
                choice = random.choice(availiable_corners)
            else:
                edges = [2, 4, 6, 8]
                availiable_edges = [
                    position for position in edges
                    if position not in check
                ]

                choice = random.choice(availiable_edges)

    check.add(choice)

    row = (choice - 1) // 3
    column = (choice - 1) % 3

    board[row][column] = "O"

    print(f"Computer chooses position {choice}.")


def find_winning_move(board, check, player):
    for choice in range(1, 10):

        if choice in check:
            continue

        row = (choice - 1) // 3
        column = (choice - 1) % 3

        # Temporarily make the move
        board[row][column] = player

        if check_winner(board, player):
            board[row][column] = " "
            return choice

        # Undo the temporary move
        board[row][column] = " "

    return


def choose_difficulty():
    while True:
        choice = input(
            "\nChoose difficulty:\n"
            "1. Easy\n"
            "2. Medium\n"
            "3. Hard\n"
            "\nEnter choice: "
        )

        if choice in ("1", "2", "3"):
            return choice

        print("Please enter 1, 2, or 3.")


def computer_move_easy(board, check):
    available_positions = [
        position
        for position in range(1, 10)
        if position not in check
    ]

    choice = random.choice(available_positions)

    check.add(choice)

    row = (choice - 1) // 3
    column = (choice - 1) % 3

    board[row][column] = "O"

    print(f"Computer chooses position {choice}.")


def main():

    game_mode = choose_game_mode()
    difficulty = None

    if game_mode == "2":
        difficulty = choose_difficulty()

    if game_mode == "1":
        player_names = {
            "X" : get_player_name("X"),
            "O" : get_player_name("O")
        }
    else:
        player_names = {
            "X": get_player_name("X"),
            "O": "Computer"
        }

    display_intro(player_names)

    scores = {
        "X" : 0,
        "O" : 0,
        "draws" : 0
    }

    while True:

        # start a new game
        board, check, current_player = reset_game()

        # Play the game
        while True:

            display_board(board)

            if game_mode == "2" and current_player == "O":

                if difficulty == "1":
                    computer_move_easy(board, check)

                elif difficulty == "2":
                    computer_move_medium(board, check)

            else:
                make_move(board, check, current_player, player_names)

            if check_game_over(board, check, current_player, scores, player_names):
                break

            current_player = switch_player(current_player)

        # Display the results of the game
        print()
        print(f"X wins: {scores['X']}")
        print(f"O wins: {scores['O']}")
        print(f"Draws: {scores['draws']}\n")

        # Ask if the player wants another game
        while True:
            answer = input("Play again? (y/n): ").lower()

            if answer == "y":
                break

            if answer == "n":
                print("Thanks for playing!")
                return

            print("Please enter y or n.")

if __name__ == "__main__":
    main()

