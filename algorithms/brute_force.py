import math
from cost_testing import *
import matplotlib.pyplot as plt
import numpy as np
import itertools
import time

def distance(p1, p2):
    return math.dist(p1, p2)

def find_path_distance(arr, cache):
    rv = 0
    for i in range(len(arr) - 1):
        if (arr[i], arr[i + 1]) not in cache:
            dist = distance(arr[i], arr[i + 1])
            cache[(arr[i], arr[i + 1])] = dist
            rv += dist
        else:
            rv += cache[(arr[i], arr[i + 1])]
    return rv

def brute_force(coordinates):
    cache = {}
    permutations = itertools.permutations(coordinates[:-1])
    min_distance = float('inf')
    optimal_path = []
    for path in permutations:
        path = list(path)
        path.append(coordinates[len(coordinates) - 1])
        curr_distance = find_path_distance(path, cache)
        if curr_distance < min_distance:
            min_distance = curr_distance
            optimal_path = path
    return optimal_path

if __name__ == "__main__":
    start_time = time.time()
    coords = [(5,6), (2,5), (3,10), (11,2), (7,4), (8,3), (5,5), (9,9), (0,11), (0,0)]
    path = brute_force(coords)
    #print(path)
    visualize_path(path)
    print("--- %s seconds ---" % (time.time() - start_time))
