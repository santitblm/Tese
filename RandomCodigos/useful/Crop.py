'''This function is used to crop the LPs out of the images according to their labels'''

import os
import cv2

# Define the directory paths

# Uncomment for Windows
#image_dir = "C:/Users/Santi LM/Downloads/train/images"
#label_dir = "C:/Users/Santi LM/Downloads/train/labels"
#cropped_img_dir = "C:/Users/Santi LM/Downloads/train/images/cropped"

# Uncomment for Linux
#image_dir = "/home/santilm/Desktop/Tese/datasets/License_Plates/train/images"
#label_dir = "/home/santilm/Desktop/Tese/datasets/License_Plates/train/labels"
#cropped_img_dir = "/home/santilm/Desktop/Tese/datasets/License_Plates/Cropped"

image_dir = "C:/Users/Vastingood/Downloads/LPs_quadradas/images/"
label_dir = "C:/Users/Vastingood/Downloads/LPs_quadradas/obj_train_data/"
cropped_img_dir = "C:/Users/Vastingood/Downloads/LPs_quadradas/images_cropped/"

# Get a list of image filenames
image_files = os.listdir(image_dir)

# Iterate through the image files
for image_file in image_files:
    # Check if it's an image file
    if image_file.endswith(".jpg") or image_file.endswith(".png") or image_file.endswith(".jpeg"):
        image_name = os.path.splitext(image_file)[0]
        label_file = os.path.join(label_dir, f"{image_name}.txt")

        # Check if the label file exists and is not empty
        if os.path.isfile(label_file) and os.path.getsize(label_file) > 0:
            with open(label_file, "r") as f:
                lines = f.readlines()

            # Open the original image to get its dimensions
            image_path = os.path.join(image_dir, image_file)
            img = cv2.imread(image_path)
            img_height, img_width, _ = img.shape

            # Iterate through the lines in the label file
            for i, line in enumerate(lines):
                line = line.strip().split()

                # Extract the relevant coordinates (scaled to the original image)
                x = float(line[1]) * img_width
                y = float(line[2]) * img_height
                width = float(line[3]) * img_width
                height = float(line[4]) * img_height

                # Calculate the cropping coordinates
                left = int(x - width / 2)
                top = int(y - height / 2)
                right = int(x + width / 2)
                bottom = int(y + height / 2)

                # Crop the image
                cropped_img = img[top:bottom, left:right]

                # Save the cropped image
                cropped_img_name = f"{i}_{image_name}.jpg"
                cropped_img_path = os.path.join(cropped_img_dir, cropped_img_name)
                cv2.imwrite(cropped_img_path, cropped_img)
                print(f"Saved cropped image: {cropped_img_name} to {cropped_img_dir}")

print("Image cropping completed.")
