import sys
import os

algorithms_dir_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../algorithms")
)
sys.path.append(algorithms_dir_path)

from MapsAPI import *
from clustering import *
from driver_selection import *

# Will probably need to change the clustering algos or smth so its easier to match the geo coords to the userIDs/Names
def get_optimal_paths(addresses: np.ndarray) -> list:
    # Will not need to get the geo array when geolocation stored with user data
    geo_array = get_geo_array(addresses)
    coords = geo_array["coord"]
    addy_dict = {tuple(coord): addy for coord, addy in geo_array}
    clusters = cluster_kmeans(coords, 4)
    paths = []
    for group in clusters:
        group = np.array(group)
        dmatrix = create_distance_matrix_address(group)
        path_indices = driver_selection_dp(group, dmatrix)
        path = group[path_indices].tolist()
        path = [addy_dict[tuple(coord)] for coord in path]
        paths.append(path)
    return paths


# addys = np.array(
#     [
#         "2009 Poinsettia Street San Ramon",
#         "9367 mediar drive San Ramon",
#         "7005 laurelspur loop San Ramon",
#         "Dougherty Valley High School San Ramon",
#         "Fitness 19 Dublin CA",
#         "Fitness 24 San Ramon CA",
#     ]
# )
# print(get_optimal_paths(addys))
