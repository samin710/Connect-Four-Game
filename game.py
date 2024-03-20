import numpy as np
import random

# Constants
EMPTY = 0
PLAYER = 1
COMPUTER = 2
ROW_COUNT = 6
COLUMN_COUNT = 7


def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT))


def is_valid_move(board, column):
    return board[ROW_COUNT - 1][column] == EMPTY


def drop_piece(board, row, column, piece):
    board[row][column] = piece


def get_next_open_row(board, column):
    for r in range(ROW_COUNT):
        if board[r][column] == EMPTY:
            return r


def is_winning_move(board, piece):
    # Check horizontal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Check vertical
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Check positive diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Check negative diagonal
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True

    return False


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER if piece == COMPUTER else COMPUTER

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score


def score_position(board, piece):
    score = 0

    # Center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Horizontal scoring
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c: c + 4]
            score += evaluate_window(window, piece)

    # Vertical scoring
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r: r + 4]
            score += evaluate_window(window, piece)

    # Positive diagonal scoring
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    # Negative diagonal scoring
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(4)]
            score += evaluate_window(window, piece)

    return score


def is_terminal_node(board):
    return (
        is_winning_move(board, PLAYER)
        or is_winning_move(board, COMPUTER)
        or len(get_valid_moves(board)) == 0
    )


def get_valid_moves(board):
    return [c for c in range(COLUMN_COUNT) if is_valid_move(board, c)]


def minimax(board, depth, alpha, beta, maximizing_player):
    valid_moves = get_valid_moves(board)
    terminal_node = is_terminal_node(board)

    if depth == 0 or terminal_node:
        if terminal_node:
            if is_winning_move(board, COMPUTER):
                return (None, 100000000000000)
            elif is_winning_move(board, PLAYER):
                return (None, -10000000000000)
            else:  # Game over, no more valid moves
                return (None, 0)
        else:  # Depth is 0
            return (None, score_position(board, COMPUTER))

    if maximizing_player:
        value = -float("inf")
        column = np.random.choice(valid_moves)
        for move in valid_moves:
            temp_board = board.copy()
            row = get_next_open_row(temp_board, move)
            drop_piece(temp_board, row, move, COMPUTER)
            new_score = minimax(temp_board, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = move
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value
    else:  # Minimizing player
        value = float("inf")
        column = np.random.choice(valid_moves)
        for move in valid_moves:
            temp_board = board.copy()
            row = get_next_open_row(temp_board, move)
            drop_piece(temp_board, row, move, PLAYER)
            new_score = minimax(temp_board, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = move
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value


def print_board(board):
    print(np.flip(board, 0))


def print_winner(board, piece):
    winning_board = board.copy()
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            if board[r][c] == piece:
                winning_board[r][c] = 1 if piece == PLAYER else 2

    print_board(winning_board)


def play_game():
    board = create_board()
    game_over = False

    # Randomly determine who starts
    if random.choice([PLAYER, COMPUTER]) == COMPUTER:
        column, _ = minimax(board, 4, -float("inf"), float("inf"), True)
        row = get_next_open_row(board, column)
        drop_piece(board, row, column, COMPUTER)
        print("Computer starts.")
        print_board(board)  # Display the board after the computer's first move

    while not game_over:
        # Player's turn
        column = int(input("Enter your move (0-6): "))
        if is_valid_move(board, column):
            row = get_next_open_row(board, column)
            drop_piece(board, row, column, PLAYER)

            if is_winning_move(board, PLAYER):
                print("Congratulations! You win!")
                print_winner(board, PLAYER)
                game_over = True
                break

            print_board(board)
            print("")

        # Computer's turn
        column, _ = minimax(board, 4, -float("inf"), float("inf"), True)
        if is_valid_move(board, column):
            row = get_next_open_row(board, column)
            drop_piece(board, row, column, COMPUTER)

            if is_winning_move(board, COMPUTER):
                print("The computer wins! You lose.")
                print_winner(board, COMPUTER)
                game_over = True
                break

            print_board(board)
            print("")

        if len(get_valid_moves(board)) == 0:
            print("It's a tie!")
            game_over = True


play_game()
