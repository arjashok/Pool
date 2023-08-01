"""
    coconut crunching vine-swinging fish catching super-phaser clinical
    optimization algorithm (volatile).
"""

from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from scipy.optimize import linear_sum_assignment
import numpy as np

coords = np.array([(0,0), (1,1), (1,0), (6,0), (8,0), (7,1), (5,4), (4,5), (1,2)])


def get_even_clusters(X, cluster_size):
    n_clusters = int(np.ceil(len(X)/cluster_size))
    kmeans = KMeans(n_clusters)
    kmeans.fit(X)
    centers = kmeans.cluster_centers_
    centers = centers.reshape(-1, 1, X.shape[-1]).repeat(cluster_size, 1).reshape(-1, X.shape[-1])
    distance_matrix = cdist(X, centers)
    clusters = linear_sum_assignment(distance_matrix)[1]//cluster_size
    return clusters

def group(arr, coords, cluster_size):
    num_clusters = int(np.ceil(len(coords)/cluster_size))
    rv = []
    for i in range(num_clusters):
        rv.append([])
    idx = 0
    for i in arr:
        rv[i].append(list(coords[idx]))
        idx += 1
    return rv

print(coords)
check = get_even_clusters(coords, 3)
hi = group(check, coords, 3)
print(hi)