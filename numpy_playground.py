from typing import Optional

import numpy as np

NAME = "Name"
HANDSOMNESS = "Handsomness"
SYCHO_LEVEL = "Sycho Level"
TEST = [
    [NAME, SYCHO_LEVEL, HANDSOMNESS],
    ['Damrir', 99, 10],
    ['Hagai', 59, 17.5],
    ['Elad', 1, 1],
    ['Elad1', 1, 1],
    ['Elad2', 1, 1],
    ['Elad3', 1, 1],
]


def test_func():
    data = np.array(TEST)
    values = get_data_by_max_column_val(data=data, column_to_compare_by_name=HANDSOMNESS, columns=[NAME, HANDSOMNESS])
    print(f'{values=}')


def get_column_index_by_name(header: np.array, column_name: str):
    return np.where(header == column_name)[0][0]


def extract_column_values(data, column_index, start_index: Optional[int] = 1) -> np.array:
    return data[start_index:, column_index].astype(float)


def get_max_val_index_in_column(data, column_name: str):
    header = data[0]
    col_index = get_column_index_by_name(header=header, column_name=column_name)
    column = extract_column_values(data=data, column_index=col_index)
    return np.argmax(column)


def get_data_by_max_column_val(data, column_to_compare_by_name: str, columns: list[str]) -> list:
    max_index = get_max_val_index_in_column(data=data, column_name=column_to_compare_by_name)
    values = []
    header = data[0]
    for column in columns:
        col_index = get_column_index_by_name(header=header, column_name=column)
        values.append(data[max_index + 1, col_index])
    return values


def get_count_by_column_name(data, column_name: str) -> dict:
    header = data[0]
    col_index = get_column_index_by_name(header=header, column_name=column_name)
    column = extract_column_values(data=data, column_index=col_index)
    column_set = set(column)
    count_dict = dict()
    for value in column_set:
        count_dict[value] = np.sum(column == value)
    return count_dict


def main():
    test_func()


main()
