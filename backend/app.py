from lib import services, accounts

from flask import Flask, request
from flask_restful import Api, Resource, reqparse

#initiializing the flask webapp
app = Flask(__name__)
api = Api(app)

#writing services endpoints
api.add_resource(services.manager, "/endpoints/<string:client_id>/services")
api.add_resource(services.manager_indv, "/endpoints/<string:client_id>/services/<string:service_id>")

#writing account endpoints
api.add_resource(accounts.registration, "/endpoints/register")
api.add_resource(accounts.acmang, "/endpoints/accounts/<string:client_id>")

#running and setting host port (local for nginx reverse proxy)
app.run(host='0.0.0.0', port=3141, debug=True)