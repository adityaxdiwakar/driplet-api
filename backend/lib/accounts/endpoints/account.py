from lib.accounts import authentication as auth
from lib.accounts import utils as account_utils

import utils

from flask import Flask, request
from flask_restful import Api, Resource, reqparse

class account(Resource):
    def get(self, client_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        user = account_utils.get(client_id)
        return auth.user(user)

    def delete(self, client_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        users = account_utils.get_users()
        for user in users:
            if user['id'] == client_id:
                shutil.rmtree(f"bin/{client_id}")
                return "", 204
        
        return NOT_FOUND

    def patch(self, client_id):
        request_token = request.headers.get('authorization')
        auth_status = authenticate_user(client_id, request_token)
        if auth_status != 200:
            return auth_status

        args = utils.gen_fields(reqparse.RequestParser(),
                    ['username', 'email', 'password'])

        updates = {}
        for key in args:
            if args[key] != None:
                updates.update({key: args[key]})

        user.update(updates)
        account_utils.offload(client_id, 'account', user)

        return auth.user(user), 200