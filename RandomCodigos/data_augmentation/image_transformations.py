'''The goal of this function is to apply random transformations to an image 
and be called with just one line of code "apply_random_transformations(image)".'''


import cv2
import numpy as np
import random

def apply_random_homography(image, max_skew=15, max_rotation=10, max_stretch=0.15):
    height, width, _ = image.shape

    skew_angle = random.uniform(-max_skew, max_skew)
    rotation_angle = random.uniform(-max_rotation, max_rotation)
    stretch_factor_x = 1 + random.uniform(-max_stretch, max_stretch)  # Stretch factor in x direction
    stretch_factor_y = 2 - stretch_factor_x#+ random.uniform(-max_stretch, max_stretch)  # Stretch factor in y direction

    # Apply skewing to the skew matrix
    skew_matrix = np.array([[1, np.tan(np.radians(skew_angle)), 0],
                            [0, 1, 0],
                            [0, 0, 1]])

    # Apply stretching to the skew matrix
    stretch_matrix = np.array([[stretch_factor_x, 0, 0],
                               [0, stretch_factor_y, 0],
                               [0, 0, 1]])

    rotation_matrix = cv2.getRotationMatrix2D((width/2, height/2), rotation_angle, 1)

    # Combine skew, stretch, and rotation matrices
    combined_matrix = np.dot(np.dot(rotation_matrix, skew_matrix), stretch_matrix)

    # Calculate new dimensions to include all original image pixels
    corners = np.array([[0, 0, 1],
                        [width, 0, 1],
                        [0, height, 1],
                        [width, height, 1]])
    
    transformed_corners = np.dot(corners, combined_matrix.T)
    
    min_x, min_y = np.min(transformed_corners[:, :2], axis=0)
    max_x, max_y = np.max(transformed_corners[:, :2], axis=0)
    
    new_width = int(np.ceil(max_x - min_x))
    new_height = int(np.ceil(max_y - min_y))

    # Adjust the translation part of the combined matrix
    combined_matrix[0, 2] -= min_x
    combined_matrix[1, 2] -= min_y

    warped_image = cv2.warpAffine(image, combined_matrix[:2], (new_width, new_height), borderMode=cv2.BORDER_REPLICATE)
    #print(f"skew_angle: {skew_angle}, rotation_angle: {rotation_angle}, stretch_factor_x: {stretch_factor_x}, stretch_factor_y: {stretch_factor_y}")
    return warped_image, combined_matrix


def apply_random_blur(image):
    kernel_size = random.choice([1, 3, 5])
    blurred_image = cv2.GaussianBlur(image, (kernel_size, kernel_size), 0)
    return blurred_image

def apply_random_brightness_contrast(image):
    brightness_reduction = random.uniform(0, -20)
    contrast_factor = random.uniform(0.9, 1.1)
    
    adjusted_image = cv2.convertScaleAbs(image, alpha=contrast_factor, beta=brightness_reduction)
    return adjusted_image

def apply_random_noise(image, noise_prob=0.67):
    if random.random() < noise_prob:
        noise_types = ['gaussian', 'speckle']
        chosen_noise = random.choice(noise_types)#, p = [0.33, 0.67])
        
        if chosen_noise == 'gaussian':
            #print ("Gaussian noise")
            noise = np.random.normal(0, 1, image.shape).astype(np.uint8)
            noisy_image = cv2.add(image, noise)
        elif chosen_noise == 'speckle':
            #print ("Speckle noise")
            speckle = np.random.randn(*image.shape) * 0.1
            noisy_image = np.clip(image + image * speckle, 0, 255).astype(np.uint8)

        
        noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
        return noisy_image
    #else:
        #print ("No noise")
    return image

def apply_random_transformations(image):
    noisy_result = apply_random_noise(image)
    homography_result, matrix_used = apply_random_homography(noisy_result)
    blurred_result = apply_random_blur(homography_result)
    final_result = apply_random_brightness_contrast(blurred_result)

    return final_result, matrix_used

#output = "C:\\Users\\Santi LM\\Documents\\GitHub\\Tese\\RandomCodigos\\RandomCodigos\\output\\"
# Load an example image
#input_image = cv2.imread('C:\\Users\\Santi LM\\Documents\\GitHub\\Tese\\RandomCodigos\\RandomCodigos\\input_image.jpg')

#for i in range(100):
    # Apply random transformations
#    output_image = apply_random_transformations(input_image)
#    cv2.imwrite(output + f'output_{i}.jpg', output_image)
# Display the input and output images
#cv2.imshow('Input Image', input_image)

#cv2.waitKey(0)
#cv2.destroyAllWindows()
