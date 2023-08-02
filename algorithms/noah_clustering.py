"""
    This model is the highly theoretical coconut crunching vine-swinging fish
    catching super-phaser clinical optimization algorithm (volatile) with
    back-propogating colonialization vision hinderance implemented in
    conjunction with the gold-digger hyderabadi pollution decleanser ritual.

    Has Einstein himself even understood what lies below? Possibly, but he once
    told the authors of this algorithm that the real genius lies in the friends
    we made along the way.
"""

# ----- Environment Setup ----- #
from sklearn.cluster import KMeans                  # clustering
from scipy.spatial.distance import cdist            # Euclidean distance
from scipy.optimize import linear_sum_assignment    # magic function lol
import numpy as np                                  # arrays
from cost_testing import *                          # testing purposes
from nearest_neighbor import *                      # distance


# ------ Clustering ------ #
"""
    A wrapping function to make functions calls less repetitive in the final
    app deployment.
"""
def cluster(coords, cluster_size):
    into_clusters = get_even_clusters(coords, cluster_size)
    return group(into_clusters, coords, cluster_size)


"""
    High-level explanation:
        The approach is essentially to use sklearns K-Means Clustering to find
        the CENTROIDS that best represent the data. The idea from there is to
        create a one-to-one mapping from a point to its closest centroid. This
        is done first by repeating each centroid cluster_size time, such that a
        maximum of cluster_size points can be mapped to a point.
        
        A distance matrix is then created from each point to each centroid.
        From there, linear sum assignment is used. Through this process, the
        optimal minimizing combination of points are associated with a centroid
        (This has O(n^3) runtime).
        
        Remember, we repeated clusters. Therefore to remove the repeats and
        find the overall cluster a point belongs to, perform floor division.
        The runtime associated with linear sum assignment is the dominant term
        meaning overall runtime is approx O(n^3).
"""
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


"""
    Uses the information from get_even_clusters to actually cluster the coords
    array.
"""
def group(arr, coords, cluster_size):
    num_clusters = int(np.ceil(len(coords) / cluster_size))
    rv = [[] for num in range(num_clusters)]
    for idx, i in enumerate(arr):
        rv[i].append(coords[idx])
    return np.array(rv)


"""
    Run as a script for testing purposes.
"""
if __name__ == "__main__":    
    coords = rand_coordinates(200)
    print(coords)
    check = get_even_clusters(coords, 5)
    hi = group(check, coords, 5)
    print(hi)
    visualize_clusters(hi)
    dmatrix = create_distance_matrix(hi[0])
    path = nearest_neighbor(dmatrix)
    visualize_path(hi[0], path)
