import os
from ultralytics import YOLO

# Set the folder path containing the images
folder_path = '/home/santilm/Downloads/k/'#Desktop/Tese/datasets/PT_LP_Characters/test/images/'

model = YOLO("runs/detect/PT_LP_Characters_x/weights/best.pt")

# Get a list of image file names in the folder
image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

# Iterate through the image files
for image_file in image_files:

    # Get the path to the current image
    source = folder_path + image_file

    # Predict results and save them to a txt file 
    # (Directory is common so double check if doing the right thing)
    results = model(source, save_txt = True, save_conf = False)
