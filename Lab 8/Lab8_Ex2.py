import tkinter as tk
import os

#CONSTANTS
FONT1 = ("Arial", 15)
FONT2 = ("Arial", 12)

#FUNCTIONS
def check_path():
    
    path = path_entry.get()

    if os.path.isdir(path):
        output_label.config(text="Answer: Yes")
    else:
        output_label.config(text="Answer: No")

#SETTING UP THE WINDOW

window = tk.Tk()

#Setup the window properties & layouts

window.title("Lab 8 Ex 2")
window.geometry("500x500")

window.columnconfigure(0,weight=1)
window.rowconfigure((0,2),weight=1)
window.rowconfigure(1,weight = 2)

#WIDGETS

#Frames & labels Widgets
title_label = tk.Label(window, text="Is Path A Directory", font=FONT1)

input_frame=tk.Frame(window)

path_label = tk.Label(input_frame, text="Path: ", font=FONT2)

#Output Widgets

output_label = tk.Label(window, text="Answer: ", font=FONT2)

#Input Widgets
path_entry=tk.Entry(input_frame, font=FONT2)
check_button=tk.Button(input_frame, text="Check", font=FONT2, command=check_path)


#LAYOUTS

#Frames & labels Widget Layout

title_label.grid(row=0, sticky="sn")
input_frame.grid(row=1)

input_frame.rowconfigure(0, weight=1)
input_frame.columnconfigure((0,1,2), weight=1)

path_label.grid(row=0,column=0,sticky="e")

#Output Widget Layout

output_label.grid(row=2, sticky="nwe")

#Input Widget Layout

path_entry.grid(row=0, column=1, sticky="w")
check_button.grid(row=0,column=2, sticky="w")
#Run the main loop
window.mainloop()