"""
    This file calculates the nearest neighbors given an n^2 matrix of distances
    between each person when given a cluster of names.
"""

# ------ Environment Setup ------ #
import numpy as np                          # array manipulation
import matplotlib.pyplot as plt             # visualizing path


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
    Visualizes the path using a basic plotting approach. Order is set by the
    results of the algorithm.
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


"""
    Visualizes all the clusters created.
"""
def visualize_clusters(clusters: list) -> None:
    

