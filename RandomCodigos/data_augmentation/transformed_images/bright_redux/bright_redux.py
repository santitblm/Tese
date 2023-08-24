import os
import cv2

# Define paths
username = "Santi LM"
input_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/"
output_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/bright_redux"
brightness_reduction = 0  # Adjust brightness reduction factor as needed

# Iterate through each image in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(('.jpg', '.png', '.jpeg')):  # Add more extensions if needed
        input_path = os.path.join(input_folder, filename)

        # Load the image
        image = cv2.imread(input_path)

        # Apply brightness reduction
        adjusted_image = cv2.convertScaleAbs(image, alpha=2, beta=brightness_reduction)

        # Save the adjusted image to the same folder
        output_path = os.path.join(output_folder, f"{filename}")
        cv2.imwrite(output_path, adjusted_image)

print("Brightness adjustment complete.")
