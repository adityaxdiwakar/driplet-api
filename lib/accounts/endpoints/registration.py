import time
import utils
import en_us

from lib.accounts import authentication as auth
from lib.accounts import utils as account_utils

from flask_restful import Resource, reqparse


class register(Resource):
    @classmethod
    def post(self):
        q_args = ["username", "email","password"]
        args = utils.gen_fields(reqparse.RequestParser(), q_args)

        same_email = utils.col.find({"email": args['email']})
        same_username = utils.col.find({"username": args['username']})

        for arg in q_args:
            if arg not in args:
                return en_us.BAD_REQUEST

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

        return auth.user(utils.encoder(user)), 201
