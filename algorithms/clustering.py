"""
    This algorithm will utilize a form of K-Means Clustering to group people
    together in the most optimal way to minimize total distance driven.

    ::::::::::::::::::::::::::::::: Approaches ::::::::::::::::::::::::::::::::
    # -- K-Means w/ Post-Processing -- #
    The first iteration of this algorithm will make the assumption that no one
    would want to pickup more than ~3 other people, for a total of 4 per car. 
    While this doesn't optimize for the number of people driving, it saves the
    most time across the board and doesn't burden one person who has a car that
    fits more people from always picking up more and therefore driving more.

    Clustering will be done without weights, our only goal right now is to
    control distances and reduce the size of the problem for driver selection.

    Distance here will be straight-line Euclidean distance to avoid excessive
    order n^2 API calls. The results may not always be optimal, but it will
    minimize miles driven on average and therefore, by some non-constant
    proportion, time.

    This model is the highly theoretical coconut crunching vine-swinging fish
    catching super-phaser clinical optimization algorithm (volatile) with
    back-propogating colonialization vision hinderance implemented in
    conjunction with the gold-digger hyderabadi pollution decleanser ritual.

    Has Einstein himself even understood what lies below? Possibly, but he once
    told the authors of this algorithm that the real genius lies in the friends
    we made along the way.

    This is the specialized clustering for groups of 50+ people.
    
    # -- Clustering via Driver Selection -- #
    This is the specialized clustering for groups of 1 - 49 people.
    
    The assumption we can make with groups of 49 and below people is that car
    size and number of drivers matters much more. The 50+ algorithm limits the
    capacity for valid reasons, but for smaller test-cases (such as a 7-person
    group, one driver with 7-person car) the algorithm completeley fails. While
    this is an edge case, the possibility of an incorrect solution, or even
    worse the inability to produce any solution, drives a need for another
    algorithm that performs well in scenarios like this.

    We make no assumptions in this algorithm about capability to drive, number
    of seats, etc. in an effort to produce a reliable, and efficient (though
    not always optimal) solution. This works better with friend groups who may
    not always be motivated to drive or have access to a car (especially for
    younger groups), and for small businesses who wish to optimize even further
    since there's no need to underfill cars.

    Given the chicken-egg nature of the driver-selection and clustering
    problem, we've opted to select drivers first and then cluster as a means of
    efficiently clustering. While this negates the utility of clustering, it
    performs, in theory, much more robustly in these edge cases. Given the
    increased amount of computation & time for computation, however, we'll
    restrict this algorithm to only smaller groups for now.
"""


# ----- Environment Setup ----- #
# static libraries
import numpy as np                                  # array manipulation
from distance import *                              # distance calculations

# dependent on algorithm chosen
from sklearn.cluster import KMeans                  # clustering
from scipy.spatial.distance import cdist            # Euclidean distance
from scipy.optimize import linear_sum_assignment    # magic function lol


# ------ K-Means & Post-Processing ------ #
"""
    Final wrapped function that dispatches the appropriate clustering algorithm
    as given by the size of the input population.
"""
def cluster(coords: np.ndarray, cluster_size: int) -> list:
    # branch #
    if len(coords) < 50:
        return cluster_ds(coords=coords)
    return cluster_kmeans(coords=coords, cluster_size=cluster_size)


# ------ K-Means & Post-Processing ------ #
"""
    A wrapping function to make functions calls less repetitive in the final
    app deployment. Returns a 2D list.
"""
def cluster_kmeans(coords: np.ndarray, cluster_size: int) -> list:
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
def get_even_clusters(coords: np.ndarray, cluster_size: int) -> np.ndarray:
    # clustering #
    n_clusters = int(np.ceil(len(coords) / cluster_size))
    kmeans = KMeans(n_clusters)
    kmeans.fit(coords)


    # post-processing #
    # process centroids
    centers = kmeans.cluster_centers_
    centers = (
        centers.reshape(-1, 1, coords.shape[-1])
        .repeat(cluster_size, 1)
        .reshape(-1, coords.shape[-1])
    )

    # efficient distance
    distance_matrix = cdist(coords, centers)

    # magic
    clusters = linear_sum_assignment(distance_matrix)[1] // cluster_size
    
    # return results
    return clusters


"""
    Uses the information from get_even_clusters to actually cluster the coords
    array.
"""
def group(clusters: np.ndarray, coords: np.ndarray, cluster_size: int) -> list:
    # setup #
    num_clusters = int(np.ceil(len(coords) / cluster_size))
    groups = [[] for num in range(num_clusters)]


    # associate coords w/ clusters
    for idx, cluster in enumerate(clusters):
        groups[cluster].append(coords[idx])
    return groups


# ----- Clustering via Driver Selection ----- #
"""
    Algorithm design to be finalized...

    Will ensure optimized paths within clusters before returning using
    optimize_path() for each path.
"""
def cluster_ds(coords: np.ndarray) -> list:
    print("incomplete algo LOLOLOLOL")
    exit(1)
    pass


"""
    Finds the shortest path given the final cluster & driver selections. This
    algorithm assumes the first coordinate is the driver.
"""
def optimize_path(coords: np.ndarray):
    pass

