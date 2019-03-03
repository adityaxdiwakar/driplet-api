import json
import random

def adupe(list, value):
    for item in list:
        if item['id'] == value:
            return True
    return False

def new_id(client_services):
    while True:
        r = random.randint(1000000000,9999999999)
        if not adupe(client_services, r):
            return 's' + str(r)

def get(client_id):
    with open(f"bin/{client_id}/services.json", "r") as f:
        return json.load(f)

def push(data, client_id):
    with open(f"bin/{client_id}/services.json", "w") as f:
        json.dump(data, f, indent=4)
