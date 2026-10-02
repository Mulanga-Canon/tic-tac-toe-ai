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


board = [
        [" ", " ", " "],
        [" ", " ", " "],
        [" ", " ", " "]
    ]

check = set()
current_player = "X"


while True:

    # Display the board
    for i, row in enumerate(board):
        print(" | ".join(row))

        if i < len(board) - 1:
            print("---------")


    # Get player's move
    choice = -1
    while True:
        choice = int(input(f"Player {current_player}, choose an empty position (1-9): "))
        if 1<=choice<=9 and choice not in check:
            check.add(choice)
            break

        print("Invalid choice. Choose an empty position from 1 to 9.")


    # convert position to row and column
    row = (choice - 1) // 3
    column = (choice - 1) % 3

    # Place the player's Symbol
    board[row][column] = current_player

    if check_winner(board, current_player):
        print()

        for i, row in enumerate(board):
            print(" | ".join(row))

            if i < len(board) - 1:
                print("---------")

        print(f"Player {current_player} wins!")
        break

    # Switch player
    if current_player == "X":
        current_player = "O"
    else:
        current_player = "X"

    print()


