import websockets
import functools
import asyncio
import subprocess
import zmq
import time
import sys

async def listener(websocket, path, service):
  command = service['log_command']
  p = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, shell=True)
  prev_sd = "-1"
  while True:
    await websocket.send(p.stdout.readline())

def listen(service):
    asyncio.set_event_loop(asyncio.new_event_loop())
    bound_handler = functools.partial(listener, service=service)
    start_server = websockets.serve(bound_handler, '127.0.0.1', service['port'])
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
