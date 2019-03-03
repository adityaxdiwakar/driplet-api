from flask import Flask, request
from flask_restful import Api, Resource, reqparse

from lib.accounts import authentication as auth
from lib.services import utils as services_util

import en_us

class service(Resource):
    def get(self, client_id, service_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        services = services_util.get(client_id)
        for service in services:
            if service['id'] == service_id:
                return service, 200

        return en_us.SERVICE_NOT_FOUND

    def delete(self, client_id, service_id):
        request_token = request.headers.get('authorization')
        auth_status = auth.verify(client_id, request_token)
        if auth_status != 200:
            return auth_status

        services = services_util.get(client_id)
        for x in range(len(services)):
            if services[x]['id'] == service_id:
                preq = services[0:x] + services[x+1:len(services)+1]
                services_util.push(preq, client_id)
                return preq, 200

        return en_us.SERVICE_NOT_FOUND