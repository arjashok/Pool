"""
    This file calculates the nearest neighbors given an n^2 matrix of distances
    between each person.
"""

# ------ Environment Setup ------ #
import math                         # distance calculations (temporary)
import pandas as pd                 # database (temporary)
import numpy as np                  # array manipulation
import matplotlib.pyplot as plt     # visualizing path


# ------ Wrapped Function ------ #
"""
    Final function that wraps all the auxiliary functions into one simple call
    that returns driver name as a `str` and order of pickup as a `list`. One
    wrapper function reduces the number of redundant calls we would have to
    make for loading data.
"""
def driver_selection(cluster: list) -> tuple[str, list]:
    # load data #
    firebase_df = pd.read_parquet(
        '../datasets/firebase.parquet',
        engine='fastparquet'
    )

    
    # push wrapped calls #



# ------ Auxiliary Functions for Distance ------ #
"""
    Temporary distance formula that relies on direct distance rather than time
    to drive the route between waypoints.

    This will eventually be replaced with a Google Maps API call, but for now
    we use this formula.
"""
def distance(p1: tuple, p2: tuple) -> float:
    # return Euclidean distance #
    return math.dist(p1, p2)


"""
    Assumed non-symmetry for distance (i.e weight, time between waypoints) to
    account for differing traffic levels, closures, etc. in the future. API
    calls will be n(n - 1) ==> O(n^2), but with symmetry they would become
    n(n - 1) / 2 ==> O(n^2).
"""
def create_distance_matrix(coordinates: np.ndarray) -> np.ndarray:
    # setup
    matrix = []
    n = len(coordinates)

    # apply distance
    for i in range(n):
        row = [0] * n
        for j in range(n):
            if i == j:
                continue
            dist = distance(coordinates[i], coordinates[j])
            row[j] = dist
        matrix.append(row)

    # return 2D
    return np.array(matrix)

    # # somehow this is more inefficient so wtf
    # # setup #
    # N = coordinates.shape[0]
    # distance_matrix = np.zeros((N, N))

    # for i in range(N):
    #     for j in range(N):
    #         if i == j:
    #             continue
    #         distance_matrix[i, j] = distance(coordinates[i], coordinates[j])

    # return distance_matrix


# ------ Auxiliary Functions for Testing ------ #
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
def rand_coordinates(num_coords: int) -> np.ndarray:
    # setup
    MULTIPLIER = 10

    # random x & y
    x_arr = np.random.uniform(-90 * MULTIPLIER, 90 * MULTIPLIER, num_coords)
    y_arr = np.random.uniform(-180 * MULTIPLIER, 180 * MULTIPLIER, num_coords)

    # return zipped array
    return np.array(list(zip(x_arr, y_arr)))


"""
    Visualizes the path using a basic 
"""
def visualize_path(coordinates: np.ndarray, order_indices: list):
    # setup #
    # order coordinates by path order
    ordered_coordinates = [coordinates[i] for i in order_indices]

    # extract values
    x_values, y_values = zip(*ordered_coordinates)


    # plotting #
    # setup plot & points
    plt.figure(figsize=(8, 6))
    plt.plot(x_values, y_values, marker='o', linestyle='-', color='b', markersize=8)

    # labels
    plt.text(x_values[0], y_values[0], 'Start', ha='right', va='bottom', fontsize=12, weight='bold')
    plt.text(x_values[-1], y_values[-1], 'End', ha='left', va='top', fontsize=12, weight='bold')
    plt.xlabel('X-coordinate')
    plt.ylabel('Y-coordinate')
    plt.title('Path Visualization')
    plt.grid(True)

    # show plot & save
    plt.savefig("../datasets/path.png", dpi=100)
    plt.show()


# ------ Auxiliary Functions for Driver Selection ------ #
"""
    Given a narrowed dataframe of only the relevant driver rows, this utility
    calculates the final driver weights according to the formula we have custom
    derived for this purpose.

    The final weights are meant to be applied as a proportional constant to the
    distance for the paths calculated for each potential driver. For
    non-drivers, this proportion will be `inf` since the lower the proportion,
    the lower the total "cost" is deemed to be and therefoer the higher the
    favorability to be driver is.
"""
def driver_weights(driver_data: pd.DataFrame) -> np.ndarray:
    # setup #
    # constants
    num_drivers = driver_data.shape[0]

    # formula variables
    alpha = np.array([1] * num_drivers)                     # constant multiplier
    gas_mileage = 1 / driver_data['gas_mileage']            # miles per gallon
    preference = driver_data['pref_to_drive']               # driving preference
    exhaustion = (driver_data['driving_instances'] + 1) \
                 / (driver_data['num_trips'] + 1)           # driving instances / num trips
    


    # calculations #
    return 


# ------ Nearest Neighbors Calculation ------ #
"""
    Uses a heuristic to calculate who the driver should be within each cluster
    and therefore what the order of pickup should be (optimally).
"""
def nearest_neighbor(distance_matrix: np.ndarray) -> list:
    # roughly O(n^2) runtime, lmk if u guys have ideas to optimize
    num_stops = len(distance_matrix)
    destination = num_stops - 1
    
    # driver must be the furthest from destination
    driver = max(range(num_stops - 1), key=lambda stop: distance_matrix[stop][destination])

    order = [driver]
    visited = set([driver])
    
    # continue visiting until all stops except destination have been visited
    while len(visited) < num_stops - 1:
        nearest_stop = None
        nearest_dist = float('inf')

        # last index will always be destination, avoid checking this
        for stop in range(num_stops - 1):
            if stop not in visited:
                dist = distance_matrix[driver][stop]
                if dist < nearest_dist:
                    nearest_stop = stop
                    nearest_dist = dist

        driver = nearest_stop
        order.append(driver)
        visited.add(driver)

    # add destination at the end, assures it is the last stop
    order.append(destination)
    return order


# ------ Test Script ------ #
if __name__ == "__main__":
    driver_selection(cluster=['monkey noah monkey, cococruncher noah, yash, arjun'])
