#custom dependencies
from lib.accounts.endpoints import account, login, verify, registration
from lib import services, sockets

#flask dependencies
from flask import Flask, request
from flask_restful import Api, Resource, reqparse

#runs the sockets, what else? lol
sockets.run()

#initiializing the flask webapp
app = Flask(__name__)
api = Api(app)

#global headers
@app.after_request
def apply_caching(response):
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, authorization'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response

#writing services endpoints
api.add_resource(services.manager, "/endpoints/<string:client_id>/services")
api.add_resource(services.manager_indv, "/endpoints/<string:client_id>/services/<string:service_id>")
api.add_resource(services.start, "/endpoints/<string:client_id>/services/<string:service_id>/start")
api.add_resource(services.stop, "/endpoints/<string:client_id>/services/<string:service_id>/stop")
api.add_resource(services.restart, "/endpoints/<string:client_id>/services/<string:service_id>/restart")

#writing account endpoints
api.add_resource(registration.register, "/endpoints/register")
api.add_resource(verify.verify, "/endpoints/accounts/<string:client_id>/verify")
api.add_resource(account.account, "/endpoints/accounts/<string:client_id>")
api.add_resource(login.login, "/endpoints/login")

#running and setting host port (local for nginx reverse proxy)
app.run(host='127.0.0.1', port=3141, debug=True)
