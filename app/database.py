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
from bson import ObjectId
import numpy as np  # array manipulation

# temporary
import pandas as pd

from pymongo import MongoClient  # database
from MapsAPI import *  # maps API
from config import *  # API keys
from firebase_admin import auth, credentials, initialize_app


# ------ Auxiliary Functions for Queries ------ #


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
def db_modify_user_pandas(users: pd.DataFrame) -> None:
    # check missing
    if not "user-id" in users.columns:
        print("Failed db update for failed column primary key `user-id`")
        return None

    # pandas deprecated
    pool_db = db_load("na")
    pool_db = pool_db.merge(users, on="user-id", how="left")
    db_save(pool_db)

    return


"""
    Modify one of the user entries in the database.
"""
def db_modify_user(userID: str, fields: dict) -> None:
    db = db_load("PoolData")
    collection = db["Users"]

    filter = {"_id": ObjectId(userID)}
    update = {"$set": fields}
    try:
        result = collection.update_one(filter, update)
        print(result.modified_count, "documents updated.")
    except Exception as e:
        print("Failed to update user: ", e)
    return None


"""
    Modify one of the event entries in the database.
"""
def db_modify_event(eventID: str, fields: dict) -> None:
    db = db_load("PoolData")
    collection = db["Events"]

    filter = {"_id": ObjectId(eventID)}
    update = {"$set": fields}
    try:
        result = collection.update_one(filter, update)
        print(result.modified_count, "documents updated.")
    except Exception as e:
        print("Failed to update user: ", e)
    return None


"""
    Modify one of the organization entries in the database.
"""
def db_modify_org(orgID: str, fields: dict) -> None:
    db = db_load("PoolData")
    collection = db["Organizations"]

    filter = {"_id": ObjectId(orgID)}
    update = {"$set": fields}
    try:
        result = collection.update_one(filter, update)
        print(result.modified_count, "documents updated.")
    except Exception as e:
        print("Failed to update user: ", e)
    return None


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
    client = MongoClient(config.CONNECTION_STRING)
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
def db_create_org(name: str, adminIDs: list) -> None:
    # setup #
    db = db_load("PoolData")
    collection_name = db["Organizations"]
    # insert #
    adminIDs = [ObjectId(str_id) for str_id in adminIDs]
    try:
        result = collection_name.insert_one(
            {"name": name.lower(), "adminIDs": adminIDs}
        )
        print(result.inserted_id, "documents inserted.")
    except Exception as e:
        print("Failed to insert organization", e)
    return None


def db_create_org_pd(entry: pd.DataFrame) -> None:
    db = db_load("PoolData")
    collection_name = db["Organizations"]
    # insert #
    adminIDs = [ObjectId(str_id) for str_id in entry["adminIDs"]]
    try:
        result = collection_name.insert_one(
            {"name": entry["name"].lower(), "adminIDs": adminIDs}
        )
        print(result.inserted_id, "documents inserted.")
    except Exception as e:
        print("Failed to insert organization", e)
    return None


"""
    Insert a user into the database.
"""
def db_create_user(name: str, email: str, address: str, password: str) -> None:
    # setup #
    db = db_load("PoolData")
    collection_name = db["Users"]
    cred = credentials.Certificate("firebase_key.json")

    try:
        geo_code = get_geo(address)
    except Exception as e:
        print("Could not find geo code for address")
        return None
    # insert #
    try:
        result = collection_name.insert_one(
            {
                "name": name.lower(),
                "email": email.lower(),
                "address": address.lower(),
                "geo": geo_code,
            }
        )
        print(result.inserted_id, "documents inserted.")
    except Exception as e:
        print("Failed to insert user to MongoDB", e)
        
    try:
        firebase_app = initialize_app(cred)
        user = auth.create_user(
            email=email,
            email_verified=False,
            password=password,
            display_name=name,
            disabled=False
        )
        print('Sucessfully created new user: {0}'.format(user.uid))
    except Exception as e:
        print("Failed to insert user to Firebase", e)
    return None


def db_create_user_pd(entry: pd.DataFrame) -> None:
    db = db_load("PoolData")
    collection_name = db["Users"]
    cred = credentials.Certificate("firebase_key.json")
    try:
        geo_code = get_geo(entry["address"])
    except Exception as e:
        print("Could not find geo code for address")
        return None
    # insert #
    try:
        result = collection_name.insert_one(
            {
                "name": entry["name"].lower(),
                "email": entry["email"].lower(),
                "address": entry["address"].lower(),
                "geo": geo_code,
            }
        )
        print(result.inserted_id, "documents inserted.")
    except Exception as e:
        print("Failed to insert user", e)
        
    try:
        firebase_app = initialize_app(cred)
        user = auth.create_user(
            email=entry["email"],
            email_verified=False,
            password=entry["password"],
            display_name=entry["name"],
            disabled=False
        )
        print('Sucessfully created new user: {0}'.format(user.uid))
    except Exception as e:
        print("Failed to insert user to Firebase", e)
    return None


"""
    Insert an event into the database.
"""
def db_create_event(name: str, orgID: str, location: str) -> None:
    # setup #
    db = db_load("PoolData")
    collection_name = db["Events"]
    try:
        geo = get_geo(location)
    except Exception as e:
        print("Could not find geo code for address")
        return None
    # insert #
    try:
        result = collection_name.insert_one(
            {
                "name": name.lower(),
                "orgID": ObjectId(orgID),
                "location": location.lower(),
                "geo": geo,
            }
        )
        print(result.inserted_id, "documents inserted.")
    except Exception as e:
        print("Failed to insert event: ", e)
    return None


def db_create_event_pd(entry: pd.DataFrame) -> None:
    # setup #
    db = db_load("PoolData")
    collection_name = db["Events"]
    try:
        geo = get_geo(entry["location"])
    except Exception as e:
        print("Could not find geo code for address")
        return None
    # insert #
    try:
        result = collection_name.insert_one(
            {
                "name": entry["name"].lower(),
                "orgID": ObjectId(entry["orgID"]),
                "location": entry["location"].lower(),
                "geo": geo,
            }
        )
        print(result.inserted_id, "documents inserted.")
    except Exception as e:
        print("Failed to insert event: ", e)
    return None

db_create_user("Noah", "bob@gmail.com", "Fitness 19 Dublin", "password1234")