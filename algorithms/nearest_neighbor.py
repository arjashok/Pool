"""
    This file calculates the nearest neighbors given an n^2 matrix of distances
    between each person.
"""

# ------ Environment Setup ------ #
import math                         # distance calculations
import numpy as np                  # array manipulation


# ------ Auxiliary Functions ------ #
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
def create_distance_matrix(coordinates: list) -> list:
    matrix = []
    n = len(coordinates)
    for i in range(n):
        row = [0] * n
        for j in range(n):
            if i == j:
                continue
            dist = distance(coordinates[i], coordinates[j])
            row[j] = dist
        matrix.append(row)
    return matrix


"""
    Create a list of randomly generated coordinates, assuming within a certain
    radius from one another.
"""



# ------ Nearest Neighbors Calculation ------ #
"""
"""
def nearest_neighbor(distance_matrix):
    # roughly O(n^2) runtime, lmk if u guys have ideas to optimize
    num_stops = len(distance_matrix)
    destination = num_stops - 1
    
    # driver must be the furthest from destination
    # peep the lambda function
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
    # build random coords #
    coordinates = [[0, 0], [2, 0], [4,4], [4, 1], [1,1]]
    distance_matrix = create_distance_matrix(coordinates)
    print(distance_matrix)
    check = nearest_neighbor(distance_matrix)
    print(check)

