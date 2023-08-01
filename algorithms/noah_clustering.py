"""
    coconut crunching vine-swinging fish catching super-phaser clinical
    optimization algorithm (volatile).
"""

from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
import numpy as np
from cost_testing import rand_coordinates, visualize_clusters, visualize_path
from nearest_neighbor import nearest_neighbor, create_distance_matrix


def get_even_clusters(X, cluster_size):
    n_clusters = int(np.ceil(len(X) / cluster_size))
    kmeans = KMeans(n_clusters)
    kmeans.fit(X)
    centers = kmeans.cluster_centers_
    centers = (
        centers.reshape(-1, 1, X.shape[-1])
        .repeat(cluster_size, 1)
        .reshape(-1, X.shape[-1])
    )
    distance_matrix = cdist(X, centers)
    clusters = linear_sum_assignment(distance_matrix)[1] // cluster_size
    return clusters


def group(arr, coords, cluster_size):
    num_clusters = int(np.ceil(len(coords) / cluster_size))
    rv = []
    for i in range(num_clusters):
        rv.append([])
    idx = 0
    for i in arr:
        rv[i].append(list(coords[idx]))
        idx += 1
    return rv


coords = rand_coordinates(200)
print(coords)
check = get_even_clusters(coords, 5)
hi = group(check, coords, 5)
print(hi)
visualize_clusters(hi)
dmatrix = create_distance_matrix(hi[0])
path = nearest_neighbor(dmatrix)
visualize_path(hi[0], path)
