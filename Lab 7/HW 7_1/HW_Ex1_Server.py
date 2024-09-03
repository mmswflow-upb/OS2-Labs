import socket
import threading

PORT = 5050
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
ROWS = 5

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)



def scytale_encryption(msg):
    
    
    """
    Encryption: 
    Transpose from rows to columns

    HELLO 
    THERE 

    len = 10;  rows = 5; cols = len / rows = 2

    Construct encryption matrix:

    H T
    E H
    L E
    L R
    O E

    Read row by row to get encrypted message: HTEHLELROE

    Encryption key is the number of rows used to construct the encryption matrix. (size of scytale)
    """
    
    #Remove spaces and convert to uppercase
    msg = list(msg.upper().replace(" ", ""))
    encrypted_msg = ""
    
    if (len(msg) % ROWS != 0): #Add padding if necessary
        msg += " "*(ROWS - len(msg)%ROWS)
    
    num_columns = len(msg)//ROWS
    
    
    encryption_matrix = [[0]*num_columns for i in range(ROWS)]

    k = 0
    #Transposing characters from rows to columns
    for j in range(num_columns):
        for i in range(ROWS):
            encryption_matrix[i][j] = msg[k]
            k += 1

    #Reading matrix row by row to get encrypted message
    print("\n[ENCRYPTION MATRIX]")
    for i in range(ROWS):
        for j in range(num_columns):
            encrypted_msg += encryption_matrix[i][j]
            print(encryption_matrix[i][j], end=" ")
        print()

    print(f"\n[ENCRYPTED MESSAGE] {encrypted_msg}")
    return encrypted_msg

def handle_client(conn, addr):
    
    print(f"\n[NEW CONNECTION] {addr} connected.")

    msg = conn.recv(2048).decode(FORMAT)

    print(f"[{addr}] {msg}")
    encrypted_msg = scytale_encryption(msg)
    conn.send(encrypted_msg.encode(FORMAT))    

def start():
    server.listen()
    print(f"\n[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()

print("\n[STARTING] Server is starting...")
start()