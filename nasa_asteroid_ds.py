# Adding my github to showcase the coding process - I am not a robot.
# https://github.com/hagixxg28/uni_python
"""
@Author: Hagai Gilor
@ID : 206037574
"""

from typing import Optional
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np

# I am using constants in order to make the workflow
# cleaner and less prone to errors

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
FLOAT = "float"
STR = "str"
INT = "int"
MILES_PER_HOUR = 'Miles per hour'

TYPE_DICT = {INT: int,
             FLOAT: float,
             STR: str}

COLOR_BLUE = "blue"
COLOR_BLACK = "black"
HAZARDOUS = "Hazardous"
NON_HAZARDOUS = f"Non {HAZARDOUS}"
NAMES = ['Neo Reference ID', NAME, ABSOLUTE_MAGNITUDE,
         EST_DIA_IN_KM_MIN, EST_DIA_IN_KM_MAX,
         'Est Dia in M(min)', 'Est Dia in M(max)', 'Est Dia in Miles(min)',
         'Est Dia in Miles(max)',
         'Est Dia in Feet(min)', 'Est Dia in Feet(max)', CLOSE_APPROACH_DATE,
         'Epoch Date Close Approach',
         'Relative Velocity km per sec', 'Relative Velocity km per hr',
         MILES_PER_HOUR,
         'Miss Dist.(Astronomical)',
         'Miss Dist.(lunar)', MISS_DISTANCE_KM, 'Miss Dist.(miles)',
         'Orbiting Body', ORBIT_ID,
         'Orbit Determination Date', 'Orbit Uncertainity',
         'Minimum Orbit Intersection',
         'Jupiter Tisserand Invariant',
         'Epoch Osculation', 'Eccentricity', 'Semi Major Axis',
         'Inclination',
         'Asc Node Longitude', 'Orbital Period',
         'Perihelion Distance', 'Perihelion Arg', 'Aphelion Dist',
         'Perihelion Time',
         'Mean Anomaly', 'Mean Motion',
         'Equinox', 'Hazardous\n']


# End of consts

def get_column_index_by_name(header: np.array, column_name: str) -> int:
    """
      Finds the column index by a given name
      :return:
          int
    """
    return np.where(header == column_name)[0][0]


def get_column_indexes_by_names(header: np.array,
                                column_names: list[str]) -> list[int]:
    """
      Returns multiple indexes by a given list of names,
      uses get_column_index_by_name.
      :return:
          list[int]
    """
    indexes = list()
    for column_name in column_names:
        column_index = get_column_index_by_name(header=header,
                                                column_name=column_name)
        indexes.append(column_index)
    return indexes


def extract_column_values(data, column_indexes: list[int],
                          start_index: Optional[int] = 1,
                          data_type: str = FLOAT) -> np.array:
    """
      Extract specific column values from an ndarray.
      data_type is used to cast the values to the right type.
      :return:
          numpy.ndarray
    """
    as_type = TYPE_DICT.get(data_type)
    if as_type is None:
        raise TypeError(f"Invalid {data_type=}")
    return data[start_index:, column_indexes].astype(as_type)


def get__val_index_in_column_by_operation(
        data,
        column_name: str,
        operation_type: Optional[str] = MAX) -> np.ndarray[int]:
    """
      Extracts either the MIN or MAX value from a column.
      :return:
          numpy.ndarray[int]
    """
    header = data[0]
    col_index = get_column_index_by_name(header=header,
                                         column_name=column_name)
    column = extract_column_values(data=data, column_indexes=[col_index])
    if operation_type == MAX:
        return np.argmax(column)
    if operation_type == MIN:
        return np.argmin(column)
    raise TypeError(f"Invalid {operation_type=}")


def get_data_by_operation_column_val(
        data,
        column_to_compare_by_name: str,
        columns: list[str],
        operation_type: Optional[str] = MAX) -> list:
    """
      Extracts the corresponding values in other columns to
      the given "column_to_compare_by_name".
      Example: I want to check the maximum value in column A
      and want the corresponding values to it in columns B and C
      :return:
          list
    """
    max_index = get__val_index_in_column_by_operation(
        data=data,
        column_name=column_to_compare_by_name,
        operation_type=operation_type)
    values = []
    header = data[0]
    for column in columns:
        col_index = get_column_index_by_name(header=header, column_name=column)
        values.append(data[max_index + 1, col_index])
    return values


def load_data(file_name: str) -> np.ndarray:
    """
      Loads the data from a given file name, supports CSV
      :return:
          numpy.ndarray
    """
    try:
        data = np.genfromtxt(fname=file_name, delimiter=",", dtype=str)
    except FileNotFoundError:
        print(f"{file_name=} not found")
        raise
    except OSError:
        print(f"Error handling {file_name=}")
        raise
    return data


def scoping_data(data: np.ndarray,
                 names: Optional[list[str]] = None) -> np.ndarray:
    """
      Clears out the given names row
      :return:
          numpy.ndarray
    """
    if names is None:
        names = NAMES
    index = np.argmax(data == names)
    mask = np.arange(data.shape[0]) != index
    new_data = data[mask]
    return new_data


def mask_data(data: np.ndarray) -> np.ndarray:
    """
      Returns values that are only after a certain date
      (In this case the year 2000).
      :return:
          numpy.ndarray
    """
    headers, data_without_headers = split_data(data=data)
    close_approach_date_column_index = np.argmax(
        headers == CLOSE_APPROACH_DATE)
    mask = data_without_headers[:, close_approach_date_column_index].astype(
        "datetime64") >= np.datetime64(YEAR_2000)
    return data_without_headers[mask]


def split_data(data: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """
         A helper function that just returns the data without the headers
         :return:
             numpy.ndarray
    """
    return data[0, :], data[1:, :]


def data_details(data: np.ndarray) -> None:
    """
         Prints out the amount of rows and columns and the headers
          of a given ndarray after clearing out certain columns
         :return:
             None
    """
    headers, _ = split_data(data=data)
    indexes = find_indexes(data=headers, items=COLUMNS_TO_CLEAR)
    data = np.delete(data, indexes, axis=1)
    rows = data.shape[0]
    columns = data.shape[1]
    print(rows)
    print(columns)
    print(data[0])


def find_indexes(data: np.ndarray, items: list) -> list:
    """
         A helper function that finds the indexes of certain values
         :return:
             list
    """
    indexes = list()
    for item in items:
        index = np.argmax(data == item)
        if index is not None:
            indexes.append(index)
    return indexes


def max_absolute_magnitude(data: np.ndarray) -> tuple[str, float]:
    """
         Finds the name and the highest absolute magnitude
          of an asteroid and returns it as a tuple
         :return:
             tuple[str, float]
    """
    return tuple(get_data_by_operation_column_val(
        data=data,
        column_to_compare_by_name=ABSOLUTE_MAGNITUDE,
        columns=[NAME, ABSOLUTE_MAGNITUDE], operation_type=MAX))


def closest_to_earth(data: np.array) -> str:
    """
         Finds the name and the lowest Miss Distance
         of an asteroid and returns it as a tuple
         :return:
             tuple[str, float]
    """
    return get_data_by_operation_column_val(
        data=data,
        column_to_compare_by_name=MISS_DISTANCE_KM,
        columns=[NAME], operation_type=MIN)[0]


def common_orbit(data) -> dict:
    """
         Returns a dict where the key is the Orbit ID and the
         value is the amount of asteroids with that id.
         :return:
             dict[int,int]
    """
    return get_count_by_column_name(data=data, column_name=ORBIT_ID)


def plot_data(data, bins: int, title: Optional[str] = None,
              x_label: Optional[str] = None,
              y_label: Optional[str] = None,
              color: str = COLOR_BLUE,
              edge_color=COLOR_BLACK,
              plot_range: Optional[tuple] = None) -> None:
    """
         A helper function that plots data.
         :return:
             None
    """
    plt.hist(x=data, bins=bins, color=color,
             edgecolor=edge_color, range=plot_range)

    if title is not None:
        plt.title(label=title)

    if x_label is not None:
        plt.xlabel(xlabel=x_label)

    if y_label is not None:
        plt.ylabel(ylabel=y_label)

    plt.show()


def plt_hist_common_orbit(data) -> None:
    """
         Plots a histogram of the amount of asteroids in each Orbit ID
         :return:
             None
    """
    common_orbit_dict = common_orbit(data=data)
    plot_data(data=common_orbit_dict, bins=6, title="Orbit ID count",
              x_label="Orbit ID",
              y_label="Count")


def plt_hist_diameter(data) -> None:
    """
         Plots a histogram of the amount of asteroids in each average diameter
         :return:
             None
    """
    name_column = get_column_values_by_name(
        data=data,
        column_names=[NAME],
        data_type=INT)
    average_mean_column = get_mean_by_column_names(
        data=data,
        column_names=[EST_DIA_IN_KM_MIN,
                      EST_DIA_IN_KM_MAX])
    plot_dict = dict(zip(name_column.flatten(), average_mean_column))
    plot_data(data=plot_dict, bins=10, title="Asteroids Diameter Count",
              x_label="Diameter",
              y_label="Count")


def get_column_values_by_name(data, column_names: list[str],
                              data_type: Optional[str] = FLOAT) -> np.array:
    """
         Extracts column values by their given names
         :return:
             numpy.array
    """
    header = data[0]
    col_indexes = get_column_indexes_by_names(header=header,
                                              column_names=column_names)
    return extract_column_values(data=data,
                                 column_indexes=col_indexes,
                                 data_type=data_type)


def get_count_by_column_name(data, column_name: str, data_type: str = FLOAT,
                             key_cast: type = int) -> dict:
    """
         Returns a dict with the key as a column value and
         the value as it's count
         :return:
             dict
    """
    column = get_column_values_by_name(data=data,
                                       column_names=[column_name],
                                       data_type=data_type)
    column_set = set(column.flatten())
    count_dict = dict()
    for value in column_set:
        values_sum = np.sum(column == value).astype(int)
        count_dict[key_cast(value)] = int(values_sum)
    return count_dict


def get_mean_by_column_names(data, column_names: list[str]) -> float:
    """
         Calculates the mean value of either one column or of a list of columns
         :return:
             float
    """
    columns = get_column_values_by_name(data=data, column_names=column_names)
    if columns.shape[1] == 1:
        return columns.mean()
    return columns.mean(axis=1)


def min_max_diameter(data) -> tuple[float, float]:
    """
         Calculates the mean of the min diameter and max diameter
         and returns it as tuple
         :return:
             tuple[float, float]
    """
    dia_in_km_min = float(get_mean_by_column_names(
        data=data,
        column_names=[EST_DIA_IN_KM_MIN]))
    dia_in_km_max = float(get_mean_by_column_names(
        data=data,
        column_names=[EST_DIA_IN_KM_MAX]))
    return dia_in_km_min, dia_in_km_max


def plt_pie_hazard(data) -> None:
    """
        Plots a pie chart of the % of Hazardous and Non Hazardous Asteroids
         :return:
             None
    """
    hazard_data = get_count_by_column_name(data=data,
                                           column_name=HAZARDOUS,
                                           data_type=STR, key_cast=str)
    updated_dict = {HAZARDOUS: hazard_data.get("True"),
                    NON_HAZARDOUS: hazard_data.get("False")}
    plt.pie(x=updated_dict.values(),
            labels=list(updated_dict.keys()),
            autopct="%1.1f%%")
    plt.title("Hazardous Asteroids")
    plt.show()


def plt_linear_motion_magnitude(data) -> None:
    """
        Plots linear regression relating to Absolute Magnitude
        and Miles Per Hour
        It appears that the lower the magnitude the faster the asteroid is.
         :return:
             None
    """
    absolute_magnitude_column = get_column_values_by_name(
        data=data, column_names=[ABSOLUTE_MAGNITUDE])
    miles_per_hour_column = get_column_values_by_name(
        data=data, column_names=[MILES_PER_HOUR])

    a, b, _, _, _ = stats.linregress(miles_per_hour_column.flatten(),
                                     absolute_magnitude_column.flatten())
    plt.scatter(miles_per_hour_column, absolute_magnitude_column)
    plt.plot(miles_per_hour_column, a * miles_per_hour_column + b)
    plt.ylabel(ABSOLUTE_MAGNITUDE)
    plt.xlabel(MILES_PER_HOUR)
    plt.title(f"{ABSOLUTE_MAGNITUDE} to {MILES_PER_HOUR}")
    plt.show()


def main() -> None:
    """
         The main function where all the magic happens
          :return:
              None
     """
    data = load_data(file_name="nasa.csv")
    plt_hist_diameter(data=data)
    plt_hist_common_orbit(data=data)
    plt_pie_hazard(data=data)
    plt_linear_motion_magnitude(data=data)


main()
