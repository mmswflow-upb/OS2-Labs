import socket
import threading

HEADER = 64
PORT = 5050
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def encrypt(msg):
    encrypted_msg = ""
    for char in msg:
        if char.isalpha():
            if char.isupper():
                encrypted_char = chr((ord(char) - 65 + 3) % 26 + 65)
            else:
                encrypted_char = chr((ord(char) - 97 + 3) % 26 + 97)
            encrypted_msg += encrypted_char
        else:
            encrypted_msg += char
    return encrypted_msg

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    while (True):
        msg_length = conn.recv(HEADER).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                return

            print(f"[{addr}] {msg}")
            encrypted_msg = encrypt(msg)
            print(f"[ENCRYPTED MESSAGE] {encrypted_msg}")
            conn.send(encrypted_msg.encode(FORMAT))    
    conn.close()

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()

print("[STARTING] Server is starting...")
start()