import socket

ROWS = 5
PORT = 5050
SERVER = "127.0.0.1"
FORMAT = "utf-8"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)


def scytale_decryption(encrypted_msg):

    """
    Encrypted message: HTEHLELROE

    len = 10; rows = 5; cols = len / rows = 2

    reconstructing encryption matrix: 
    
    H T
    E H
    L E
    L R
    O E

    read column by column to get decrypted message: HELLOTHERE

    """

    decrypted_msg = ""

    num_columns = len(encrypted_msg)//ROWS
    
    encryption_matrix = [[0]*num_columns for i in range(ROWS)]

    k = 0
    #Transposing from rows to columns
    for i in range(ROWS):
        for j in range(num_columns):
            encryption_matrix[i][j] = encrypted_msg[k]
            k += 1

    for j in range(num_columns):
        for i in range(ROWS):
            decrypted_msg += encryption_matrix[i][j]
            
    
    return decrypted_msg

def send(msg):
    
    message = msg.encode(FORMAT)    
    client.send(message)
    encrypted_msg = client.recv(2048).decode(FORMAT)
    print(f"\n[ENCRYPTED MESSAGE] {encrypted_msg}")
    print(f"\n[DECRYPTED MESSAGE] {scytale_decryption(encrypted_msg)}")

send(input("Message to be sent: "))