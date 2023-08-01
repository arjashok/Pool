"""
    This algorithm will utilize a form of K-Means Clustering to group people
    together in the most optimal way to minimize total distance driven.

    # -- Approach I -- #
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
"""

# --------------------------------------------------------------------------- #

