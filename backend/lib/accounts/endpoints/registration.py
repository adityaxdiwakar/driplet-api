import time
import utils
import en_us

from lib.accounts import authentication as auth
from lib.accounts import utils as account_utils

from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from passlib.apps import custom_app_context as pwd_context

class register(Resource):
    def post(self):
        args = utils.gen_fields(reqparse.RequestParser(), ['username', 'email', 'password'])
        users = account_utils.get_users()
        for user in users:
            if user['email'] == args['email']:
                return en_us.EMAIL_EXISTS
            if user['username'] == args['username']:
                return en_us.UNAME_EXISTS

        user = {
            "username": args['username'],
            "email": args['email'],
            "password": auth.make_password(args['password']),
            "id": account_utils.get_user_id(),
            "time_created": int(time.time())
        }

        user.update({"salt": auth.salt()})

        account_utils.push(user)

        user.update({"token": auth.generate(user, user['salt'])})
        
        return auth.user(user), 201