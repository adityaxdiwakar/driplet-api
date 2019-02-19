import websockets
import functools
import asyncio
import subprocess
import zmq
import threading
import time
import sys
import os
import json

async def listener(websocket, path, service):
  command = service['log_command']
  p = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, shell=True)
  while True:
    await websocket.send(p.stdout.readline())

def listen(service):
    asyncio.set_event_loop(asyncio.new_event_loop())
    bound_handler = functools.partial(listener, service=service)
    start_server = websockets.serve(bound_handler, '127.0.0.1', service['port'])
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

def run():
    users = os.listdir("bin")
    for user in users:
        services = json.load(
            open(f"bin/{user}/services.json")
        )
        for service in services:
            thread = threading.Thread(target=listen, args=[service], name=f"{users}:{service['id']}")
            thread.start()