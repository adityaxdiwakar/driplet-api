#general requirements
import time, json, os, random, threading, asyncio

#API dependencies
from flask import Flask
from flask_restful import Api, Resource, reqparse

#helper functions
def check_dupe(list1, value):
    for item in list1:
        if item['id'] == value:
            return True
    return False

def get_service_id(client_services):
    while True:
        r = random.randint(1000000000,9999999999)
        if not check_dupe(client_services, r):
            return 's' + str(r)

def get_services(client_id):
    with open(f"bin/{client_id}/services.json", "r") as f:
        return json.load(f)

def push_services(data, client_id):
    with open(f"bin/{client_id}/services.json", "w") as f:
        json.dump(data, f, indent=4)

def allocate_new_port():
    used_ports = json.load(
        open("global_bin/used_ports.json", "r")
    )
    while True:
        r = random.randint(3142, 99999)
        if r not in used_ports:
            used_ports.append(r)
            json.dump(
                used_ports,
                open("global_bin/used_ports.json", "w"),
                indent = 4
            )
            return r

class manager(Resource):
    def get(self, client_id):
        return get_services(client_id)
    def post(self, client_id):
        user_services = get_services(client_id)
        
        parser = reqparse.RequestParser()
        parser.add_argument("name")
        parser.add_argument("start_command")
        parser.add_argument("stop_command")
        parser.add_argument("restart_command")
        parser.add_argument("status_command")
        parser.add_argument("log_command")
        args = parser.parse_args()
        
        service = {
            "name": args['name'],
            "id": get_service_id(get_services(client_id)),
            "start_command": args['start_command'],
            "stop_command": args['stop_command'],
            "restart_command": args['restart_command'],
            "status_command": args['status_command'],
            "log_command": args['log_command'],
            "port": allocate_new_port()
        }

        user_services.append(service)
        push_services(user_services, client_id)
        return service, 201

websockets = {}

class manager_indv(Resource):
    def get(self, client_id, service_id):
        services = get_services(client_id)
        for service in services:
            if service['id'] == service_id:
                websockets.update({
                    client_id: {
                        service_id: threading.Thread(
                            name=str(f"{client_id}:{service_id}"), 
                            target=systemctl.listen,
                            args=[service]
                        )
                    }
                })
                websockets[client_id][service_id].start()
                return service
        return {"message": "User could not be found", "code": 404}, 404
    def delete(self, client_id, service_id):
        services = get_services(client_id)
        for x in range(len(services)):
            if services[x]['id'] == service_id:
                preq = services[0:x] + services[x+1:len(services)+1]
                push_services(preq, client_id)
                return preq

class start(Resource):
    def post(self, client_id, service_id):
        services = get_services(client_id)
        for service in services:
            if service['id'] == service_id:
                os.system(service['start_command'])
                return service, 200

class stop(Resource):
    def post(self, client_id, service_id):
        services = get_services(client_id)
        for service in services:
            if service['id'] == service_id:
                os.system(service['stop_command'])
                return service, 200

class restart(Resource):
    def post(self, client_id, service_id):
        services = get_services(client_id)
        for service in services:
            if service['id'] == service_id:
                os.system(service['restart_command'])
                return service, 200