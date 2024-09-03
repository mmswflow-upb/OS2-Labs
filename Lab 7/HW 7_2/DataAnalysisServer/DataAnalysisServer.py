import socket
import threading

import DataAnalysisModule as DAM
import random

import os
import time
import inspect

PORT = 5050
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)



def handle_client(conn, addr):

    print(f"\n[NEW CONNECTION] {addr} connected.")
    os.chdir(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))))

    while True:
        #receive the csv file name from the client
        try:
            csv_file_name = conn.recv(2048).decode(FORMAT)
        except Exception as e:
            print(f"\n[CLIENT] {addr} disconnected.")
            return

        print(f"\n[CLIENT] {addr} requested the analysis for the file: {csv_file_name}\n")
        if (csv_file_name == ""):
            return

        habit_options = ['eating', 'running', 'sleeping', 'working', 'playing']
        location_options = ['Bucuresti', 'Cluj-Napoca', 'Timisoara', 'Iasi', 'Constanta']

        # Initialize the environment
        envTemperature = random.randint(20, 45)
        noiseLevel = random.randint(30, 80)
        environment = DAM.Environment( envTemperature, 50, "Clear", noiseLevel)

        # Initialize the virtual space
        vspace = DAM.VirtualSpace(100, "Bucuresti", [], [], environment)

        # Initialize the reasoning system
        dbcon = DAM.DBConnection("Connect1")
        reasoning = DAM.Reasoning(dbcon, vspace, csv_file_name+".csv")  # Provide the correct path to your CSV file

        # Assign diseases to the people

        try:
            reasoning.getCases()
            print("File found and read successfully")

        except FileNotFoundError as e:
            conn.send("exit".encode(FORMAT))
            continue
            

        vspace.people = reasoning.refSmartHome.people
        
        #Assemble the message to be sent to the client

        analysis_lines = "Reading the results of the analysis...\n" + "With the temperature at " + str(envTemperature) + " degrees and the noise level at " + str(noiseLevel) + " dB, we have the following patients:\n"



        for i,person in enumerate(vspace.people):
            
            habit = random.choice(habit_options)
            location = random.choice(location_options)

            person.habit = habit
            person.location = location
            
            msg = f"Person {i+1} (Habit: {person.habit}, Location: {person.location}) has {person.disease.name} with severity {person.disease.severity}\n"

            analysis_lines += msg
        
        print(f"The message: {analysis_lines}\n")
        conn.send(analysis_lines.encode(FORMAT))

def start():
    server.listen()
    print(f"\n[LISTENING] Server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client,args=(conn,addr))
        thread.start()

if __name__ == "__main__":
    print("[STARTING] server is starting...")
    start()