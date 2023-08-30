import os
import cv2

username = "Santi LM"
# Define the folder containing the images
input_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/to_transform/"
output_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/transformed/"

# Get a list of all image files in the input folder
image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

#Flag to show the images
show = False

# Loop through each image file
for image_file in image_files:
    image_path = os.path.join(input_folder, image_file)

    # Read the image
    image = cv2.imread(image_path)

    # Apply Gaussian blur
    #gaussian_blur = cv2.GaussianBlur(image, (9, 9), 0)
    gaussian_blur = cv2.convertScaleAbs(image, alpha=2, beta=0)
    # Apply average blur
    #kernel_size = 9
    #average_blur = cv2.blur(image, (kernel_size, kernel_size))

    # Show the original, Gaussian blur, and average blur images
    if show:
        cv2.imshow('Original Image', image)
        #cv2.imshow('Gaussian Blur', gaussian_blur)
        #cv2.imshow('Average Blur', average_blur)

    # Save the modified images
    gaussian_output_path = os.path.join(output_folder, f'{image_file}')
    #average_output_path = os.path.join(output_folder, f'average_{image_file}')

    cv2.imwrite(gaussian_output_path, gaussian_blur)
    #cv2.imwrite(average_output_path, average_blur)

    # Wait for a key press and then close the windows
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
