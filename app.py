#flask dependencies
from flask import Flask, request
from flask_restful import Api, Resource, reqparse

#initiializing the flask webapp
app = Flask(__name__)
api = Api(app)

#custom dependencies
from lib.accounts.endpoints import account, login, verify, registration, reset, change
from lib.services.endpoints import services, service, actions

#grab .env file information
from dotenv import load_dotenv
load_dotenv()

#global headers
@app.after_request
def apply_caching(response):
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, authorization'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = '*'
    return response

#writing services endpoints
api.add_resource(services.services, "/endpoints/<string:client_id>/services")
api.add_resource(service.service, "/endpoints/<string:client_id>/services/<string:service_id>")
api.add_resource(actions.start, "/endpoints/<string:client_id>/services/<string:service_id>/start")
api.add_resource(actions.stop, "/endpoints/<string:client_id>/services/<string:service_id>/stop")
api.add_resource(actions.restart, "/endpoints/<string:client_id>/services/<string:service_id>/restart")

#writing account endpoints
api.add_resource(change.pw, "/endpoints/reset/<string:clientid>/<string:key>")
api.add_resource(reset.reset, "/endpoints/reset/<string:clientid>")
api.add_resource(registration.register, "/endpoints/register")
api.add_resource(verify.verify, "/endpoints/accounts/<string:client_id>/verify")
api.add_resource(account.account, "/endpoints/accounts/<string:client_id>")
api.add_resource(login.login, "/endpoints/login")

#running and setting host port (local for nginx reverse proxy)
if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3141, debug=False)