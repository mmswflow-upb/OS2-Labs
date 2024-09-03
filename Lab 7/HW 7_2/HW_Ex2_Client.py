import pyttsx3
import speech_recognition as SR
import socket
import time

PORT = 5050
SERVER = "127.0.0.1"
FORMAT = "utf-8"
ADDR = (SERVER, PORT)
VOICE_RATE = 150

REC = SR.Recognizer()
TTS_ENGINE = pyttsx3.init()
TTS_ENGINE.setProperty('rate', VOICE_RATE)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def speak_text(text):
    TTS_ENGINE.say(text)
    TTS_ENGINE.runAndWait()


def listen_text():

    while True:

        try:
            with SR.Microphone() as source:
                
                print("Listening for CSV file name (dont say the file extension)...")
                
                #Wait for 0.2 seconds to let the recognizer adjust the energy threshold
                REC.adjust_for_ambient_noise(source, duration = 0.2)

                #Listen for the CSV file name
                audio = REC.listen(source, None, 1.5)

                #Using Google Speech Recognition
                csv_file_name = REC.recognize_google(audio).lower().replace(" ", "")

                print(f"\nYou said: {csv_file_name}\n")
                
                if (csv_file_name == ""):
                    
                    continue

                return csv_file_name
        
        except SR.RequestError as e1:

            print("Could not request results; {0}".format(e1))
        
        except SR.UnknownValueError as e2:

            print("Unknown error occured")

def send():
    
    sent_msg = listen_text().encode(FORMAT)

    while True:
    
        client.send(sent_msg)
        try:
            received_msg = client.recv(2048).decode(FORMAT)
           

        except Exception as e:
            print(f"\n[SERVER] disconnected.")
            return
        
        if (received_msg != "exit"):
            
            #Split the received message by new line and speak them one by one with a delay
            for line in received_msg.split("\n"):

                time.sleep(0.8)
                speak_text(line)
        else:
            print("Error assigning diseases to people\n")
            speak_text("Error assigning diseases to people")

        sent_msg = listen_text().encode(FORMAT)
           
                
            
if __name__ == "__main__":

    send()