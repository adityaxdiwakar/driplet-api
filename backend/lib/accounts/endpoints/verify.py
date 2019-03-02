from flask import Flask, request
from flask_restful import Api, Resource, reqparse

from lib.accounts import authentication as auth

import en_us

class verify(Resource):
    def get(self, client_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status
            
        return en_us.TOKEN_VERIFIED