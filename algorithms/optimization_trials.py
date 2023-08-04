"""
    Utility file that generates random data to measure time and space
    complexity of the POOL Algorithm.
"""

# ------ Environment Setup ------ #
# static libraries
import numpy as np                          # array manipulation
import pandas as pd                         # db manipulation
import time

# experimentation libraries
from pool import pool                       # wrapped function for POOL API call
from database import *                      # database ops
from distance import *                      # underlying distance calculations


# ------ Trials for Database Performance ------ #
"""
    Tests the write & read speed for the database being employed. Parameters
    can be set to dictate the ~probability of a column to store strings.
"""
def trial_db_perf(num_data_points: int, num_cols: int, prop: int) -> float:
    # generate data #
    # setup
    threshold = prop / 100.0
    columns = trial_rand_strings(num_cols)
    types = np.random.random(num_cols) <= threshold

    rand_df = pd.DataFrame()

    # fill data
    for col_name, type in zip(columns, types):
        # random
        if type:
            col = trial_rand_strings(num_data_points)
        else:
            col = trial_rand_coordinates(num_data_points)
        
        # add column
        rand_df[col_name] = col
    

    # time performance #
    start_time = time.time()

    # modify db
    db_modify_users(rand_df)

    # load back db
    db = db_load()

    # query db
    # TODO:

    # results
    exec_time = time.time() - start_time
    print(
        "Modifying, saving, loading, and querying the db took ",
        f"{exec_time} seconds"
    )

    # return
    return exec_time


# ------ Auxiliary Functions for Time & Space Trials ------ #
"""
    Create a list of randomly generated coordinates, assuming within a certain
    radius from one another. Since coordinates are domained as follows:
        latitude: [-90, 90]
        longitude: [-180, 180]
    We will be using a multiplier to artifically boost range while maintaing a
    static variable type of `float`. This multiplier is 10 for now since
    coordinates only need 6 decimals of precision to be very accurate, while
    floats in python can hold up to 8 digits of precision.
"""
def trial_rand_coordinates(num_coords: int) -> np.ndarray:
    # setup
    MULTIPLIER = 10

    # random x & y
    x_arr = np.random.uniform(-90 * MULTIPLIER, 90 * MULTIPLIER, num_coords)
    y_arr = np.random.uniform(-180 * MULTIPLIER, 180 * MULTIPLIER, num_coords)

    # return zipped array
    return np.array(list(zip(x_arr, y_arr)))


"""
    Generates a random list of strings for use as data, column names, etc. This
    assumes a max number of 720 unique strings need to be created.
"""
def trial_rand_strings(num_strings: int) -> list:
    # setup
    chars = "abcdefghijklmnopqrstuvwxyz"
    characters = list(chars)

    # random sample
    strings = [
        ''.join(np.random.choice(characters, size=6)) for _ in range(num_strings)
    ]
    return strings


# ------ Auxiliary Functions for Time & Space Trials ------ #
"""
    Run the optimization trials.
"""
if __name__ == "__main__":
    # write which trials to perform
    trial_db_perf(100000)


