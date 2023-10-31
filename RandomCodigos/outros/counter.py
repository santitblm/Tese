import tkinter as tk
from openpyxl import Workbook

# Initialize a list to store the data
data_list = []

# Create a function to update and log the data
def update_and_log():
    pedestrianenter_count = pedestrianenter_var.get()
    bicycleenter_count = bicycleenter_var.get()
    scooterenter_count = scooterenter_var.get()
    pedestrianexit_count = pedestrianexit_var.get()
    bicycleexit_count = bicycleexit_var.get()
    scooterexit_count = scooterexit_var.get()
    data_list.append([pedestrianenter_count, pedestrianexit_count, bicycleenter_count, bicycleexit_count, scooterenter_count, scooterexit_count])
    
    pedestrianenter_var.set(0)
    pedestrianexit_var.set(0)
    bicycleenter_var.set(0)
    bicycleexit_var.set(0)
    scooterenter_var.set(0)
    scooterexit_var.set(0)

# Create a function to save data to an Excel file
def save_to_excel():
    excel_file_path = "RandomCodigos/outros/data.xlsx"  # Change the path as needed
    workbook = Workbook()
    sheet = workbook.active

    for data_row in data_list:
        sheet.append(data_row)

    workbook.save(excel_file_path)

# Create the main window
root = tk.Tk()
root.title("Counter App")

# Create variables for counter values
pedestrianenter_var = tk.IntVar()
pedestrianexit_var = tk.IntVar()
bicycleenter_var = tk.IntVar()
bicycleexit_var = tk.IntVar()
scooterenter_var = tk.IntVar()
scooterexit_var = tk.IntVar()

# Create labels and buttons for counters
counter_labels = ["Pedestrian+", "Pedestrian-", "Bicycle+", "Bicycle-", "Scooter+", "Scooter-"]
counters = [pedestrianenter_var, pedestrianexit_var, bicycleenter_var, bicycleexit_var, scooterenter_var, scooterexit_var]

button_colors = {"Display": "gray", "+": "green", "-": "red", "Log": "yellow", "Save to Excel": "green", "Close": "red"}

# Arrange counters side by side using the grid layout
for i, (label, var) in enumerate(zip(counter_labels, counters)):
    tk.Label(root, text=label).grid(row=i+1, column=0, sticky='w')
    display_label = tk.Label(root, textvariable=var)
    display_label.grid(row=i+1, column=1)
    tk.Button(root, text="+", command=lambda v=var: v.set(v.get() + 1), bg=button_colors["+"]).grid(row=i+1, column=4)
    tk.Button(root, text="-", command=lambda v=var: v.set(v.get() - 1), bg=button_colors["-"]).grid(row=i+1, column=3)

# Create a "Log" button
log_button = tk.Button(root, text="Log", command=update_and_log, bg=button_colors["Log"])
log_button.grid(row=len(counter_labels)+1, column=0)

# Create a "Save to Excel" button
save_button = tk.Button(root, text="Save to Excel", command=save_to_excel, bg=button_colors["Save to Excel"])
save_button.grid(row=0, column=0)


# Start the Tkinter main loop
root.mainloop()
