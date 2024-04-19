import random


def generate_number() -> int:
    """
        Generates a random number between 1000 to 9999
        :return:
            int
    """
    return random.randint(1000, 9999)


def which_player_start() -> int:
    """
         Decides which player starts
         :return:
             int
     """
    return random.randint(1, 2)


def is_digit_exist(num: int, digit: int) -> bool:
    """
         Determines if the digit is within the number
         :return:
             bool
     """
    num_str = str(num)
    digit_str = str(digit)
    return digit_str in num_str


def num_of_existing_digits(guess_num: int, secret_num: int) -> int:
    """
         Determines the number of digits that exist within the secret number
         :return:
             int
     """
    existing_digits = 0
    guess_num_str = str(guess_num)

    for digit_str in guess_num_str:
        digit = int(digit_str)
        if is_digit_exist(num=secret_num, digit=digit):
            existing_digits += 1

    return existing_digits


def num_of_cows(guess_num: int, secret_num: int, bulls: int) -> int:
    """
         Determines the number of cows
         :return:
             int
     """
    return num_of_existing_digits(guess_num=guess_num,
                                  secret_num=secret_num) - bulls


def num_of_bulls(guess_num: int, secret_num: int) -> int:
    """
         Determines the number of bulls
         :return:
             int
    """
    guess_num_str = str(guess_num)
    secret_num_str = str(secret_num)
    bulls = 0
    index = 0
    for digit_str in guess_num_str:
        if digit_str == secret_num_str[index]:
            bulls += 1
        index += 1
    return bulls


def determine_bulls_and_cows(guess_num: int, secret_num: int) -> [int, int]:
    """
        A function that determines the number of cows and bulls
        :return:
             list
    """
    bulls = num_of_bulls(guess_num=guess_num, secret_num=secret_num)
    cows = num_of_cows(guess_num=guess_num, secret_num=secret_num, bulls=bulls)
    return [bulls, cows]


def current_player(turn: int, first_player: int) -> int:
    """
        Determines the current player
         :return:
             int
    """
    if turn % 2 == 0:
        return second_player(first_player=first_player)
    return first_player


def second_player(first_player: int) -> int:
    """
        Determines the second player
        :return:
            int
    """
    if first_player == 1:
        return 2
    return 1


def play_turn(secret_num: int, player: int) -> bool:
    """
        Runs a turn and determines if the player has won
        :return:
            bool
    """
    num = generate_number()

    if secret_num == num:
        print("Correct guess!", num)
        return True

    bulls, cows = determine_bulls_and_cows(guess_num=num,
                                           secret_num=secret_num)
    print("Player", player, 'guessed number = ', num, ' Bulls = ',
          bulls, ' Cows = ', cows)
    return False


def start_game():
    """
        Starts the game with a loop until a player wins
        :return:
            None
    """
    turn = 1
    first_player = which_player_start()
    secret = generate_number()
    print("Secret number =", secret)
    print("Player", first_player, "starts!")

    while True:
        player = current_player(turn=turn, first_player=first_player)
        if play_turn(secret_num=secret, player=player):
            print('Player', player, 'wins!')
            return
        turn += 1


def main():
    start_game()


main()
