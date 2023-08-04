"""
    This file calculates the nearest neighbors given an n^2 matrix of distances
    between each person when given a cluster of names.
"""

# ------ Environment Setup ------ #
import pandas as pd                     # database (temporary)
import numpy as np                      # array manipulation
import matplotlib.pyplot as plt         # visualizing path
from cost_testing import *              # testing the costs & approaches
from corporate_clustering import *      # full process


# ------ Wrapped Function ------ #
"""
    Final function that wraps all the auxiliary functions into one simple call
    that returns driver name as a `str` and order of pickup as a `list`. One
    wrapper function reduces the number of redundant calls we would have to
    make for loading data.
"""


"""
    Full process.
"""
def cluster_and_order(coords):
    clustered = cluster(coords, 5)
    rv = []
    for i in clustered:
        distance_matrix = create_distance_matrix(i)
        rv.append(nearest_neighbor(distance_matrix, i))
    return np.array(rv)


# ------ Test Script ------ #
if __name__ == "__main__":
    coords = rand_coordinates(20)
    check = cluster_and_order(coords)
    print(check)
    for i in check:
        visualize_path(i)
