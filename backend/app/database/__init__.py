import os

from pymongo import MongoClient

username = os.environ["MONGO_USERNAME"]
password = os.environ["MONGO_PASSWORD"]

mongoClient = MongoClient(f"mongodb://{username}:{password}@mongo:27017")
database = mongoClient["DoNotDisturb"]
users_collection = database["users"]
transactions_collection = database["transactions"]
