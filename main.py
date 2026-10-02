def check_winner(board, player):
    # check rows
    for row in board:
        if all(player==cell for cell in row):
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

    for i, row in enumerate(board):
        print(" | ".join(row))

        if i < len(board) - 1:
            print("---------")

def make_move(board, check, player):
    while True:
        try:
            choice = int(input(f"Player {current_player}, choose an empty position (1-9): "))
            if 1 <= choice <= 9 and choice not in check:
                check.add(choice)
                break

            print("Invalid choice. Choose an empty position from 1 to 9.")

        except ValueError:
            print("Please enter a number.")

        # convert position to row and column
    row = (choice - 1) // 3
    column = (choice - 1) % 3

    # Place the player's Symbol
    board[row][column] = player

def switch_player(player):
    return "O" if player == "X" else "X"


def check_game_over(board, check, player):
    if check_winner(board, current_player):
        display_board(board)
        print(f"Player {current_player} wins!")
        return True

    if len(check) == 9:
        display_board(board)
        print("It's a draw!")
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


while True:
    
    # start a new game
    board, check, current_player = reset_game()

    # Play the game
    while True:

        display_board(board)

        make_move(board, check, current_player)

        if check_game_over(board, check, current_player):
            break

        current_player = switch_player(current_player)

        #print()

    # Ask if the player wants another game
    while True:
        answer = input("Play again? (y/n): ").lower()

        if answer == "y":
            break

        if answer == "n":
            print("Thanks for playing!")
            exit()

        print("Please enter y or n.")



