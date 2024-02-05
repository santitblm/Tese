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

def apply_random_blur(image, resize_factor): # Average or motion blur
    if random.random() < 0.5 and resize_factor > 0.6:
        kernel_size = random.choice([1, 11, 13, 15]) # 1/6 chance of no blur, the kernel from 11 to 19
  
        # Create the vertical kernel.
        kernel_h = np.zeros((kernel_size, kernel_size))
        
        # Fill the middle row with ones.
        kernel_h[int((kernel_size - 1)/2), :] = np.ones(kernel_size)
        
        # Normalize.
        kernel_h /= kernel_size

        # Apply the horizontal kernel.
        blurred_image = cv2.filter2D(image, -1, kernel_h)
    else:
        if resize_factor > 0.6:
            kernel_size = random.choice([1, 3, 5, 7, 9])
        else:
            kernel_size = random.choice([1, 3])
        blurred_image = cv2.blur(image, (kernel_size, kernel_size))
    return blurred_image

def apply_random_brightness_contrast_saturation(image):
    brightness_reduction = random.uniform(0, -20)
    contrast_factor = random.uniform(0.9, 1.1)
    adjusted_image = cv2.convertScaleAbs(image, alpha=contrast_factor, beta=brightness_reduction)
    # Adjust the image's saturation randomly
    if random.random() < 0.5:
        saturation_factor = random.uniform(0.3, 0.8)
        hsv_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2HSV)
        hsv_image[:, :, 1] = hsv_image[:, :, 1] * saturation_factor
        adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    return adjusted_image

def apply_random_noise(image, noise_prob=0.67):
    if random.random() < noise_prob:
        noise_types = ['gaussian', 'speckle']
        chosen_noise = random.choice(noise_types)#, p = [0.33, 0.67])
        
        if chosen_noise == 'gaussian':
            #print ("Gaussian noise")
            noise = np.random.normal(0.4, 1, image.shape).astype(np.uint8)
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

def apply_shadow(image):
    # Add a shadow to the image with a 35% chance of occurrence
    if random.random() < 0.35:
        # Get image width and height
        height, width, _ = image.shape

        # Generate random points on the left and right sides of the image
        left_point = (0, random.randint(0, height - 1))
        right_point = (width - 1, random.randint(0, height - 1))

        # Define a line between the two points
        line_coefficients = np.polyfit([left_point[0], right_point[0]], [left_point[1], right_point[1]], 1)
        a, b = line_coefficients

        # Create a mesh grid of X and Y coordinates
        Y, X = np.meshgrid(range(height), range(width), indexing='ij')

        # Use the equation of the line to check which pixels are above the line
        above_line_mask = Y < (a * X + b)

        # Adjust the brightness of pixels above the line
        # Randomly choose a value between 0.3 and 0.6
        brightness_reduction = random.random() * 0.3 + 0.3
        image[above_line_mask] = np.clip(image[above_line_mask]*brightness_reduction, 0, 255)
    return image

def apply_random_temperature_change(image):
    # Define the temperature adjustment factor (positive for warmer, negative for cooler)
    temperature_factor = random.random()*0.5 - 0.25  # You can adjust this value as needed

    # Increase the blue channel (for warmth) and decrease the blue channel (for coolness)
    blue_channel = np.clip(image[:, :, 0] * (1 + temperature_factor), 0, 255).astype(np.uint8)
    red_channel = np.clip(image[:, :, 2] * (1 - temperature_factor), 0, 255).astype(np.uint8)

    # Create the output image with adjusted channels
    adjusted_image = image.copy()
    adjusted_image[:, :, 0] = blue_channel
    adjusted_image[:, :, 2] = red_channel
    return adjusted_image

def apply_random_resize(image):
    # Define the resize factor (randomly chosen between 0.25 and 1)
    resize_factor = random.uniform(0.25, 1.0)
    # Resize the image
    resized_image = cv2.resize(image, None, fx=resize_factor, fy=resize_factor, interpolation=cv2.INTER_CUBIC)
    return resized_image, resize_factor

def apply_random_colors(image, p=0.70):
    """
    Apply one of the three transformations to the input image based on probability:
    1. Original image with probability p
    2. Random channel set to 0 with probability (1-p)/2
    3. Negative of the original image with probability (1-p)/2

    Parameters:
    - image: Input RGB image (numpy array).
    - p: Probability of keeping the original image.

    Returns:
    - Transformed image.
    """
    # Ensure the image is in the correct format (RGB)
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError("Input image must be a 3-channel RGB image.")

    # Randomly choose a transformation based on probability
    rand_num = random.random()

    if rand_num < p:
        # Option 1: Original image
        transformed_image = image.copy()
    elif rand_num < p + (1 - p) / 2:
        # Option 2: Randomly set 1 or 2 channels to 0
        num_channels_to_zero = random.choice([1, 2])
        channels_to_zero = random.sample([0, 1, 2], num_channels_to_zero)
        transformed_image = image.copy()
        transformed_image[:, :, channels_to_zero] = 0
    else:
        # Option 3: Negative of the original image
        transformed_image = cv2.bitwise_not(image)

    return transformed_image

def apply_chromatic_aberration(image, max_shift=1):
    # Split the image into its color channels
    b, g, r = cv2.split(image)

    # Generate random shifts for each channel
    shift_b = np.random.randint(-max_shift, max_shift + 1)
    shift_g = np.random.randint(-max_shift, max_shift + 1)
    shift_r = np.random.randint(-max_shift, max_shift + 1)

    # Shift the color channels
    b_shifted = np.roll(b, shift_b, axis=(0, 1))
    g_shifted = np.roll(g, shift_g, axis=(0, 1))
    r_shifted = np.roll(r, shift_r, axis=(0, 1))

    # Merge the shifted channels back into an image
    shifted_image = cv2.merge([b_shifted, g_shifted, r_shifted])

    # Clip values to ensure they are within the valid range [0, 255]
    shifted_image = np.clip(shifted_image, 0, 255).astype(np.uint8)

    return shifted_image


def apply_random_transformations(image):
    image = apply_random_noise(image)
    image, matrix_used = apply_random_homography(image)
    image = apply_random_temperature_change(image)
    image = apply_shadow(image)
    image = apply_chromatic_aberration(image)
    image, resize_factor = apply_random_resize(image)
    image = apply_random_blur(image, resize_factor)
    image = apply_random_brightness_contrast_saturation(image)
    image = apply_random_colors(image)

    return image, matrix_used, resize_factor

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
