import os
import cv2
import shutil

# Input and output folder paths
input_folder = '/home/santilm/Desktop/Tese/datasets/License_Plates/Cropped'
output_folder = '/home/santilm/Downloads/retiradas'

# Iterate over files in the input folder
for filename in os.listdir(input_folder):
    file_path = os.path.join(input_folder, filename)
    
    # Check if the file is an image
    if not os.path.isfile(file_path) or not any(filename.lower().endswith(ext) for ext in ['.jpg', '.jpeg', '.png', '.gif']):
        continue
    
    # Read the image using OpenCV
    img = cv2.imread(file_path)
    
    # Check if the image is valid
    if img is None:
        continue
    
    # Get the height of the image
    image_height = img.shape[0]
    
    # Check if the image height is less than 10 pixels
    if image_height < 15:
        # Construct the destination path in the output folder
        dest_path = os.path.join(output_folder, filename)
        
        # Move the image to the output folder
        shutil.move(file_path, dest_path)
        print(f"Moved {filename} to {dest_path}")
