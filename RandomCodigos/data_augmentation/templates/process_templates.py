import os
import cv2

# Set the path to the templates folder and the target size
username = "Vastingood"
templates_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/templates/"
target_width = 500
target_height = 140

# Create the output folder if it doesn't exist
output_folder = os.path.join(templates_folder, "output")
os.makedirs(output_folder, exist_ok=True)

# Iterate through the images in the templates folder
for filename in os.listdir(templates_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(templates_folder, filename)

        # Read the image
        image = cv2.imread(image_path)

        if image is not None:
            # Apply Gaussian blur
            blurred_image = cv2.GaussianBlur(image, (5, 5), 0)

            # Resize the image
            resized_image = cv2.resize(blurred_image, (target_width, target_height))

            # Show the resulting image
            cv2.imshow("Resized Image", resized_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

            # Save the resulting image
            output_path = os.path.join(output_folder, filename)
            cv2.imwrite(output_path, resized_image)

print("Processing complete.")
