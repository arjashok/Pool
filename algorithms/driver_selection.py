"""
    This function dispatches the corresponding driver selection algorithm as
    specified.

    Approaches:
    ::::: Traveling Salesman w/ Cycle, Reversed & Cut :::::
        TSP from the destination to destination (cycle), remove the duplicate
        destination node and reverse the order to find the roughly optimized
        path order. Ensure that the edges from the destination out are
        weighted while the edges from the person nodes in are 0-weighted such
        that the weight of the last edge doesn't influence the order of
        pickup (for the last node, the weight of the edge may affect who is
        picked up last otherwise, so the furthest driver will be least likely
        to be the driver, which is usually not optimal).
        
    ::::: Brute-Force Permutation w/ Dynamic Programming Approach :::::
        Generating all possible paths and orders and simply choose the path
        that minimizes the total weight of the path driven. Given that
        clustering GUARANTEES an O(1) size problem for the >50 case, we can
        ensure that this appraoch that normally takes O(n!*k) for n nodes and k
        clusters will be O(k) where k is the number of clusters.
"""


# ------ Environment Setup ------ #
# static libraries
from sklearn.cluster import KMeans                  # clustering
from scipy.optimize import linear_sum_assignment    # magic function lol
import numpy as np                                  # arrays
import itertools                                    # iteration

# temporary, testing
import math                                         # distance
from scipy.spatial.distance import cdist            # Euclidean distance
import matplotlib.pyplot as plt                     # visualizing
import pandas as pd                                 # dataframe
from cost_testing import *                          # testing purposes
from corporate_clustering import *                  # clustering help


# ------ Brute-Force Permutation ------ #



# ------ TSP Algo ------ #


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
    Auxiliary function to allow for triangular-matrix space optimization. Since
    variables are auto passed by reference in python unless acted on by a
    non-in-place manner, we can assume some efficiency.
"""
def get_dist(coordinates: np.ndarray, row: int, col: int) -> float:
    # check direct access
    if row >= col:
        return coordinates[row, col]
    
    # indirect access
    return coordinates[col, row]


"""
    Assumed non-symmetry for distance (i.e weight, time between waypoints) to
    account for differing traffic levels, closures, etc. in the future. API
    calls will be n(n - 1) ==> O(n^2), but with symmetry they would become
    n(n - 1) / 2 ==> O(n^2).

    UPDATE: we are now switching to a symmetric approach to ensure undirected
    edges when clustering and finding optimal driver
"""
def create_distance_matrix(coordinates: np.ndarray) -> np.ndarray:
    # setup
    n = coordinates.shape[0]
    matrix = [[0] * i for i in range(1, n + 1)]

    # get all distances
    for i in range(n):
        for j in range(0, i):
            dist = distance(coordinates[i], coordinates[j])
            matrix[i, j] = dist

    # return 2D
    return np.array(matrix)


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
    exhaustion = (driver_data["trips_driven"]) / (
        driver_data["trips_taken"] + 1
    )                                                   # driving instances / num trips + 1
    rsvp_time = (
        1 / driver_data["rsvp_time"]
    )                                                   # time to rsvp as response_time / time_to_respond

    # calculations #
    return alpha * gas_mileage * preference * exhaustion * rsvp_time
