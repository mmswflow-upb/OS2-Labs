import tkinter as tk

#CONSTANTS
FONT1 = ("Arial", 15)
FONT2 = ("Arial", 10)

#FUNCTIONS
def factorial(n):
    if n == 0 or n < 0:
        return 1
    else: 
        return n * factorial(n-1)
def power(n,m):
    return pow(n,m)

def factorial_btn_click():
    
    n = factorial_textbox.get()

    if (n == None):
        result_factorial_label.config(text="Please enter a valid number")
        return
    
    n = int(n)
    
    result = factorial(n)
    result_factorial_label.config(text="Calculated factorial: " + str(result))

def power_btn_click():
    
    n = base_n_textbox.get()
    m = power_m_textbox.get()

    if (n == None or m == None):
        result_power_label.config(text="Please enter a valid number")
        return
    
    n = float(n)
    m = float(m)
    
    result = power(n,m)
    result_power_label.config(text="Calculated power: " + str(result))

#SETTING UP THE WINDOW

window = tk.Tk()

#Setup the window properties & layouts

window.title("Lab 8 Ex 3")
window.geometry("500x500")
window.columnconfigure(0, weight=1)

window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=4)


#WIDGETS

#Frames & labels Widgets

title_label = tk.Label(window, text="Factorials & Powers\nCalculator", font=FONT1)

input_frame = tk.Frame(window)

factorial_label = tk.Label(input_frame, text="Factorial of: ", font=FONT2)
base_n_label = tk.Label(input_frame, text="Base n: ", font=FONT2)
power_m_label = tk.Label(input_frame, text="Power m: ", font=FONT2)

#Output Widgets

result_factorial_label = tk.Label(input_frame, text="Calculated factorial: ", font=FONT2, wraplength=100)
result_power_label = tk.Label(input_frame, text="Calculated power: ", font=FONT2, wraplength=100)

#Input Widgets

factorial_textbox = tk.Entry(input_frame, font=FONT2)
compute_factorial_button = tk.Button(input_frame,text="Compute Factorial", font=FONT2, command=factorial_btn_click)

base_n_textbox = tk.Entry(input_frame, font=FONT2)
power_m_textbox = tk.Entry(input_frame, font=FONT2)
compute_power_button = tk.Button(input_frame,text="Compute Power", font=FONT2, command=power_btn_click)

#LAYOUTS

#Frames & labels Widget Layout


title_label.grid(row=0,column=0,sticky="sn")

input_frame.grid(row=1,column=0,sticky="nsew")
input_frame.columnconfigure((0,1,2,3), weight=1, uniform="a")
input_frame.rowconfigure((0,1,2), weight=1, uniform="a")

factorial_label.grid(row=0,column=0, sticky="e")

base_n_label.grid(row=0,column=2, sticky="e")
power_m_label.grid(row=1,column=2, sticky="e")

#Output Widget Layout
result_factorial_label.grid(row=1,column=0, sticky="e")
result_power_label.grid(row=2,column=2, sticky="e")


#Input Widget Layout

factorial_textbox.grid(row = 0, column=1, sticky="w")
compute_factorial_button.grid(row = 1, column=1, sticky="w")

base_n_textbox.grid(row = 0, column=3, sticky="w")
power_m_textbox.grid(row = 1, column=3, sticky="w")
compute_power_button.grid(row = 2, column=3, sticky="w")




#Run the main loop
window.mainloop()