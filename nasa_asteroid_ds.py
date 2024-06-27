from typing import Optional

import numpy as np

NAMES = ['Neo Reference ID', 'Name', 'Absolute Magnitude', 'Est Dia in KM(min)', 'Est Dia in KM(max)',
         'Est Dia in M(min)', 'Est Dia in M(max)', 'Est Dia in Miles(min)', 'Est Dia in Miles(max)',
         'Est Dia in Feet(min)', 'Est Dia in Feet(max)', 'Close Approach Date', 'Epoch Date Close Approach',
         'Relative Velocity km per sec', 'Relative Velocity km per hr', 'Miles per hour', 'Miss Dist.(Astronomical)',
         'Miss Dist.(lunar)', 'Miss Dist.(kilometers)', 'Miss Dist.(miles)', 'Orbiting Body', 'Orbit ID',
         'Orbit Determination Date', 'Orbit Uncertainity', 'Minimum Orbit Intersection', 'Jupiter Tisserand Invariant',
         'Epoch Osculation', 'Eccentricity', 'Semi Major Axis', 'Inclination', 'Asc Node Longitude', 'Orbital Period',
         'Perihelion Distance', 'Perihelion Arg', 'Aphelion Dist', 'Perihelion Time', 'Mean Anomaly', 'Mean Motion',
         'Equinox', 'Hazardous\n']


def load_data(file_name: str):
    data = np.genfromtxt(fname=file_name, delimiter=",", dtype=str)
    return data


def scoping_data(data: np.ndarray, names: Optional[list[str]] = None):
    if names is None:
        names = NAMES
    index = np.argmax(data == names)
    mask = np.arange(data.shape[0]) != index
    new_data = data[mask]
    return new_data


def main():
    data = load_data(file_name="nasa.csv")
    print(f'{data=}')
    scoped_data = scoping_data(data=data)
    print(f"{scoped_data=}")


main()
