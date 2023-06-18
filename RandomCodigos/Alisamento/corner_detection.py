import cv2
import os
import numpy as np

# Folder path containing the images
folder_path = 'C:/Users/Santi LM/Downloads/cropped'

# Create lists to store the original images and corner images
original_images = []
corner_images = []

# Iterate through the files in the folder
for filename in os.listdir(folder_path):
    # Check if the file is an image
    if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
        # Load the image
        image_path = os.path.join(folder_path, filename)
        image = cv2.imread(image_path)

        # Convert the image to grayscale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Harris Corner Detection
        corner_image = cv2.cornerHarris(gray, 2, 3, 0.04)

        # Dilate the corner points to mark them clearly
        corner_image = cv2.dilate(corner_image, None)

        # Threshold the corner image to obtain strong corners
        threshold = 0.01 * corner_image.max()
        corner_image[corner_image > threshold] = 255

        # Convert corner points to white pixels
        corner_image[corner_image != 255] = 0

        # Store the original and corner images
        original_images.append(image / 255.0)  # Divide by 255 to change range to 0-1
        corner_images.append(corner_image)

# Combine and display the images
for i in range(len(original_images)):
    # Resize the images to have the same height
    max_height = max(original_images[i].shape[0], corner_images[i].shape[0])
    resized_original = cv2.resize(original_images[i], (int(original_images[i].shape[1] * max_height / original_images[i].shape[0]), max_height))
    resized_corner = cv2.resize(corner_images[i], (int(corner_images[i].shape[1] * max_height / corner_images[i].shape[0]), max_height))

    # Convert the corner image to color to match the original image's channels
    corner_rgb = cv2.cvtColor(resized_corner, cv2.COLOR_GRAY2BGR)

    # Concatenate the original image and the corner image horizontally
    combined_image = np.concatenate((resized_original, corner_rgb), axis=1)

    # Display the combined image
    cv2.imshow('Corner Detection', combined_image)

    # Wait for a key press
    key = cv2.waitKey(0)

    # Check if the 'q' key was pressed to quit
    if key == ord('q'):
        break

cv2.destroyAllWindows()
