from lib.accounts import authentication as auth
from lib.accounts import utils as account_utils

from flask import Flask, request
from flask_restful import Resource, reqparse

import en_us
import time
import utils
import jwt


class pw(Resource):
    @classmethod
    def post(self, clientid, key):
        cur_time = int(time.time())
        user = utils.col.find({"id": clientid})
        if user.count() == 0:
            return en_us.AUTH_FAILED
        user = utils.encoder(user)[0]
        secret = user["salt"]

        try:
            enterance_payload = jwt.decode(key,
                                           secret,
                                           algorithms=["HS256"])
        except jwt.exceptions.DecodeError:
            return en_us.AUTH_FAILED

        if enterance_payload["expiration"] < cur_time:
            return en_us.AUTH_FAILED

        if enterance_payload['user'] != clientid:
            return en_us.AUTH_FAILED

        # good to go reset the password, but what is the password?
        args = utils.gen_fields(reqparse.RequestParser(), ['password'])
        if args["password"] == "" or args["password"] == None:
            return en_us.BAD_REQUEST

        utils.col.update({"id": clientid}, {
                         "$set": {"password": auth.make_password(args["password"])}})
