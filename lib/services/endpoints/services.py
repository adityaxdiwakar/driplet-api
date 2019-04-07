from flask import request
from flask_restful import Resource, reqparse

from lib.accounts import authentication as auth
from lib.services import utils as services_util

import utils


class services(Resource):
    @classmethod
    def get(self, client_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        return utils.encoder(utils.get_all_services(client_id))

    @classmethod
    def post(self, client_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        args = utils.gen_fields(reqparse.RequestParser(),
                                ['name', 'description', 'start_command', 'stop_command',
                                 'restart_command', 'status_command', 'log_command'])
        service = args

        service.update(
            {
                "id": services_util.new_id(),
                "associated_to": client_id,
                "logs": []
            }
        )

        utils.services.insert(service)
        return utils.encoder(service), 201
