import os

directory = "C:/Users/Vastingood/Downloads/obj_train_data/"

for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)

            # Read lines from the file
            with open(file_path, 'r') as file:
                lines = file.readlines()
            if len(lines) != 6:
                 print(len(lines), " on ", filename)