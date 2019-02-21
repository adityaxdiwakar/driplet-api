#password hashing
from passlib.apps import custom_app_context as pwd_context

#general requirements
import time, json, os, random, shutil, string, jwt

#API dependencies
from flask import Flask
from flask_restful import Api, Resource, reqparse

#helper functions
def random_salt(size=1024, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
        return ''.join(random.choice(chars) for _ in range(size))

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

def public_user(user):
    user.pop('salt')
    user.pop('password')
    return user

def generate_token(user, salt):
    token = jwt.encode(user, salt, algorithm='HS256')
    return token

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
            if user['username'] == args['username']:
                return "A user with that username already exists", 400
        
        user = {
            "username":args['username'],
            "email":args['email'],
            "password": pwd_context.hash(args['password']),
            "id":get_user_id(),
            "time_created":int(time.time())
        }
        
        salt = random_salt()
        
        user.update(
            {
                "salt": salt
            }
        )

        users.append(user)
        push_user(user)

        user.pop('salt')
        user.update(
            {
                "token": generate_token(user, salt).decode('utf-8')
            }
        )
        user.pop('password')
        return user, 201

class acmang(Resource):
    def get(self, client_id):
        user = get_user(client_id)
        if user == None:
            return {"message": "User could not be found", "code": 404}, 404
        else:
            return public_user(user)

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
        if 'password' in updates:
            updates['password'] = pwd_context.hash(updates['password'])

        users = get_users()
        for user in users:
            if user['id'] == client_id:
                user.update(updates)
                json.dump(
                    user,
                    open(f"bin/{client_id}/account.json", "w"),
                    indent = 4
                )
                return public_user(user), 200
        return {"message": "User could not be found", "code": 404}, 404


class login(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("password")      
        args = parser.parse_args()  

        users = get_users()
        for user in users:
            if user['username'] == args['username']:
                if pwd_context.verify(args['password'], user['password']):
                    salt = user['salt']
                    user.pop('salt')
                    user.update({
                        "token": generate_token(user, salt).decode('utf-8')
                    })
                    user.pop('password')
                    return user, 200
                else:
                    return {"message": "Authorization failed", "code": 401}, 401
        return {"message": "User could not be found", "code": 404}, 404 