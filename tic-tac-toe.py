def check_winner(board):
    # Check rows, columns, and diagonals for a winner
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]              # diagonals
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] != '-':
            return board[condition[0]]
    # Check for a tie
    if '-' not in board:
        return 'Tie'
    # If no winer yet
    return None

def find_best_move(board):
    # Check for immediate winning move
    for i in range(9):
        if board[i] == '-':
            board[i] = 'X'
            if check_winner(board) == 'X':
                board[i] = '-'
                return i
            board[i] = '-'

    # Check for immediate blocking move
    for i in range(9):
        if board[i] == '-':
            board[i] = 'O'
            if check_winner(board) == 'O':
                board[i] = '-'
                return i
            board[i] = '-'

    # Place in the middle if available
    if board[4] == '-':
        return 4

    # Palce in the corners
    for i in [0, 2, 6, 8]:
        if board[i] == '-':
            return i

    # Place in any remaining spot
    for i in range(9):
        if board[i] == '-':
            return i

board = ['-', '-', '-',
         '-', '-', '-',
         '-', '-', '-']

print("Wecome to Tic-Tac-Toe!")
print(board[0] + " " + board[1] + " " + board[2])
print(board[3] + " " + board[4] + " " + board[5])
print(board[6] + " " + board[7] + " " + board[8])

while True:
    # Computer's move
    computer_move = find_best_move(board)
    board[computer_move] = 'X'

    print("\nComputer's move:")
    print(board[0] + " " + board[1] + " " + board[2])
    print(board[3] + " " + board[4] + " " + board[5])
    print(board[6] + " " + board[7] + " " + board[8])

    # Check for computer win
    winner = check_winner(board)
    if winner == 'X':
        print("Computer won!")
        break
    elif winner == 'Tie':
        print("Tied")
        break

    # User's move
    while True:
        user_input = input("Enter the field number (1-9): ")
        try:
            user_index = int(user_input) - 1
            if user_index < 0 or user_index > 8 or board[user_index] != '-':
                print("Error: Invalid move. Try again.")
            else:
                board[user_index] = 'O'
                break
        except ValueError:
            print("Error: Please enter a number.")

    print("\nYour move:")
    print(board[0] + " " + board[1] + " " + board[2])
    print(board[3] + " " + board[4] + " " + board[5])
    print(board[6] + " " + board[7] + " " + board[8])

    # Check for user win or tie
    winner = check_winner(board)
    if winner == 'O':
        print("Congratulations! You won!")
        break
    elif winner == 'Tie':
        print("Tied")
        break
