import googlemaps
import config
import numpy as np

api_key = config.MAPS_API_KEY

gmaps = googlemaps.Client(key=api_key)


def get_duration(origin: str, destination: str) -> float:
    directions = gmaps.directions(origin, destination, mode="driving", units="metric")
    if len(directions) > 0:
        duration = directions[0]["legs"][0]["duration"]["text"].split()[0]
        return float(duration)
    else:
        return None


def get_geo(address: str) -> tuple:
    coords_dict = gmaps.geocode(address)[0]["geometry"]["location"]
    return (coords_dict["lat"], coords_dict["lng"])


def get_geo_array(addresses: np.ndarray) -> np.ndarray:
    coords_array = np.empty(
        addresses.shape[0], dtype=[("coord", "float64", 2), ("address", "U100")]
    )
    for i in range(addresses.shape[0]):
        coords_array[i] = (get_geo(addresses[i]), addresses[i])
    return coords_array


def create_distance_matrix_address(addresses: np.ndarray) -> np.ndarray:
    # setup
    n = addresses.shape[0]
    matrix = np.zeros((n, n))

    # get all distances
    for i in range(n):
        for j in range(0, i):
            dist = 2
            dist = get_duration(addresses[i], addresses[j])
            matrix[i][j] = dist

    # return 2D
    return matrix


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
