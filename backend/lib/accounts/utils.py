import random
import json
import os

def get_user_id():
    while True:
        r = random.randint(1000000000, 9999999999)
        if r not in os.listdir('bin'):
            return 'u' + str(r)

def get_users():
    users = []
    for user in os.listdir('bin'):
        data = json.load(open(f"bin/{user}/account.json", "r"))
        users.append(data)
    return users

def get(id):
    users = os.listdir('bin')
    if str(id) not in users:
        return None
    else:
        return json.load(open(f"bin/{id}/account.json", "r"))

def offload(id, filename, data):
    json.dump(
        data,
        open(f"bin/{id}/{filename}.json", "w"),
        indent=4
    )

def push(user):
    os.mkdir(f"bin/{user['id']}")
    offload(user['id'], 'account', user)
    offload(user['id'], 'services', [])


