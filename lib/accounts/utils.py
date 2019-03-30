import random
import json
import os
import pymongo
import utils


def get_user_id():
    while True:
        r = random.randint(1000000000, 9999999999)
        if utils.col.find({"id": 'u' + str(r)}).count() == 0:
            return 'u' + str(r)
