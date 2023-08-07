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
import numpy as np  # array manipulation

# temporary
import pandas as pd

from pymongo import MongoClient  # database
from MapsAPI import *  # maps API


# ------ Auxiliary Functions for Queries ------ #
"""
    Functionality to query an organization's id based on name
"""


def db_query_org_id(name: str) -> str:
    # setup #
    db = db_load("PoolData")
    collection_name = db["Organizations"]
    org_id = collection_name.find_one({"name": name})["_id"]

    # query #
    return org_id


"""
    Get user info for a specified list of users using their designated ID.
"""


def db_query_users(users: np.ndarray) -> pd.DataFrame:
    # setup #
    db = db_load()

    # query #
    return db[db["user-id"] == users]


# ------ Auxiliary Functions for Operations ------ #
"""
    Given a dataframe of users, all user info for which there are defined
    columns will be modified to match the inputted dataframe. The user-ids will
    be matched as primary key to accomplish this.
"""


def db_modify_users(users: pd.DataFrame) -> None:
    # check missing
    if not "user-id" in users.columns:
        print("Failed db update for failed column primary key `user-id`")
        return None

    # pandas deprecated
    pool_db = db_load("na")
    pool_db = pool_db.merge(users, on="user-id", how="left")

    return


# ------ Auxiliary Functions for DB Functionality ------ #
"""
    Functionality for now to load in the database.
"""


def db_load(database) -> pd.DataFrame:
    # # deprecated #
    # pool_db = pd.read_parquet(
    #     "../datasets/poolDB.parquet",
    #     engine = "fastparquet"
    # )

    # return pool_db

    # read & return #
    CONNECTION_STRING = (
        "mongodb+srv://yashravipati:YAdPCgjsuicf8Qfq@pooldb.gcjiexs.mongodb.net/"
    )
    client = MongoClient(CONNECTION_STRING)
    return client[database]


"""
    Functionality for now to save updates to the database.
"""


def db_save(pool_db: pd.DataFrame) -> None:
    # save & end #
    pool_db = pd.to_parquet("../datasets/poolDB.parquet", engine="fastparquet")

    return None


"""
    Functionality to insert a new organization into the database.
"""


def db_insert_org(name, userIDs) -> None:
    # setup #
    db = db_load("PoolData")
    collection_name = db["Organizations"]
    # insert #
    collection_name.insert_one({"name": name.lower(), "user-ids": userIDs})
    return None


"""
    Insert a user into the database.
"""


def db_insert_user(name, email, orgName, address) -> None:
    # setup #
    db = db_load("PoolData")
    collection_name = db["Users"]
    geo_code = get_geo(address)
    # insert #
    collection_name.insert_one(
        {
            "name": name.lower(),
            "email": email.lower(),
            "org-id": db_query_org_id(orgName.lower()),
            "address": address.lower(),
            "geo": geo_code,
        }
    )
    return None


db_insert_user(
    "Coconut Sniffer", "noahantisseril@gmail.com", "test", "Fitness 19 Dublin"
)
