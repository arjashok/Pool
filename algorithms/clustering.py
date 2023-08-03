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
    
    # -- Driver Selection by Clustering -- #
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

# --------------------------------------------------------------------------- #

