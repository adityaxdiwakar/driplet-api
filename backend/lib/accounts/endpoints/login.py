from flask import Flask, request
from flask_restful import Api, Resource, reqparse

from lib.accounts import authentication as auth
from lib.accounts import utils as account_utils

import utils
import en_us

class login(Resource):
    def post(self):
        args = utils.gen_fields(reqparse.RequestParser(), ['username', 'password'])
        
        users = account_utils.get_users()
        for user in users:
            if user['username'] == args['username']:
                if auth.check_password(args['password'], user['password']):
                    user.update({"token": auth.generate(user, user['salt'])})
                    return auth.user(user), 200
                else:
                    return en_us.AUTH_FAILED

        return en_us.NOT_FOUND



