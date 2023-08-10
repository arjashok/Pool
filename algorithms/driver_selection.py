"""
    All functionality for selecting a driver from a pre-clustered group of
    drivers.

    ::::::::::::::::::::::::::::::: Approaches ::::::::::::::::::::::::::::::::
    # -- Traveling Salesman w/ Cycle, Reversed & Cut -- #
    TSP from the destination to destination (cycle), remove the duplicate
    destination node and reverse the order to find the roughly optimized path
    order. Ensure that the edges from the destination out are weighted while
    the edges from the person nodes in are 0-weighted such that the weight of
    the last edge doesn't influence the order of pickup (for the last node, the
    weight of the edge may affect who is picked up last otherwise, so the
    furthest driver will be least likely to be the driver, which is usually not
    optimal).
        
    # -- Brute-Force Permutation w/ Dynamic Programming Approach -- #
    Generating all possible paths and orders and simply choose the path that
    minimizes the total weight of the path driven. Given that clustering
    GUARANTEES an O(1) size problem for the >50 case, we can ensure that this
    appraoch that normally takes O(n!*k) for n nodes and k clusters will be
    O(k) where k is the number of clusters.

    # -- Nearest Neighbors w/ Heuristics -- #
    Uses a heuristic to calculate who the driver should be within each cluster
    and therefore what the order of pickup should be (optimally). The heuristic
    used is based on minimizing the number of deviations the driver faces on
    the way to the destination while picking up people, essentially limiting
    the distance by virtue of reducing the distance to destination during the
    pickup process. This is done by selecting the furthest driver from the
    destination.
"""


# ------ Environment Setup ------ #
# static libraries
from sklearn.cluster import KMeans                  # clustering
from scipy.optimize import linear_sum_assignment    # magic function lol
import numpy as np                                  # arrays
import itertools                                    # iteration
from distance import *                              # all distance functionality
from database import *                              # all database functionality

# temporary, testing
import matplotlib.pyplot as plt                     # visualizing
import pandas as pd                                 # dataframe


# ------ Dispatch ------ #
"""
    This function dispatches the chosen method and returns the selected driver
    and the order of pickup given a cluster of user IDs.
"""
def driver_selection(cluster_db: pd.DataFrame) -> list:
    # get params #
    coords = cluster_db["location-coords"]
    dist_matrix = create_distance_matrix(coords)
    driv_weights = driver_weights(driver_data=cluster_db)

    # dispatch #
    # NOTE: for now, nn for testing purposes while this file is in construction
    return driver_selection_nn(
        distance_matrix = dist_matrix,
        coordinates = coords,
        weights = driv_weights
    )


# ------ Brute-Force Permutation ------ #
"""
    Wrapper function for the dynamic-programmming brute-force approach towards
    driver-selection within a constant size cluster.

    TODO: implement weighting for the driver likelihood
"""
def driver_selection_dp(coords: np.ndarray, distance_matrix: np.ndarray) -> list:
    # setup #
    # distance matrix
    # distance_matrix = create_distance_matrix(coords)

    # consider all permutations
    permutations = itertools.permutations(range(len(coords) - 1))


    # get minimum path distance #
    # storage
    min_distance = float('inf')
    optimal_path = []

    # for each possible path
    for path in permutations:
        # consider current path
        path = list(path)
        path.append(len(coords) - 1)
        cur_distance = find_path_distance(distance_matrix, path)

        # choose min
        if cur_distance < min_distance:
            min_distance = cur_distance
            optimal_path = path

    # return optimal
    return optimal_path


"""
    Auxiliary function for finding the distance between two coordinates in the
    cluster.
"""
def find_path_distance(distance_matrix: np.ndarray, indices: list) -> float:
    # return path distance #
    dist_traveled = 0
    for i in range(len(indices) - 1):
        dist_traveled += get_dist(distance_matrix, indices[i], indices[i + 1])
    return dist_traveled


# ------ TSP Algo & Reversing ------ #
"""
    Wrapper function for Traveling Salesman from destination to destination.
"""
def driver_selection_tsp(cluster: np.ndarray) -> list:
    pass


# ------ Nearest Neighbors & Heuristics ------ #
"""
    Uses a heuristic to calculate who the driver should be within each cluster
    and therefore what the order of pickup should be (optimally).

    Instead of returning the intended order, return the points in order.
"""
def driver_selection_nn(distance_matrix: np.ndarray, coordinates: np.ndarray, weights: dict) -> list:
    # setup #
    # variable declaration
    num_stops = len(distance_matrix)
    destination = num_stops - 1

    driver = max(
        range(num_stops - 1),
        key=lambda stop: get_dist(distance_matrix, stop, destination) * weights[stop]
    )
    
    # setup order tracking
    order = [coordinates[driver]]
    visited = set([driver])
    
        
    # find order #
    # while there are people to be picked up
    while len(visited) < num_stops - 1:
        # setup next stop
        nearest_stop = None
        nearest_dist = float("inf")
            
        # check each stop for nearest
        for stop in range(num_stops - 1):
            if stop not in visited:
                dist = get_dist(distance_matrix, driver, stop)
                if dist < nearest_dist:
                    nearest_stop = stop
                    nearest_dist = dist

        # store nearest stop & update trackers
        driver = nearest_stop
        order.append(coordinates[driver])
        visited.add(driver)
    
    # add destination
    order.append(coordinates[destination])


    # return final ordering #
    return order


# ------ Auxiliary Functions for Selection ------ #
"""
    Given a narrowed dataframe of only the relevant driver rows, this utility
    calculates the final driver weights according to the formula we have custom
    derived for this purpose.

    The final weights are meant to be applied as a proportional constant to the
    distance for the paths calculated for each potential driver. For
    non-drivers, this proportion will be `inf` since the lower the proportion,
    the lower the total "cost" is deemed to be and therefoer the higher the
    favorability to be driver is.

    TODO: STILL WORK IN PROGRESS. Formula is almost finalized, just need to
    transfer implementation
"""
def driver_weights(driver_data: pd.DataFrame) -> dict:
    # setup #
    # constants
    DRIVERS = driver_data.shape[0]
    MILEAGE = 1
    RSVP = 1
    PREF = 1
    EXHAUSTION = 1
    ALPHA = MILEAGE * RSVP * PREF * EXHAUSTION

    # formula variables
    alpha = np.array([ALPHA] * DRIVERS)                 # constant multiplier
    gas_mileage = 1 / driver_data["gas_mileage"]        # miles per gallon
    preference = 1 / driver_data["pref_to_drive"]       # driving preference
    exhaustion = (driver_data["trips_driven"] \
                  + driver_data["miles_driven"]) \
                  / (driver_data["trips_taken"] + 1
    )                                                   # driving instances / num trips + 1
    rsvp_time = (
        1 / driver_data["rsvp_time"]
    )                                                   # time to rsvp as response_time / time_to_respond


    # calculations #
    driver_coords = driver_data["location-coords"]
    raw_weights = alpha * gas_mileage * preference * exhaustion * rsvp_time
    weights = dict(zip(driver_coords, raw_weights))

    return weights

