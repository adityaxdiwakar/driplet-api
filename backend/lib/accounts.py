#password hashing
from passlib.apps import custom_app_context as pwd_context

#general requirements
import time, json, os, random, shutil, string, jwt

#API dependencies
from flask import Flask, request
from flask_restful import Api, Resource, reqparse

#string definitions
NOT_FOUND = {"message": "User could not be found", "code": 404}
AUTH_FAILED = {"message": "Authorization failed", "code": 401}
UNAME_EXISTS = {"message": "A user with that username already exists", "code": 400}
EMAIL_EXISTS = {"message": "A user with that email already exists", "code": 400}
TOKEN_VERIFIED ={"message": "Successfully verified your token", "code": 200}


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
    user.pop('salt')   
    token = jwt.encode(user, salt, algorithm='HS256')
    return token

def authenticate_user(client_id, token):
    user = get_user(client_id)
    if user == None:
        return NOT_FOUND, 404
    try:
        payload = jwt.decode(token, user['salt'], algorithms=['HS256'])
    except:
        return AUTH_FAILED, 401
    if 'id' in payload:
        if payload['id'] == user['id']:
            return 200
    return AUTH_FAILED, 401

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
                return EMAIL_EXISTS, 400
            if user['username'] == args['username']:
                return UNAME_EXISTS, 400
        
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

        user.update(
            {
                "token": generate_token(user, salt).decode('utf-8')
            }
        )
        user.pop('password')
        return user, 201

class acmang(Resource):
    def get(self, client_id):
        request_token = request.headers.get('authorization')
        auth = authenticate_user(client_id, request_token)
        if auth != 200:
            return auth
        user = get_user(client_id)
        if user == None:
            return NOT_FOUND, 404
        else:
            return public_user(user)

    def delete(self, client_id):
        request_token = request.headers.get('authorization')
        auth = authenticate_user(client_id, request_token)
        if auth != 200:
            return auth
        users = get_users()
        for user in users:
            if user['id'] == client_id:
                shutil.rmtree(f"bin/{client_id}")
                return "", 204
        return NOT_FOUND, 404

    def patch(self, client_id):
        request_token = request.headers.get('authorization')
        auth = authenticate_user(client_id, request_token)
        if auth != 200:
            return auth
            
        parser = reqparse.RequestParser()
        parser.add_argument("username")
        parser.add_argument("email")
        parser.add_argument("password")
        parser.add_argument("authorization")
        args = parser.parse_args()
        updates = {}
        for key in args:
            if args[key] != None:
                updates.update({key:args[key]})
                
        user = get_user(client_id)
        if user == None:
            return NOT_FOUND, 404
        user.update(updates)
        json.dump(
            user,
            open(f"bin/{client_id}/account.json", "w"),
            indent = 4
        )
        user.pop('salt')
        user.pop('password')
        return user, 200

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
                    user.update({
                        "token": generate_token(user, salt).decode('utf-8')
                    })
                    user.pop('password')
                    return user, 200
                else:
                    return AUTH_FAILED, 401
        return NOT_FOUND, 404 

class verify(Resource):
    def get(self, client_id):
        request_token = request.headers.get('authorization')
        auth = authenticate_user(client_id, request_token)
        if auth != 200:
            return auth
        return TOKEN_VERIFIED
