from flask_restful import reqparse

import pymongo
import json
import copy
from bson import json_util

def encoder(input):
    return copy.copy(json.loads(json_util.dumps(input)))

<<<<<<< HEAD
client = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
=======
client = pymongo.MongoClient("mongodb://0.0.0.0:27017/")
>>>>>>> 36c17188960298c79b13f761ab3da3c5a33a9f33
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

