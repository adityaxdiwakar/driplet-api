import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["driplet"]
mycol = db["users"]

