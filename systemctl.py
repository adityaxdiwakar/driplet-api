import subprocess

def listen(service_name):
  command = f"journalctl -u {service_name} -f"
  p = subprocess.Popen(command, stdout=subprocess.PIPE, bufsize=1, shell=True)
  while True:
    print(p.stdout.readline())