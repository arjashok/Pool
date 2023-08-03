"""
    Utility file for all functions relating to database queries and operations.

    Guidelines:
        - Naming for query functions is "db_query_{query_target}"
        - For query functions, the input should always be an array of user-ids,
          and the output should always be a DataFrame
        - Naming for operation functions is "db_{action}_{target}"
        - For operation functions, the input should be a dataframe with user-id
          and any other info that should be modified, and the output should
          always be a boolean for successful versus unsuccesful operation
    
    Reference @ database_design.md for the layout of all the databases we will
    eventually implement.
"""


# ----- Environment setup ----- #
# static libraries
import numpy as np                  # array manipulation

# temporary
import pandas as pd                 # temporary database location


# ------ Auxiliary Functions for Queries ------ #
"""
    Get user info for a specified list of users using their designated ID.
"""
def db_query_users(users: np.ndarray) -> pd.DataFrame:
    # setup #
    db = db_load()

    # query #
    return db[db['user-id'] == users]


# ------ Auxiliary Functions for Operations ------ #
"""
    Given a dataframe of users, all user info for which there are defined
    columns will be modified to match the inputted dataframe. The user-ids will
    be matched as primary key to accomplish this.
"""
def db_modify_users(users: pd.DataFrame) -> None:
    pass


# ------ Auxiliary Functions for DB Functionality ------ #
"""
    Functionality for now to load in the database.
"""
def db_load() -> pd.DataFrame:
    # read & return #
    firebase_db = pd.read_parquet(
        "../datasets/firebase.parquet",
        engine = "fastparquet"
    )

    return firebase_db


"""
    Functionality for now to save updates to the database.
"""
def db_save(firebase_db: pd.DataFrame) -> None:
    # save & end #
    firebase_db = pd.to_parquet(
        "../datasets/firebase.parquet",
        engine = "fastparquet"
    )

    return None

