from flask import Flask, request
from flask_restful import Api, Resource, reqparse

from lib.accounts import authentication as auth
from lib.services import utils as services_util

import os

class start(Resource):
    def post(self, client_id, service_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        services = services_util.get(client_id)
        for service in services:
            if service['id'] == service_id:
                os.system(service['start_command'])
                return service, 200

class stop(Resource):
    def post(self, client_id, service_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        services = services_util.get(client_id)
        for service in services:
            if service['id'] == service_id:
                os.system(service['stop_command'])
                return service, 200

class restart(Resource):
    def post(self, client_id, service_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status
            
        services = services_util.get(client_id)
        for service in services:
            if service['id'] == service_id:
                os.system(service['restart_command'])
                return service, 200