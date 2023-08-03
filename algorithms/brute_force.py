import math
from cost_testing import *
import matplotlib.pyplot as plt
import numpy as np
import itertools

def distance(p1, p2):
    return math.dist(p1, p2)

def find_path_distance(arr):
    rv = 0
    for i in range(len(arr) - 1):
        rv += distance(arr[i], arr[i + 1])
    return rv

def brute_force(coordinates):
    permutations = itertools.permutations(coordinates[1:-1])
    min_distance = float('inf')
    optimal_path = []
    for path in permutations:
        path = list(path)
        path.append(coordinates[len(coordinates) - 1])
        path.insert(0, coordinates[0])
        curr_distance = find_path_distance(path)
        if curr_distance < min_distance:
            min_distance = curr_distance
            optimal_path = path
    return optimal_path

if __name__ == "__main__":
    coords = rand_coordinates(5)
    print(np.array(coords))
    path = brute_force(coords)
    print(np.array(path))
    visualize_path(path)
