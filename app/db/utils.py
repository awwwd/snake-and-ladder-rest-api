from app.core.config import settings, database_name, all_db_collections, logger
from app.db.mongodb import db
from pymongo import MongoClient


def connect_to_mongo():
    logger.info("Connecting to mongodb")
    db.client = MongoClient(str(settings.DATABASE_URL),
                            maxPoolSize=settings.MAX_CONNECTIONS_COUNT,
                            minPoolSize=settings.MIN_CONNECTIONS_COUNT)
    database = db.client[database_name]
    for collections in all_db_collections:
        logger.info(f"Creating {collections} in mongodb")
        database.get_collection(collections)


def close_mongo_connection():
    logger.info("Disconnecting from mongo")
    db.client.close()
