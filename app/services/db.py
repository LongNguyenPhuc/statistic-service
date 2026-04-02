from functools import lru_cache
import motor.motor_asyncio as Motor
from .settings import get_settings
from pymongo import MongoClient


@lru_cache
def get_db():
    client = get_client()
    settings = get_settings()
    dbConfig = settings.DATABASE
    return client[dbConfig.DBNAME]


@lru_cache
def get_client():
    settings = get_settings()
    dbConfig = settings.DATABASE
    connection_string = f"mongodb://{dbConfig.USER}:{dbConfig.PASS}@{dbConfig.HOST}:{dbConfig.PORT}/{dbConfig.DBNAME}?authSource={dbConfig.AUTHDB}"

    return Motor.AsyncIOMotorClient(connection_string)


@lru_cache
def get_pymongo_client():
    settings = get_settings()
    dbConfig = settings.DATABASE
    connection_string = f"mongodb://{dbConfig.USER}:{dbConfig.PASS}@{dbConfig.HOST}:{dbConfig.PORT}/{dbConfig.DBNAME}?authSource={dbConfig.AUTHDB}"
    client = MongoClient(connection_string)
    return client
