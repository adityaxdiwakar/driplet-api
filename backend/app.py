#custom dependencies
from lib import services, accounts, sockets

#flask dependencies
from flask import Flask, request
from flask_restful import Api, Resource, reqparse

#initiializing the flask webapp
app = Flask(__name__)
api = Api(app)

#runs the sockets, what else? lol
sockets.run()

#writing services endpoints
api.add_resource(services.manager, "/endpoints/<string:client_id>/services")
api.add_resource(services.manager_indv, "/endpoints/<string:client_id>/services/<string:service_id>")
api.add_resource(services.start, "/endpoints/<string:client_id>/services/<string:service_id>/start")
api.add_resource(services.stop, "/endpoints/<string:client_id>/services/<string:service_id>/stop")
api.add_resource(services.restart, "/endpoints/<string:client_id>/services/<string:service_id>/restart")

#writing account endpoints
api.add_resource(accounts.registration, "/endpoints/register")
api.add_resource(accounts.acmang, "/endpoints/accounts/<string:client_id>")

#running and setting host port (local for nginx reverse proxy)
app.run(host='0.0.0.0', port=3141, debug=True)