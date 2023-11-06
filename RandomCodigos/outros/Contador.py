import tkinter as tk
from openpyxl import Workbook
import os
import time
from datetime import date
import pygetwindow
import pyautogui

# Create a function to send a space key press to VLC
def pause_play_vlc():
    # Find the VLC window
    vlc_windows = pygetwindow.getWindowsWithTitle("VLC media player")
    if vlc_windows:
        vlc_window = vlc_windows[0]

        # Switch focus to VLC
        vlc_window.activate()

        # Send a space key press to VLC
        pyautogui.press('space')

        # Switch the focus back to your GUI
        root.focus_force()

# Initialize a list to store the data
data_list = []

# Create labels for counters
#keys_NC = ["a", "s", "d", "f", "h", "j", "k", "l"]
#keys_Caps = ["A", "S", "D", "F", "H", "J", "K", "L"]
keys_NC = ["e", "d", "r", "f", "t", "g", "7", "4", "8", "5", "9", "6"]
keys_Caps = ["E", "D", "R", "F", "T", "G", "7", "4", "8", "5", "9", "6"]

n_keys = len(keys_NC)

# Create a function to update and log the data
def enter(event):
    update_and_log()

def update_and_log():
    data = [counter_vars[i].get() for i in range(n_keys)]
    data_list.append(data)

    for i in range(n_keys):
        counter_vars[i].set(0)
    save_to_excel_temp()

# Create a function to temporarily save data to an Excel file
def save_to_excel_temp():
    excel_file_path = "C:/Users/Vastingood/Documents/Github/Tese/RandomCodigos/outros/"  # Change the path as needed
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(text_data)
    for data_row in data_list:
        sheet.append(data_row)

    workbook.save(excel_file_path + "temp_Resultados.xlsx")

# Create a function to save data to an Excel file
def save_to_excel():
    excel_file_path = "C:/Users/Vastingood/Documents/Github/Tese/RandomCodigos/outros/"  # Change the path as needed
    today = date.today()
    t = time.localtime()
    current_time = time.strftime("%H%M%S", t)

    workbook = Workbook()
    sheet = workbook.active
    sheet.append(text_data)
    for data_row in data_list:
        sheet.append(data_row)

    workbook.save(excel_file_path + f"Resultados_{today}_{current_time}.xlsx")

# Create a function to decrement counters
def decrement_counter(index):
    counter_vars[index].set(counter_vars[index].get() - 1)

# Create a main window
root = tk.Tk()
root.title("Contadores")

# Create variables for counters
counter_vars = [tk.IntVar() for _ in range(n_keys)]

# Load text data from a text file
text_data = []
try:
    with open("C:/Users/Vastingood/Documents/Github/Tese/RandomCodigos/outros/text_data.txt", "r") as file:
        text_data = file.read().splitlines()
except FileNotFoundError:
    # If the file doesn't exist, initialize with empty values
    text_data = [""] * n_keys

for n in range(2):
    for i in range(int(n_keys/2)):
        tk.Label(root, text=keys_Caps[2*i+n]).grid(row=5*n, column=i*2, padx=30)
        text_label = tk.Label(root, text=text_data[2*i+n])
        text_label.grid(row=5*n+1, column=i*2)
        tk.Label(root, textvariable=counter_vars[2*i+n]).grid(row=5*n+2, column=i*2)
        tk.Button(root, text="-", command=lambda i=2*i+n: decrement_counter(i), bg="red").grid(row=5*n+3, column=i*2)
    

tk.Label(root, text="").grid(row=4, column=0, pady=10)

# Create a "Log" button
log_button = tk.Button(root, text="Guardar e repôr a 0 (Enter)", command=update_and_log, bg="yellow")
log_button.grid(row=1, column=30, columnspan=8)

# Create a "Save to Excel" button
save_button = tk.Button(root, text="Save to Excel", command=save_to_excel, bg="green")
save_button.grid(row=3, column=30, columnspan=8)

# Create a key-press event handler to increment counters
def on_key(event):
    key = event.keysym
    if key in keys_NC:
        index = keys_NC.index(key)
        counter_vars[index].set(counter_vars[index].get() + 1)
    elif key in keys_Caps:
        index = keys_Caps.index(key)
        counter_vars[index].set(counter_vars[index].get() + 1)
    elif key == "space":
        # Pause/Play VLC
        pause_play_vlc()


root.bind("<Key>", on_key)

# Bind the "Guardar e repôr a 0 (Enter)" button to the Enter key
root.bind("<Return>", enter)

# Start the Tkinter main loop
root.mainloop()
