import os
import cv2
import numpy as np

def create_sum_binary_images(source_folder1, source_folder2, output_folder):
    # Create the output directory if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    image_files1 = [f for f in os.listdir(source_folder1) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    kernel = np.ones((1, 1), np.uint8)  # Define a kernel for morphological operations

    for image_file1 in image_files1:
        # Load binary images from both folders
        image_path1 = os.path.join(source_folder1, image_file1)
        image_path2 = os.path.join(source_folder2, image_file1)

        binary_image1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
        binary_image2 = cv2.imread(image_path2, cv2.IMREAD_GRAYSCALE)

        # Perform element-wise addition of the pixel values
        sum_image = cv2.add(binary_image1, binary_image2)

        # Perform a morphological closing operation
        closing_image = cv2.morphologyEx(sum_image, cv2.MORPH_CLOSE, kernel)

        # Save the closing image to the output folder
        output_image_path = os.path.join(output_folder, image_file1)
        cv2.imwrite(output_image_path, closing_image)

        print(f"Created and saved: {output_image_path}")

if __name__ == "__main__":
    username = "Vastingood"
    source_folder_adaptive = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/binary_adaptive/"
    source_folder_otsu = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/binary_otsu/"
    output_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/sum_with_closing/"

    create_sum_binary_images(source_folder_adaptive, source_folder_otsu, output_folder)
