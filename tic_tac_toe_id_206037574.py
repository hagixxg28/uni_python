import random

X = "X"
CIRCLE = "O"
EMPTY = ""
DEFAULT_SIZE = 3

PLAYER_SYMBOL_DICT = {1: X, 2: CIRCLE}


def which_player_start() -> int:
    """
         Decides which player starts
         :return:
             int
    """
    return random.randint(1, 2)


def next_turn(player: int) -> int:
    """
           Decides who's the next player
           :return:
               int
    """
    if player == 1:
        return 2
    return 1


def create_board(size: int = DEFAULT_SIZE) -> list[list[str]]:
    """
         Takes an integer and creates a board according to the size
         :return:
             list[list[str]]
    """
    board = list()
    for _ in range(size):
        board.append(list())
    for col in board:
        for _ in range(size):
            col.append(EMPTY)
    return board


def print_board(board: list[list[str]], size: int) -> None:
    """
         Prints the board by rows, iterates according to size
         :return:
            None
    """
    for index in range(size):
        print_row(board=board, index=index)


def print_row(board: list[list[str]], index: int, ) -> None:
    """
           This function is used to print a specific row
           :return:
              None
    """
    row = ""
    for col in board:
        row += f"[{col[index]}]"
    print(row)


def move(board: list[list[str]], player: int, row: int, col: int) -> bool:
    """
           Performs a move by a player, first checks if the play is legal.
           Returns a bool to show that a move has been made.
           :return:
              bool
    """
    if is_move_legal(board=board, row=row, col=col):
        board[col][row] = PLAYER_SYMBOL_DICT[player]
        return True
    return False


def is_move_legal(board: list[list[str]], row: int, col: int) -> bool:
    """
           Makes sure that the planned move is legal.
           Checking if the cell is not already taken
           and making sure it's not out of bounds.
           :return:
              bool
    """
    try:
        if board[col][row] == EMPTY:
            return True
        print('This cell is already taken!')
    except IndexError:
        print('Invalid row or col value')
    return False


def win_in_row(board: list[list[str]], player: int) -> bool:
    """
           Checks if the win condition is meet on all of the rows.
           Uses a recursive function to determine that.
           :return:
              bool
    """
    player_symbol = PLAYER_SYMBOL_DICT[player]
    for index in range(len(board)):
        win_condition = has_same_symbol(board=board, symbol=player_symbol,
                                        col=0, row=index,
                                        col_shift=1, row_shift=0)
        if win_condition:
            return True
    return False


def win_in_col(board: list[list[str]], player: int) -> bool:
    """
           Checks if the win condition is meet on all of the columns.
           Uses a recursive function to determine that.
           :return:
              bool
    """
    player_symbol = PLAYER_SYMBOL_DICT[player]
    for index in range(len(board)):
        win_condition = has_same_symbol(board=board, symbol=player_symbol,
                                        col=index, row=0,
                                        col_shift=0, row_shift=1)
        if win_condition:
            return True
    return False


def win_in_diagonal(board: list[list[str]], player: int) -> bool:
    """
           Checks if the win condition is meet on both diagonal sides.
           Uses a recursive function to determine that.
           :return:
              bool
    """
    player_symbol = PLAYER_SYMBOL_DICT[player]
    win_condition_right_diagonal = has_same_symbol(board=board,
                                                   symbol=player_symbol,
                                                   col=0, row=0,
                                                   col_shift=1, row_shift=1)
    if win_condition_right_diagonal:
        return True

    win_condition_left_diagonal = has_same_symbol(board=board,
                                                  symbol=player_symbol,
                                                  col=len(board) - 1, row=0,
                                                  col_shift=-1, row_shift=1)
    if win_condition_left_diagonal:
        return True

    return False


def win_game(board: list[list[str]], player: int,
             turn: int, size: int) -> bool:
    """
           Wraps all the win condition funcs together to
           check if the player won in a certain turn
           Avoids doing the checks if the win is not possible
           (Can't win on turn 2 if the size is 3)
           :return:
              bool
    """
    if turn < size:
        return False

    if win_in_row(board=board, player=player):
        return True

    if win_in_col(board=board, player=player):
        return True

    if win_in_diagonal(board=board, player=player):
        return True

    return False


def has_same_symbol(board: list[list[str]], symbol: str, col: int, row: int,
                    col_shift: int, row_shift: int) -> bool:
    """
           A recursive function that iterates on cells and checks
           if they share the same symbol as the given symbol
           Will return True once it reaches out of bounds -
           meaning all the symbols are the same until reaching that point
           If not it will return False prior to that.
           The shift args are made to what cells
           next to the original cells to check
           (Either the ones in it's row / collum / diagonal)
           :return:
              bool
    """
    try:
        cell = board[col][row]
        if cell == symbol:
            return has_same_symbol(board=board, symbol=symbol,
                                   col=col + col_shift,
                                   row=row + row_shift,
                                   col_shift=col_shift, row_shift=row_shift)
    except IndexError:
        return True
    return False


def board_is_full(board: list[list[str]], turn: int) -> bool:
    """
        This function makes a basic check if the board is full.
        The board can be filled only when a certain
        amount of turns have been played.
           :return:
              bool
    """
    return len(board) ** 2 < turn


def operate_turn(board: list[list[str]], current_player: int) -> None:
    """
       Performs the player's turn, also validating that the
       planned turn is valid.
           :return:
              None
    """
    while True:
        print('Go on player ' + str(current_player) + ' it\'s your turn!')
        row = int(input("Enter row position:"))
        col = int(input("Enter col position:"))

        made_a_move = move(board=board, player=current_player,
                           row=row, col=col)
        if made_a_move:
            return


def has_game_ended(board: list[list[str]], current_player: int,
                   size: int, turn: int) -> bool:
    """
      Performs a series of checks to see if the game has ended either
      by a tie or a win.
           :return:
              bool
    """
    if win_game(board=board, player=current_player, turn=turn, size=size):
        print(str(current_player) + ' wins!')
        return True

    if board_is_full(board=board, turn=turn):
        print("It's a tie!")
        return True
    return False


def start_game():
    """
       The core function that brings it all together.
       It starts by determining the first player and making sure
        the board size is valid.
       After that it enters a loop that ends either
       when a player wins or at a tie.
           :return:
              bool
    """
    size = int(input("Select board size"))

    if size < DEFAULT_SIZE:
        size = DEFAULT_SIZE

    current_player = which_player_start()
    board = create_board(size=size)
    print_board(board=board, size=size)
    turn = 1
    while True:

        if turn != 1:
            current_player = next_turn(player=current_player)

        operate_turn(board=board, current_player=current_player)
        print_board(board=board, size=size)

        game_ended = has_game_ended(board=board, current_player=current_player,
                                    size=size, turn=turn)
        if game_ended:
            break

        turn += 1


start_game()
