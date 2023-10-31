import tkinter as tk
from openpyxl import Workbook

# Initialize a list to store the data
data_list = []

# Create labels for counters
keys_NC = ["a", "s", "d", "f", "h", "j", "k", "l"]
keys_Caps = ["A", "S", "D", "F", "H", "J", "K", "L"]
n_keys = len(keys_NC)

# Create a function to update and log the data
def update_and_log(event):
    data = [counter_vars[i].get() for i in range(n_keys)]
    data_list.append(data)

    for i in range(n_keys):
        counter_vars[i].set(0)

# Create a function to save data to an Excel file
def save_to_excel():
    excel_file_path = "data.xlsx"  # Change the path as needed
    workbook = Workbook()
    sheet = workbook.active

    for data_row in data_list:
        sheet.append(data_row)

    workbook.save(excel_file_path)

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
    with open("text_data.txt", "r") as file:
        text_data = file.read().splitlines()
except FileNotFoundError:
    # If the file doesn't exist, initialize with empty values
    text_data = [""] * n_keys


for i in range(n_keys):
    tk.Label(root, text=keys_Caps[i]).grid(row=0, column=i*2, padx=30)
    text_label = tk.Label(root, text=text_data[i])
    text_label.grid(row=1, column=i*2)
    tk.Label(root, textvariable=counter_vars[i]).grid(row=2, column=i*2)
    tk.Button(root, text="-", command=lambda i=i: decrement_counter(i), bg="red").grid(row=3, column=i*2)
    

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

root.bind("<Key>", on_key)

# Bind the "Guardar e repôr a 0 (Enter)" button to the Enter key
root.bind("<Return>", update_and_log)

# Start the Tkinter main loop
root.mainloop()
