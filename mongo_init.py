import pymongo

client = pymongo.MongoClient("mongodb://localhost:27017/")

db = myclient["driplet"]
mycol = db["users"]


