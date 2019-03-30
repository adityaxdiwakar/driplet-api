from flask import Flask, request
from flask_restful import Api, Resource, reqparse

from lib.accounts import authentication as auth
from lib.services import utils as services_util

import en_us
import utils

import os


class start(Resource):
    def post(self, client_id, service_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        service = utils.get_service(client_id, service_id)
        if service.count() == 0:
            return en_us.NOT_FOUND

        os.system(utils.encoder(service)[0]['start_command'])
        return "", 204


class stop(Resource):
    def post(self, client_id, service_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        service = utils.get_service(client_id, service_id)
        if service.count() == 0:
            return en_us.NOT_FOUND

        os.system(utils.encoder(service)[0]['stop_command'])
        return "", 204


class restart(Resource):
    def post(self, client_id, service_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        service = utils.get_service(client_id, service_id)
        if service.count() == 0:
            return en_us.NOT_FOUND

        os.system(utils.encoder(service)[0]['restart_command'])
        return "", 204
