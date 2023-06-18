import cv2
import os
import numpy as np

def binarize_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to create a binary image
    _, binary_image = cv2.threshold(grayscale_image, 127, 255, cv2.THRESH_BINARY_INV)
    
    # Find white pixels and set them to 1
    binary_image[binary_image == 255] = 1
    
    # Show the original and binary images
    cv2.imshow("Original Image", image)
    cv2.imshow("Binary Image", binary_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Folder path containing the images
folder_path = "C:/Users/Santi LM/Downloads/cropped"

# Iterate over images in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(('.png', '.jpg', '.jpeg')):  # Filter files based on extensions if needed
        image_path = os.path.join(folder_path, file_name)
        binarize_image(image_path)
