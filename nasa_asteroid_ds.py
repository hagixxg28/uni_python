from datetime import datetime
from typing import Optional
import numpy as np

CLOSE_APPROACH_DATE = "Close Approach Date"
EQUINOX = "Equinox"
ORBITING_BODY = "Orbiting Body"
NEO_REFERENCE_ID = "Neo Reference ID"
ABSOLUTE_MAGNITUDE = "Absolute Magnitude"
COLUMNS_TO_CLEAR = [EQUINOX, ORBITING_BODY, NEO_REFERENCE_ID]
NAME = "Name"
YEAR_2000 = "2000-01-01"

NAMES = ['Neo Reference ID', NAME, ABSOLUTE_MAGNITUDE, 'Est Dia in KM(min)', 'Est Dia in KM(max)',
         'Est Dia in M(min)', 'Est Dia in M(max)', 'Est Dia in Miles(min)', 'Est Dia in Miles(max)',
         'Est Dia in Feet(min)', 'Est Dia in Feet(max)', CLOSE_APPROACH_DATE, 'Epoch Date Close Approach',
         'Relative Velocity km per sec', 'Relative Velocity km per hr', 'Miles per hour', 'Miss Dist.(Astronomical)',
         'Miss Dist.(lunar)', 'Miss Dist.(kilometers)', 'Miss Dist.(miles)', 'Orbiting Body', 'Orbit ID',
         'Orbit Determination Date', 'Orbit Uncertainity', 'Minimum Orbit Intersection', 'Jupiter Tisserand Invariant',
         'Epoch Osculation', 'Eccentricity', 'Semi Major Axis', 'Inclination', 'Asc Node Longitude', 'Orbital Period',
         'Perihelion Distance', 'Perihelion Arg', 'Aphelion Dist', 'Perihelion Time', 'Mean Anomaly', 'Mean Motion',
         'Equinox', 'Hazardous\n']


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


def max_absolute_magnitude(data: np.ndarray) -> tuple[str, float]:
    headers, _ = split_data(data=data)
    indexes = find_indexes(data=headers, items=[NAME, ABSOLUTE_MAGNITUDE])
    name_column = data[:, indexes[0]]
    absolute_magnitude_column = data[:, indexes[1]]
    max_index = np.argmax(absolute_magnitude_column)
    name = str(name_column[max_index])
    absolute_magnitude = absolute_magnitude_column[max_index]
    print(f'{name_column=}')
    print(f"{name=}")
    print(f"{absolute_magnitude=}")
    return None, None


def main():
    data = load_data(file_name="nasa.csv")
    print(max_absolute_magnitude(data=data))


main()
