import pymongo

client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
db = client["driplet"]
users = db["users"]
services = db["services"]

def reset():
    print("Resetting...")
    users.delete_many({})
    services.delete_many({})