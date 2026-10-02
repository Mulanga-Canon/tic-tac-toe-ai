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

def main():

    player_names = {
        "X" : get_player_name("X"),
        "O" : get_player_name("O")
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

