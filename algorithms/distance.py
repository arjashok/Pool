"""
    Utility file for all functions relating to distance and distance
    calculations. Eventually, we will be replacing the Euclidean distance
    with API calls to Google Maps in order to provide more accurate times
    results. Clustering will still rely on Euclidean distance, however, to
    limit API calls for now.
"""


# ------ Environment Setup ------ #
# static libaries
import numpy as np                  # array manipulation

# temporary libraries
import math                         # distance calculations


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
    Finalized distance formula that relies on direct distance rather than time
    to drive the route between waypoints.

    This is for exclusive use in clustering to avoid order n-squared API calls
    where n is the population size, but in the future we may use API calls for
    this as well.
"""
def cluster_distance(p1: tuple, p2: tuple) -> float:
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

