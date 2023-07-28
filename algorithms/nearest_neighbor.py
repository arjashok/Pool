import math

def distance(p1, p2):
    # in this case, we could replace the distance formula with an Google Maps API call
    # not sure how to factor rest of constraints as of rn
    return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

def create_distance_matrix(coordinates):
    # rn i am assuming NON-SYMMETRY in distance matrix
    # that is, the distance to go from a to b may not be the exact same as the distance to go from b to a
    # makes it more realistic, for instance suppose a highway is closed one way but not the other
    # however, API calls would currently be n(n-1)
    # assuming symmetry, API calls become n(n-1)/2
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

        # move driver to current nearest stop, add this stop to the order
        driver = nearest_stop
        order.append(driver)
        visited.add(driver)

    # add destination at the end, assures it is the last stop
    order.append(destination)
    return order

coordinates = [[4,4], [4,3], [2,4], [0,0], [2,2]]
distance_matrix = create_distance_matrix(coordinates)
print(distance_matrix)
check = nearest_neighbor(distance_matrix)
print(check)

