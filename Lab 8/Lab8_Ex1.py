import tkinter as tk
import os

#CONSTANTS
FONT1 = ("Arial", 15)
FONT2 = ("Arial", 12)

#FUNCTIONS

def show_all_files():

    #Clear previous results
    for label in output_frame.winfo_children():
        label.destroy()

    filepath = path_textbox.get()

    try:
        files = os.listdir(filepath)
    
    except:
    
        file_name_label = tk.Label(output_frame, text="Invalid path", font=FONT2)
        file_name_label.pack()
        return
   

    if len(files) == 0:
    
        file_name_label = tk.Label(output_frame, text="No files found", font=FONT2)
        file_name_label.pack()
        return
    
    output_scrollbar = tk.Scrollbar(output_frame, orient="vertical")

    output_listbox = tk.Listbox(output_frame, yscrollcommand=output_scrollbar.set)
    for file in files:
        output_listbox.insert("end", file)

    output_scrollbar.pack(side="right", fill="y")
    output_listbox.pack(fill="both")
    output_scrollbar.config(command=output_listbox.yview)
    
#SETTING UP THE WINDOW

window = tk.Tk()

#Setup the window properties & layouts

window.title("Lab 8 Ex 1")
window.geometry("500x500")

window.rowconfigure(0, weight=1)
window.rowconfigure((1,2), weight=2)

window.columnconfigure(0, weight=1)


#WIDGETS


#Frames & labels Widgets
title_label = tk.Label(window, text="Content At Given Path", font=FONT1)

input_frame = tk.Frame(window)

path_label = tk.Label(input_frame, text="Path: ", font=FONT2)

output_frame = tk.Frame(window)


#Output Widgets

no_result_label = tk.Label(output_frame, text="No files found", font=FONT2)


#Input Widgets

path_textbox = tk.Entry(input_frame, font=FONT2)
search_path_button = tk.Button(input_frame, text="Search", font=FONT2, command=show_all_files)
#LAYOUTS

#Frames & labels Widget Layout
title_label.grid(row=0, sticky="sn")
input_frame.grid(row=1)

input_frame.rowconfigure(0, weight=1)
input_frame.columnconfigure((0,1,2), weight=1)

path_label.grid(row=0,column=0,sticky="e")

output_frame.grid(row=2, sticky="we")

#Output Widget Layout
no_result_label.pack()

#Input Widget Layout

path_textbox.grid(row=0, column=1, sticky="w")
search_path_button.grid(row=0,column=2, sticky="w")



#Run the main loop
window.mainloop()