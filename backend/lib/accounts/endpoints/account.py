from lib.accounts import authentication as auth
from lib.accounts import utils as account_utils

import utils
import pymongo
import shutil

from flask import Flask, request
from flask_restful import Api, Resource, reqparse

class account(Resource):
    def get(self, client_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        user = utils.col.find({"id": client_id})
        return auth.user(user)

    def delete(self, client_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        utils.col.delete_one({"id": client_id})
        
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

        utils.col.update({'id': client_id}, {"$set": updates}, upsert=False)
        user = utils.col.find({"id": client_id})

        return auth.user(user), 200