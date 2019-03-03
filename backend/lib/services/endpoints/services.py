from flask import Flask, request
from flask_restful import Api, Resource, reqparse

from lib.accounts import authentication as auth
from lib.services import utils as services_util

import os
import en_us
import utils

class services(Resource):
    def get(self, client_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        return services_util.get(client_id)

    def post(self, client_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        args = utils.gen_fields(reqparse.RequestParser(), 
                                                 ['name', 'description', 'start_command', 'stop_command', 
                                                'restart_command', 'status_command', 'log_command'])

        if os.system(f"systemctl is-active {args['name']} --quiet") != 0:
            return en_us.SERVICE_NOT_FOUND

        all_services = services_util.get(client_id)
        service = args
        service.update({"id": services_util.new_id(all_services)})

        all_services.append(service)
        services_util.push(all_services, client_id)
        return service, 201
