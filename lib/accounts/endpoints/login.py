from flask import Flask, request
from flask_restful import Api, Resource, reqparse

from lib.accounts import authentication as auth
from lib.accounts import utils as account_utils

import utils
import en_us
import pymongo

class login(Resource):
    def post(self):
        args = utils.gen_fields(reqparse.RequestParser(), ['username', 'password'])
        
        users = utils.encoder(utils.col.find({"username": args['username']}))

        if len(users) == 0:
            return en_us.NOT_FOUND

        user = utils.encoder(users)[0]

        if not auth.check_password(args['password'], user['password']):
            return en_us.AUTH_FAILED

        user.update({"token": auth.generate(user, user['salt'])})
        return auth.user(user), 200



