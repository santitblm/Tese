import os
import shutil

# Directories A, B, and C
dir_a = "/home/santilm/Documents/GitHub/Tese/cropped/"
dir_b = "/home/santilm/Desktop/Tese/datasets/PT_LP_Characters/valid/images/"
dir_c = "/home/santilm/Desktop/Tese/datasets/PT_LP_Characters/train/images/"
dir_d = "/home/santilm/Desktop/Tese/datasets/PT_LP_Characters/test_nolabels/images/"

# Get the list of files in directories B and C
files_b = os.listdir(dir_b)
files_c = os.listdir(dir_c)
# Iterate through files in directory A
for filename in os.listdir(dir_a):
    file_path_a = os.path.join(dir_a, filename)
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        # Check if the file exists in directories B and C
        if filename not in files_b and filename not in files_c:
            # Copy the file from A to D
            shutil.copy(file_path_a, os.path.join(dir_d, filename))

print("Copying completed.")
