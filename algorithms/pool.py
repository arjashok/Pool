"""
    This is the fully wrapped algorithm that handles all function calls,
    storage, and more for a neatly-packed function to be called in the web-app
    and any future implementations.
"""


# ----- Environment Setup ----- #
from clustering import cluster                          # cluster groups
from driver_selection import driver_selection           # select drivers
from database import *                                  # query users


# ----- Pool Algorithm ----- #
"""
    Wrapper function for all sub-calls. Takes in a carpool list (of IDs) and
    destination coordinates, then generates a dictionary of drivers to routes:

    // schema //
    {
        driver-name: {
            names:  order-names,
            coords: order-coords,
            ids:    order-ids
        }
    }
"""
def pool(carpool_list: list, destination: tuple) -> dict[str: dict[str: list]]:
    # setup #
    # parameters
    PEOPLE_PER_CAR = 4
    
    # store final results
    pools = dict()

    # variable handling
    pool_size = len(carpool_list)

    # query information
    population_db = db_query_users(users=carpool_list)
    coords = population_db['location-coords']

    
    # cluster & driver select #
    # cluster
    clusters = cluster(coords, PEOPLE_PER_CAR)

    # add destination to path
    for cluster in clusters:
        cluster.append(destination)

    # branch off algorithm
    if pool_size < 50:
        # format & return
        return format_path(population_db, clusters)

    # cluster driver selection
    paths = []
    for cluster in clusters:
        user_ids = lookup_userids(cluster)
        cluster_db = population_db[population_db["user-id"] == user_ids]
        path = driver_selection(cluster_db)
        paths.append([cluster[idx] for idx in path])

    # format & return
    response = format_path(population_db=population_db, coords=paths)
    return response


# ----- Auxiliary Methods for Formatting Output ----- #
"""
    Given a list of coordinates, generates a complete dictionary as defined in
    the schema above for return by the pool algorithm.

    Input:
    [
        [(x, y), (x, y), . . .],
        . . .
    ]
"""
def format_path(population_db: pd.DataFrame, coords: list) -> dict:
    pass


"""
    Given a list of coordinates, generates a list of user-ids for use with
    realigning with the primary key.

    TODO: eventually this should be redundant because we'll need to transfer to
    using user-id's and lookups to do all coordinates.
"""
def lookup_userids(db: pd.DataFrame, coords: list) -> list:
    # lookup user-id #
    user_ids = [
        db.loc[db.index[db["location-coords"] == coord][0], 'user-id'] \
        for coord in coords
    ]

    return user_ids

