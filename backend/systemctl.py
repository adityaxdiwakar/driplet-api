import subprocess, zmq, time, sys

def listen(service):
  context = zmq.Context()
  socket = context.socket(zmq.PUB)
  socket.bind(f"tcp://0.0.0.0:{service['port']}")
  command = service['log_command']
  p = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, shell=True)
  time.sleep(5)
  socket.send(p.stdout.readline())
  prev_sd = -1
  while True:
    if p.stdout.readline() != prev_sd:
      prev_sd = p.stdout.readline()
      socket.send(p.stdout.readline())