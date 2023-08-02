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

# A wrapping function to make functions calls less repetitive
def cluster(coords, cluster_size):
    into_clusters = get_even_clusters(coords, cluster_size)
    return group(into_clusters, coords, cluster_size)

# A high level explanation of how this works (Arjun make this look amazing pls)
# The approach is essentially to use sklearns K-Means Clustering to find the CENTROIDS
# that best represent the data
# The idea from there is to create a one-to-one mapping from a point to its closest centroid
# This is done first by repeating each centroid cluster_size time, such that a maximum 
# of cluster_size points can be mapped to a point
# A distance matrix is then created from each point to each centroid
# From there, linear sum assignment is used. Through this process, the optimal minimizing combination of 
# points are associated with a centroid (This has O(n^3) runtime)
# Remember, we repeated clusters. Therefore to remove the repeats and find the overall cluster
# A point belongs to, perform floor division
# The runtime associated with linear sum assignment is the dominant term
# meaning overall runtime is approx O(n^3)
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

# Uses the information from get_even_clusters to actually cluster the coords array
def group(arr, coords, cluster_size):
    num_clusters = int(np.ceil(len(coords) / cluster_size))
    rv = [[] for num in range(num_clusters)]
    for idx, i in enumerate(arr):
        rv[i].append(coords[idx])
    return np.array(rv)


