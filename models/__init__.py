
from pymongo import MongoClient
from configs import MONGO_URI, MONGO_DB

mongo = MongoClient(MONGO_URI, connect=False)
db = mongo[MONGO_DB]