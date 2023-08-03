"""
    This is the fully wrapped algorithm that handles all function calls,
    storage, and more for a neatly-packed function to be called in the web-app
    and any future implementations.
"""


# ----- Environment Setup ----- #
from clustering import cluster                          # cluster groups
from driver_selection import driver_selection           # select drivers


# ----- Pool Algorithm ----- #
"""
    Wrapper function for all sub-calls. Takes in a carpool list and generates
    a dictionary of drivers to routes:

    // schema //
    {
        driver-name: {
            names:  order-names,
            coords: order-coords,
            ids:    order-ids
        }
    }
"""
def pool(carpool_list: list) -> dict[str: dict[str: list]]:
    pass

