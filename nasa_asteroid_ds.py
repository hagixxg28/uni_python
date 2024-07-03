# Adding my github to showcase the coding process - I am not a robot.
# https://github.com/hagixxg28/uni_python
"""
@Author: Hagai Gilor
@ID : 206037574
"""

from typing import Optional
import numpy as np

EST_DIA_IN_KM_MAX = 'Est Dia in KM(max)'

EST_DIA_IN_KM_MIN = 'Est Dia in KM(min)'

CLOSE_APPROACH_DATE = "Close Approach Date"
EQUINOX = "Equinox"
ORBITING_BODY = "Orbiting Body"
NEO_REFERENCE_ID = "Neo Reference ID"
ABSOLUTE_MAGNITUDE = "Absolute Magnitude"
MISS_DISTANCE_KM = 'Miss Dist.(kilometers)'
ORBIT_ID = 'Orbit ID'
MAX = "max"
MIN = "min"
COLUMNS_TO_CLEAR = [EQUINOX, ORBITING_BODY, NEO_REFERENCE_ID]
NAME = "Name"
YEAR_2000 = "2000-01-01"

NAMES = ['Neo Reference ID', NAME, ABSOLUTE_MAGNITUDE, EST_DIA_IN_KM_MIN, EST_DIA_IN_KM_MAX,
         'Est Dia in M(min)', 'Est Dia in M(max)', 'Est Dia in Miles(min)', 'Est Dia in Miles(max)',
         'Est Dia in Feet(min)', 'Est Dia in Feet(max)', CLOSE_APPROACH_DATE, 'Epoch Date Close Approach',
         'Relative Velocity km per sec', 'Relative Velocity km per hr', 'Miles per hour', 'Miss Dist.(Astronomical)',
         'Miss Dist.(lunar)', MISS_DISTANCE_KM, 'Miss Dist.(miles)', 'Orbiting Body', ORBIT_ID,
         'Orbit Determination Date', 'Orbit Uncertainity', 'Minimum Orbit Intersection', 'Jupiter Tisserand Invariant',
         'Epoch Osculation', 'Eccentricity', 'Semi Major Axis', 'Inclination', 'Asc Node Longitude', 'Orbital Period',
         'Perihelion Distance', 'Perihelion Arg', 'Aphelion Dist', 'Perihelion Time', 'Mean Anomaly', 'Mean Motion',
         'Equinox', 'Hazardous\n']


def get_column_index_by_name(header: np.array, column_name: str):
    return np.where(header == column_name)[0][0]


def extract_column_values(data, column_index, start_index: Optional[int] = 1) -> np.array:
    return data[start_index:, column_index].astype(float)


def get__val_index_in_column_by_operation(data, column_name: str, operation_type: Optional[str] = MAX):
    header = data[0]
    col_index = get_column_index_by_name(header=header, column_name=column_name)
    column = extract_column_values(data=data, column_index=col_index)
    if operation_type == MAX:
        return np.argmax(column)
    if operation_type == MIN:
        return np.argmin(column)
    raise TypeError(f"Invalid {operation_type=}")


def get_data_by_operation_column_val(data, column_to_compare_by_name: str, columns: list[str],
                                     operation_type: Optional[str] = MAX) -> list:
    max_index = get__val_index_in_column_by_operation(data=data, column_name=column_to_compare_by_name,
                                                      operation_type=operation_type)
    values = []
    header = data[0]
    for column in columns:
        col_index = get_column_index_by_name(header=header, column_name=column)
        values.append(data[max_index + 1, col_index])
    return values


def load_data(file_name: str) -> np.ndarray:
    try:
        data = np.genfromtxt(fname=file_name, delimiter=",", dtype=str)
    except FileNotFoundError:
        print(f"{file_name=} not found")
        raise
    except OSError:
        print(f"Error handling {file_name=}")
        raise
    return data


def scoping_data(data: np.ndarray, names: Optional[list[str]] = None) -> np.ndarray:
    if names is None:
        names = NAMES
    index = np.argmax(data == names)
    mask = np.arange(data.shape[0]) != index
    new_data = data[mask]
    return new_data


def mask_data(data: np.ndarray) -> np.ndarray:
    headers, data_without_headers = split_data(data=data)
    close_approach_date_column_index = np.argmax(headers == CLOSE_APPROACH_DATE)
    mask = data_without_headers[:, close_approach_date_column_index].astype("datetime64") >= np.datetime64(YEAR_2000)
    return data_without_headers[mask]


def split_data(data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    return data[0, :], data[1:, :]


def data_details(data: np.ndarray) -> None:
    headers, _ = split_data(data=data)
    indexes = find_indexes(data=headers, items=COLUMNS_TO_CLEAR)
    data = np.delete(data, indexes, axis=1)
    rows = data.shape[0]
    columns = data.shape[1]
    print(f'{rows=}')
    print(f'{columns=}')
    print(f'Headers: {data[0]}')


def find_indexes(data: np.ndarray, items: list) -> list:
    indexes = list()
    for item in items:
        index = np.argmax(data == item)
        if index is not None:
            indexes.append(index)
    return indexes


def max_absolute_magnitude(data: np.ndarray) -> list:
    return get_data_by_operation_column_val(data=data, column_to_compare_by_name=ABSOLUTE_MAGNITUDE,
                                            columns=[NAME, ABSOLUTE_MAGNITUDE], operation_type=MAX)


def closest_to_earth(data: np.array) -> str:
    return get_data_by_operation_column_val(data=data, column_to_compare_by_name=MISS_DISTANCE_KM,
                                            columns=[NAME], operation_type=MIN)[0]


def common_orbit(data) -> dict:
    return get_count_by_column_name(data=data, column_name=ORBIT_ID)


def get_column_values_by_name(data, column_name: str) -> np.array:
    header = data[0]
    col_index = get_column_index_by_name(header=header, column_name=column_name)
    return extract_column_values(data=data, column_index=col_index)


def get_count_by_column_name(data, column_name: str) -> dict:
    column = get_column_values_by_name(data=data, column_name=column_name)
    column_set = set(column)
    count_dict = dict()
    for value in column_set:
        count_dict[int(value)] = int(np.sum(column == value).astype(int))
    return count_dict


def get_mean_by_column_name(data, column_name: str) -> float:
    column = get_column_values_by_name(data=data, column_name=column_name)
    return np.mean(column)


def min_max_diameter(data) -> tuple[float, float]:
    dia_in_km_min = float(get_mean_by_column_name(data=data, column_name=EST_DIA_IN_KM_MIN))
    dia_in_km_max = float(get_mean_by_column_name(data=data, column_name=EST_DIA_IN_KM_MAX))
    return dia_in_km_min, dia_in_km_max


def main():
    data = load_data(file_name="nasa.csv")
    print(min_max_diameter(data=data))


main()
