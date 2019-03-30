from flask import Flask, request
from flask_restful import Api, Resource, reqparse

from lib.accounts import authentication as auth
from lib.services import utils as services_util

import en_us
import utils


class service(Resource):
    def get(self, client_id, service_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        service = utils.get_service(client_id, service_id)
        if service.count() == 0:
            return en_us.SERVICE_NOT_FOUND

        return utils.encoder(service[0])

    def delete(self, client_id, service_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        utils.services.delete_one(
            {"associated_to": client_id, "id": service_id}
        )

        return "", 204
