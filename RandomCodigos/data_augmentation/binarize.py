import os
import cv2

# Update the username and paths as needed
username = "Vastingood"
input_path = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/"
output_path = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/binary_adaptive/"
adaptive = True
# Create the output directory if it doesn't exist
if not os.path.exists(output_path):
    os.makedirs(output_path)

image_files = [f for f in os.listdir(input_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

for image_file in image_files:
    # Load the image
    image_path = os.path.join(input_path, image_file)
    color_image = cv2.imread(image_path)
    
    # Convert color image to grayscale
    gray_image = cv2.cvtColor(color_image, cv2.COLOR_BGR2GRAY)
    
    if adaptive:
        # Apply adaptive thresholding for local binarization
        binarized_image = cv2.adaptiveThreshold(
            gray_image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2
        )
    else:
        # Apply global thresholding for binarization
        _, binarized_image = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    
    # Save the binarized image to the output folder
    output_image_path = os.path.join(output_path, image_file)
    cv2.imwrite(output_image_path, binarized_image)

    print(f"Binarized and saved: {output_image_path}")
