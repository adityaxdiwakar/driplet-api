from flask_restful import reqparse

import pymongo
import json
from bson import ObjectId

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, ObjectId):
            return str(o)
        return json.JSONEncoder.default(self, o)

def encoder(input):
    return JSONEncoder().encode(input)

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["driplet"]
col = db["users"]

def gen_fields(parser, fields):
    for field in fields:
        parser.add_argument(field)
    return parser.parse_args()

def user_get(clientid=None, username=None, email=None):
    if clientid != None:
        return col.find({"id": clientid})
    if username != None:
        return col.find({"username": username})
    if email != None:
        return col.find({"email": email})

