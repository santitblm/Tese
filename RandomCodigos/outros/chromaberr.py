import cv2
import numpy as np

def apply_chromatic_aberration(image, max_shift=10):
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

# Example usage:
input_image = cv2.imread('C:/Users/Santi LM/Downloads/WhatsApp Image 2023-12-16 at 13.54.07 (1).jpeg')
result_image = apply_chromatic_aberration(input_image, max_shift=20)

# Display the original and result images
cv2.imshow('Original Image', input_image)
cv2.imshow('Chromatic Aberration Simulation', result_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
