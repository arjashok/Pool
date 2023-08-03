"""
    This file calculates the nearest neighbors given an n^2 matrix of distances
    between each person when given a cluster of names.
"""

# ------ Environment Setup ------ #
import math                             # distance calculations (temporary)
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
def driver_selection(cluster: list) -> tuple[str, list]:
    # load data #
    firebase_df = pd.read_parquet(
        "../datasets/firebase.parquet",
        engine="fastparquet"
    )

    # execute wrapped calls #


# ------ Auxiliary Functions for Driver Selection ------ #


# ------ Nearest Neighbors Calculation ------ #
"""
    Uses a heuristic to calculate who the driver should be within each cluster
    and therefore what the order of pickup should be (optimally).
"""
def nearest_neighbor_order(distance_matrix: np.ndarray) -> list:
    # roughly O(n^2) runtime, lmk if u guys have ideas to optimize
    num_stops = len(distance_matrix)
    destination = num_stops - 1

    # driver must be the furthest from destination
    driver = max(
        range(num_stops - 1),
        key=lambda stop: distance_matrix[stop][destination]
    )

    order = [driver]
    visited = set([driver])

    # continue visiting until all stops except destination have been visited
    while len(visited) < num_stops - 1:
        nearest_stop = None
        nearest_dist = float("inf")

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

# Instead of returning the intended order, return the points in order. Same logic as previous
def nearest_neighbor(distance_matrix: np.ndarray, coordinates: np.ndarray) -> list:
    num_stops = len(distance_matrix)
    destination = num_stops - 1
    driver = max(
        range(num_stops - 1),
        key=lambda stop: distance_matrix[stop][destination]
    )
    order = [coordinates[driver]]
    visited = set([driver])
    while len(visited) < num_stops - 1:
        nearest_stop = None
        nearest_dist = float("inf")
        for stop in range(num_stops - 1):
            if stop not in visited:
                dist = distance_matrix[driver][stop]
                if dist < nearest_dist:
                    nearest_stop = stop
                    nearest_dist = dist

        driver = nearest_stop
        order.append(coordinates[driver])
        visited.add(driver)
    order.append(coordinates[destination])
    return np.array(order)


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
