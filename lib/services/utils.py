import json
import random
import utils

def adupe(list, value):
    for item in list:
        if item['id'] == value:
            return True
    return False


def new_id():
    while True:
        r = random.randint(1000000000, 9999999999)
        if utils.services.find({"id": 'u' + str(r)}).count() == 0:
            return 'u' + str(r)
