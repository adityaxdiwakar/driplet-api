import time
import utils
import json
import en_us
from bson import json_util
import pymongo

from lib.accounts import authentication as auth
from lib.accounts import utils as account_utils

from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from passlib.apps import custom_app_context as pwd_context


class register(Resource):
    def post(self):
        args = utils.gen_fields(reqparse.RequestParser(), [
                                'username', 'email', 'password'])

        same_email = utils.col.find({"email": args['email']})
        same_username = utils.col.find({"username": args['username']})
        print(json_util.dumps(same_email))
        if same_email.count() > 0:
            return en_us.EMAIL_EXISTS
        if same_username.count() > 0:
            return en_us.UNAME_EXISTS

        user = {
            "username": args['username'],
            "email": args['email'],
            "password": auth.make_password(args['password']),
            "id": account_utils.get_user_id(),
            "time_created": int(time.time())
        }

        user.update({"salt": auth.salt()})

        utils.col.insert(user)

        user.update({"token": auth.generate(user)})

        return auth.user(json.loads(json_util.dumps(user))), 201
