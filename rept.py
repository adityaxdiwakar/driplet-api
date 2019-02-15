import zmq
context = zmq.Context()
socket = context.socket(zmq.SUB)
# We can connect to several endpoints if we desire, and receive from all.
socket.connect('tcp://0.0.0.0:3142')
socket.setsockopt_string(zmq.SUBSCRIBE, '')

while True:
    message = socket.recv()
    print(message)