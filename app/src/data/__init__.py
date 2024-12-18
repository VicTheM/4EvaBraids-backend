from motor import motor_asyncio
from pymongo import MongoClient
from config import settings

client = MongoClient(settings.db["uri"])

db = client[settings.db["name"]]
async_db = motor_asyncio.AsyncIOMotorClient(settings.db["uri"])[
    settings.db["name"]
]
