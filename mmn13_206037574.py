# Adding my github to showcase the coding process - I am not a robot.
# https://github.com/hagixxg28/uni_python
"""
@Author: Hagai Gilor
@ID : 206037574
"""


def find_missing_item_v1(items: list[int]) -> int:
    """
           Iterates on a list of integers and finds
           the missing number in the series by comparing the integers' delta to do the
           calculated incline.
           If there is a mismatch that means we found our missing number
            in the series and we calculate it.
           If none is found it will return -1 (I know I didn't need to do this part)
           :return:
               int
           """
    incline = find_incline_of_list(items=items)
    last_item = None
    for item in items:

        if last_item is None:
            last_item = item
            continue

        delta_items = item - last_item
        if delta_items == incline:
            last_item = item
            continue

        return int(last_item + incline)
    return -1


def find_incline_of_list(items: list[int]) -> float:
    """
      Calculates the rate of change between each jump in the integers' series
      by using basic Calculus
      :return:
          int
    """
    items_len = len(items)
    delta = items[-1] - items[0]
    return delta / items_len


def find_missing_item_v2(items: list[int]) -> int:
    """
        Iterates on a list of integers and finds
        the missing number in the series using the given guidance.
        If none is found it will return -1 (I know I didn't need to do this part)
        :return:
            int
        """
    incline = find_incline_of_list(items=items)
    for index, item in enumerate(items):
        if index == 0:
            continue

        expected_item = calculate_item_by_index(first_item=items[0],
                                                incline=incline, index=index)
        if expected_item != item:
            return int(expected_item)
    return -1


def calculate_item_by_index(first_item: int,
                            incline: float, index: int) -> float:
    """
        A helper function that does some math.
        It calculates the expected value of an item in a series
        :return:
            float
        """
    return first_item + index * incline


def split_list_index(items: list[int]) -> int:
    """
        Iterates on a list of integers and finds the index where the list's sum
        is equal from both sides.
        If that index is not found will return -1
        :return:
            int
        """
    list_sum = sum(items)
    sub_sum = 0
    for index, item in enumerate(items):
        sub_sum += item

        if sub_sum == list_sum - sub_sum:
            return index
    return -1


def max_sequence(items: list[int]) -> int:
    """
     I know this is not a recursive function but I wanted to make sure
     I won't lose points by adding variables even though you said it's okay.
     This function calls a recursive function to count the number of times 2 consecutive numbers
     had the first one's digit number equal to the second's first digit
     :return:
         int
     """
    return sequence_counter(items=items)


def sequence_counter(items: list[int], index: int = 0,
                     longest_sequence: int = 1,
                     current_sequence: int = 1) -> int:
    """
     Iterates on a list of integers and counts the highest sequence of
     same numbers as described before.
     The moment the sequence breaks it compares the current count to the longest thus in the end
     returning the highest count.
     :return:
         int
     """
    if index == 0:
        return sequence_counter(items=items, index=index + 1)

    try:
        if digit_checker(last_item=items[index - 1],
                         current_item=items[index]):
            current_sequence += 1
        else:
            longest_sequence = max(longest_sequence, current_sequence)
            current_sequence = 1

    except IndexError:
        return max(longest_sequence, current_sequence)

    return sequence_counter(items=items,
                            index=index + 1,
                            longest_sequence=longest_sequence,
                            current_sequence=current_sequence)


def digit_checker(last_item: int, current_item: int) -> bool:
    """
      Checks if the last digit of a certain number is equal
      to the first digit of another number
      :return:
          bool
      """
    item_str = str(current_item)
    last_item_str = str(last_item)
    return last_item_str[-1] == item_str[0]


def order(s1: str, s2: str) -> str:
    """
      A recursive function that sorts 2 strings by their ASCI values (ascending)
      :return:
          str
      """

    try:
        if ord(s1[0]) < ord(s2[0]):
            return s1[0] + order(s1=s1[1:], s2=s2)
        return s2[0] + order(s1=s1, s2=s2[1:])
    except IndexError:
        if s1 != "":
            return s1

        if s2 != "":
            return s2


def test():
    """
    A small test function so I can manually check if the expected values are correct
    :return:
        None
    """
    find_missing_items_list = [
        [5, 7, 11, 13, 15],
        [3, 9, 12, 15, 18],
        [6, 2, -2, -6, -10]
    ]
    split_list_items = [
        [1, 3, -1, 2, -2, 7],
        [1, -2, 7, 0, 3]
    ]
    max_sequence_items = [
        [15, 52, 25, 1981, 123, 33, 321],
        [9, 196, 20606, 1981],
        [1234]
    ]
    order_strings = [
        ("acct", "bbdz"),
        ("a", "a"),
        ("cd", "ab"),
        ("", "ab"),

    ]
    for items in find_missing_items_list:
        print(f'find_missing_item_v1 {items=}'
              f' {find_missing_item_v1(items=items)}')
        print(f'find_missing_item_v2 {items=}'
              f' {find_missing_item_v2(items=items)}')

    for items in split_list_items:
        print(f'split_list_index {items=} {split_list_index(items=items)}')

    for items in max_sequence_items:
        print(f'max_sequence {max_sequence(items=items)}')
    for str_tuple in order_strings:
        print(f'order {order(s1=str_tuple[0], s2=str_tuple[1])}')
