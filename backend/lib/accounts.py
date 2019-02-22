#general requirements
import time, json, os, random, shutil

#API dependencies
from flask import Flask
from flask_restful import Api, Resource, reqparse

#helper functions
def get_user_id():
    while True:
        r = random.randint(1000000000,9999999999)
        if r not in os.listdir('bin'):
            return 'u' + str(r)

def get_users():
    users = []
    for user in os.listdir('bin'):
        data = json.load(open(f"bin/{user}/account.json", "r"))
        users.append(data)
    return users

def get_user(id):
    users = os.listdir('bin')
    if str(id) not in users:
        return None
    else:
        return json.load(open(f"bin/{id}/account.json", "r"))

def push_user(user):
    os.mkdir(f"bin/{user['id']}")
    json.dump(
        user,
        open(f"bin/{user['id']}/account.json", "w"),
        indent = 4
    )
    json.dump(
        [],
        open(f"bin/{user['id']}/services.json", "w"),
        indent = 4
    )

class registration(Resource):
    def post(self): 
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("email")
        parser.add_argument("password")
        args = parser.parse_args()

        users = get_users()
        for user in users:
            if user['email'] == args['email']:
                return "A user with that email already exists", 400
        
        user = {
            "username":args['username'],
            "email":args['email'],
            "password":args['password'],
            "id":get_user_id()
        }

        users.append(user)
        push_user(user)
        return user, 201

class acmang(Resource):
    def get(self, client_id):
        user = get_user(client_id)
        if user == None:
            return {"message": "User could not be found", "code": 404}, 404
        else:
            return user

    def delete(self, client_id):
        users = get_users()
        for user in users:
            if user['id'] == client_id:
                shutil.rmtree(f"bin/{client_id}")
                return "", 204
        return {"message": "User could not be found", "code": 404}, 404

    def patch(self, client_id):
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("email")
        parser.add_argument("password")
        args = parser.parse_args()
        updates = {}
        for key in args:
            if args[key] != None:
                updates.update({key:args[key]})
                
        user = get_user(client_id)
        if user == None:
            return {"message": "User could not be found", "code": 404}, 404
        user.update(updates)
        json.dump(
            user,
            open(f"bin/{client_id}/account.json", "w"),
            indent = 4
        )
        return user, 200