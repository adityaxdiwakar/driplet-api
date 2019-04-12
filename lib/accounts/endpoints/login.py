from flask_restful import Resource, reqparse

from lib.accounts import authentication as auth

import utils
import en_us

class login(Resource):
    @classmethod
    def post(self):
        fields = ["username", "email"]
        q_args = ["username", "password"]
        args = utils.gen_fields(reqparse.RequestParser(), q_args)
        
        for arg in q_args:
            if arg not in args:
                return en_us.BAD_REQUEST
            if args[arg] == None or args[arg] == "":
                return en_us.BAD_REQUEST

        m_length = 0
        users = None
        for field in fields:
            length = len(utils.encoder(utils.col.find({field: args['username']})))
            if length > m_length:
                m_length = length
                users = utils.encoder(utils.col.find({field: args['username']}))

        if m_length == 0:
            return en_us.NOT_FOUND

        user = utils.encoder(users)[0]

        if not auth.check_password(args['password'], user['password']):
            return en_us.AUTH_FAILED

        user.update({"token": auth.generate(user)})
        return auth.user(user), 200



