import random

X = "X"
Circle = "O"

PLAYER_SYMBOL_DICT = {1: X, 2: Circle}


def which_player_start() -> int:
    """
         Decides which player starts
         :return:
             int
     """
    return random.randint(1, 2)


def next_turn(player: int) -> int:
    if player == 1:
        return 2
    return 1


def create_board(size: int = 3) -> list[list[str]]:
    board = list()
    for _ in range(size):
        board.append(list())
    for col in board:
        for _ in range(size):
            col.append("")
    return board


def print_board(board: list[list[str]], size: int) -> None:
    for index in range(size):
        print_row(board=board, index=index)


def print_row(board: list[list[str]], index: int, ) -> None:
    row = ""
    for col in board:
        row += f"[{col[index]}]"
    print(row)


def move(board: list[list[str]], player: int, row: int, col: int) -> bool:
    if is_move_legal(board=board, row=row, col=col):
        board[col][row] = PLAYER_SYMBOL_DICT[player]
        return True
    print('This cell is already taken!')
    return False


def is_move_legal(board: list[list[str]], row: int, col: int) -> bool:
    try:
        return board[col][row] == ""
    except IndexError:
        print(f'Invalid row or col value')
        return False


def win_in_row(board: list[list[str]], player: int) -> bool:
    player_symbol = PLAYER_SYMBOL_DICT[player]
    for index in range(len(board)):
        win_condition = has_same_symbol(board=board, symbol=player_symbol, col=0, row=index,
                                        col_shift=1, row_shift=0)
        if win_condition:
            return True
    return False


def win_in_col(board: list[list[str]], player: int) -> bool:
    player_symbol = PLAYER_SYMBOL_DICT[player]
    for index in range(len(board)):
        win_condition = has_same_symbol(board=board, symbol=player_symbol, col=index, row=0,
                                        col_shift=0, row_shift=1)
        if win_condition:
            return True
    return False


def win_in_diagonal(board: list[list[str]], player: int) -> bool:
    player_symbol = PLAYER_SYMBOL_DICT[player]
    win_condition_right_diagonal = has_same_symbol(board=board, symbol=player_symbol, col=0, row=0,
                                                   col_shift=1, row_shift=1)
    if win_condition_right_diagonal:
        return True

    win_condition_left_diagonal = has_same_symbol(board=board, symbol=player_symbol,
                                                  col=len(board) - 1, row=0,
                                                  col_shift=-1, row_shift=1)
    if win_condition_left_diagonal:
        return True

    return False


def has_same_symbol(board: list[list[str]], symbol: str,
                    col: int, row: int, col_shift: int, row_shift: int) -> bool:
    try:
        cell = board[col][row]
        print(f"Checking {cell=} vs {symbol=}")
        if cell == symbol:
            return has_same_symbol(board=board, symbol=symbol, col=col + col_shift,
                                   row=row + row_shift,
                                   col_shift=col_shift, row_shift=row_shift)
    except IndexError:
        print(f"Reached {col=} {row=}")
        return True
    print(f'Returning False')
    return False


my_board = create_board()
print(my_board)
print(my_board[0])
move(board=my_board, player=1, row=0, col=0)
move(board=my_board, player=1, row=1, col=1)
move(board=my_board, player=1, row=2, col=2)
print_board(board=my_board, size=3)
player_win = win_in_diagonal(board=my_board, player=1)
print(f"{player_win=}")
