import cv2
import numpy as np
import random
import os
import shutil

def apply_random_blur(image): # Average or motion blur
    p = random.random()

    if p <= 0.4:
        kernel_size = random.choice([1, 11, 13, 15, 17])
        kernel_h = np.zeros((kernel_size, kernel_size))
        kernel_h[int((kernel_size - 1)/2), :] = np.ones(kernel_size)
        kernel_h /= kernel_size
        blurred_image = cv2.filter2D(image, -1, kernel_h)

    elif p <= 0.9:
        kernel_size = random.choice([1, 3, 5])
        blurred_image = cv2.blur(image, (kernel_size, kernel_size))

    else:
        blurred_image = image
    return blurred_image

def apply_random_brightness_contrast_saturation(image):
    #brightness_reduction = random.uniform(10, -10)
    #contrast_factor = random.uniform(0.5, 1.3)
    #adjusted_image = cv2.convertScaleAbs(image, alpha=contrast_factor, beta=brightness_reduction)
    brightness_reduction = random.random() * 0.75 + 0.25
    image = np.clip(image*brightness_reduction, 0, 255)
    # Adjust the image's saturation randomly
    #if random.random() < 0.0:
    #    saturation_factor = random.uniform(0.1, 2.0)
    #    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #    hsv_image[:, :, 1] = hsv_image[:, :, 1] * saturation_factor
    #    adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
    return image

def apply_random_noise(image, noise_prob=0.85):
    if random.random() < noise_prob:
        noise_types = ['gaussian', 'speckle']
        chosen_noise = random.choice(noise_types)#, p = [0.33, 0.67])

        if chosen_noise == 'gaussian':
            #print ("Gaussian noise")
            #print(image)
            noise = np.random.normal(0.4, 1, image.shape).astype(np.uint8)
            noisy_image = cv2.add(image.astype(np.uint8), noise)
        elif chosen_noise == 'speckle':
            #print ("Speckle noise")
            speckle = np.random.randn(*image.shape) * 0.3
            noisy_image = np.clip(image + image * speckle, 0, 255).astype(np.uint8)


        noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
        return noisy_image
    #else:
        #print ("No noise")
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

def apply_random_resize(image, path, n, max_skew=20, max_rotation=15, max_stretch=0.5):
    image = image[10:-20, 10:-10]
    # Generate a random background color (RGBA)
    background_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    image[:, -1] = background_color
    image[-1, :] = background_color
    image[:, 0] = background_color
    image[0, :] = background_color

    height, width, _ = image.shape

    skew_angle = random.uniform(-max_skew, max_skew)
    rotation_angle = random.uniform(-max_rotation, max_rotation)

    stretch_factor_x = 1 + random.uniform(-max_stretch, max_stretch-0.1)  # Stretch factor in x direction
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
    
    resize = random.uniform(0.15, 0.4)
    resized_image = cv2.resize(warped_image, None, fx=resize, fy=resize, interpolation=cv2.INTER_CUBIC)
    
    # Get the height and width of the original image
    original_height, original_width, _ = warped_image.shape

    x_center_normalized = random.uniform(resize/2, 1-resize/2)
    y_center_normalized = random.uniform(resize/2, 1-resize/2)
    width_normalized = resize
    height_normalized = resize


    # Calculate the coordinates of the top-left corner based on center coordinates
    x_top_left = int((x_center_normalized - width_normalized / 2) * original_width)
    y_top_left = int((y_center_normalized - height_normalized / 2) * original_height)

    # Calculate the coordinates of the bottom-right corner based on center coordinates
    x_bottom_right = x_top_left + resized_image.shape[1]
    y_bottom_right = y_top_left + resized_image.shape[0]


    # Create a blank image with the same size as the original image and fill it with the background color
    new_image = np.full_like(warped_image, background_color, dtype=np.uint8)
    # Paste the cropped image onto the new image
    new_image[y_top_left:y_bottom_right, x_top_left:x_bottom_right] = resized_image

    with open(path + f"{n}.txt", "w") as f:
        f.write(f"1 {x_center_normalized} {y_center_normalized} {width_normalized} {height_normalized}")
    
    return new_image

def apply_random_colors(image, p=0.25):
    # Randomly choose a transformation based on probability
    rand_num = random.random()
    transformed_image = image.copy()

    if rand_num < p:
        transformed_image[:, :, 0] = 0

    return transformed_image

def apply_chromatic_aberration(image, max_shift=1):
    if random.random()<0.75:
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
    else:
        shifted_image = image
    return shifted_image

def create_new_images(images_path, new_images_path, new_labels_path):
    images_files = [f for f in os.listdir(images_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    n = 0
    new_images = 5 # Number of different images created from the original
    for image in images_files:
        image_path = os.path.join(images_path + image)
        image = cv2.imread(image_path)
        for i in range(new_images):
            new_image = apply_random_resize(image, new_labels_path, n)
            cv2.imwrite(new_images_path+f"{n}.jpg", new_image)
            n += 1
    return

def transforms(image):
    image = apply_random_noise(image)
    image = apply_random_temperature_change(image)
    image = apply_chromatic_aberration(image)
    image = apply_random_blur(image)
    image = apply_random_brightness_contrast_saturation(image)
    image = apply_random_colors(image)

    return image

#images_path = "C:/Users/Vastingood/Downloads/LPs_quadradas/transformed/"
#labels_path = "C:/Users/Vastingood/Downloads/LPs_quadradas/train/images/"
#new_images_path = "C:/Users/Vastingood/Downloads/LPs_quadradas/train/images/"
#new_labels_path = "C:/Users/Vastingood/Downloads/LPs_quadradas/train/labels/"
#newer_images_path = "C:/Users/Vastingood/Downloads/LPs_quadradas/train/images/new_images/"
#newer_labels_path = "C:/Users/Vastingood/Downloads/LPs_quadradas/train/labels/new_labels/"
images_path = "/home/santilm/Downloads/LPs_quadradas/transformed/"
labels_path = "/home/santilm/Downloads/LPs_quadradas/train/images/"
new_images_path = "/home/santilm/Downloads/LPs_quadradas/train/images/"
new_labels_path = "/home/santilm/Downloads/LPs_quadradas/train/labels/"
newer_images_path = "/home/santilm/Downloads/LPs_quadradas/train/images/new_images/"
newer_labels_path = "/home/santilm/Downloads/LPs_quadradas/train/labels/new_labels/"

create_new_images(images_path, new_images_path, new_labels_path)

image_files = [f for f in os.listdir(new_images_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
transformations = 5 # Number of transformations that each image is subjected to
n = 0
# Loop through each image file
for image_file in image_files:
    image_path = os.path.join(new_images_path, image_file)

    # Read the image
    image = cv2.imread(image_path)
    for i in range(transformations):
    
        image = transforms(image)
        new_image_name = f"{i}_" + image_file
        cv2.imwrite(os.path.join(newer_images_path, new_image_name), image)
        new_txt_filename = os.path.join(newer_labels_path, f"{i}_" + os.path.splitext(image_file)[0] + '.txt')
        old_txt_filename = os.path.join(new_labels_path, os.path.splitext(image_file)[0] + '.txt')

        shutil.copy2(old_txt_filename, new_txt_filename)
        n += 1
