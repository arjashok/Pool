import math
from cost_testing import *
import matplotlib.pyplot as plt
import numpy as np
import itertools
from corporate_clustering import *



def distance(p1, p2):
    return math.dist(p1, p2)

def create_distance_matrix(coordinates: np.ndarray) -> np.ndarray:
    # setup
    n = len(coordinates)

    # apply distance
    matrix = np.zeros((n, n))  # Initialize the matrix with zeros

    for i in range(n):
        for j in range(n):
            if i == j:
                continue
            dist = distance(coordinates[i], coordinates[j])
            matrix[i, j] = dist
            matrix[j, i] = dist  # Assign the same value to the symmetric element

    # return 2D
    return matrix


def find_path_distance(distance_matrix, indices):
    rv = 0
    for i in range(len(indices) - 1):
        rv += distance_matrix[indices[i]][indices[i + 1]]
    return rv
    

def brute_force(coordinates):
    distance_matrix = create_distance_matrix(coordinates)
    permutations = itertools.permutations(range(len(coordinates) - 1))
    min_distance = float('inf')
    optimal_path = []
    for path in permutations:
        path = list(path)
        path.append(len(coordinates) - 1)
        curr_distance = find_path_distance(distance_matrix, path)
        if curr_distance < min_distance:
            min_distance = curr_distance
            optimal_path = path
    return optimal_path

def cluster_and_order(coordinates):
    clustered = cluster(coordinates, 5)
    rv = []
    for i in clustered:
        path = brute_force(i)
        rv.append([i[idx] for idx in path])
    return np.array(rv)

def visualize_paths(paths):
    plt.figure()
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for idx, path in enumerate(paths):
        x = [point[0] for point in path]
        y = [point[1] for point in path]
        plt.plot(x, y, color=colors[idx % len(colors)], marker='o', label=f'Path {idx+1}')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Visualizing Paths')
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    coords = rand_coordinates(40)

