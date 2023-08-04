import googlemaps
import config
from datetime import datetime
import numpy as np

api_key = config.MAPS_API_KEY

gmaps = googlemaps.Client(key=api_key)


def get_distance(origin: str, destination: str) -> int:
    directions = gmaps.directions(origin, destination, mode="driving", units="metric")
    if len(directions) > 0:
        distance = directions[0]["legs"][0]["distance"]["text"].split()[0]
        return float(distance)
    else:
        return None


def get_geo(address: str) -> tuple:
    coords_dict = gmaps.geocode(address)[0]["geometry"]["location"]
    return (coords_dict["lat"], coords_dict["lng"])


def create_distance_matrix(addresses: np.ndarray) -> np.ndarray:
    # setup
    n = addresses.shape[0]
    matrix = np.zeros((n, n))

    # get all distances
    for i in range(n):
        for j in range(0, i):
            dist = 2
            dist = get_distance(addresses[i], addresses[j])
            matrix[i][j] = dist

    # return 2D
    return matrix


print(get_geo("9367 mediar drive San Ramon"))
# addys = np.array(
#     [
#         "2009 Poinsettia Street San Ramon",
#         "9367 mediar drive San Ramon",
#         "7005 laurelspur loop San Ramon",
#         "Dougherty Valley High School San Ramon",
#     ]
# )

# matrix = create_distance_matrix(addys)
# print(matrix)
