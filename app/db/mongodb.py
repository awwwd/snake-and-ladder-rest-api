from pymongo import MongoClient
from functools import lru_cache


class DataBase:
    client: MongoClient = None


db = DataBase()


# Cache the object
@lru_cache
def get_database() -> MongoClient:
    return db.client
