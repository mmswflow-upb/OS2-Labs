import socket


HEADER = 64
PORT = 5050
SERVER = "127.0.0.1"
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def decrypt(msg):
    decrypted_msg = ""
    for char in msg:
        if char.isalpha():
            if char.isupper():
                decrypted_char = chr((ord(char) - 65 - 3) % 26 + 65)
            else:
                decrypted_char = chr((ord(char) - 97 - 3) % 26 + 97)
            decrypted_msg += decrypted_char
        else:
            decrypted_msg += char
    return decrypted_msg

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    encrypted_msg = client.recv(2048).decode(FORMAT)
    print(f"[ENCRYPTED MESSAGE] {encrypted_msg}")
    print(f"[DECRYPTED MESSAGE] {decrypt(encrypted_msg)}")

send(input("Message to be sent: "))
send(DISCONNECT_MESSAGE)