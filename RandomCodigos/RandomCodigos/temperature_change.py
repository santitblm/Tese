import cv2
import numpy as np

# Load the image
image = cv2.imread('C:/Users/Vastingood/Documents/GitHub/Tese/RandomCodigos/RandomCodigos/input_image.jpg')

# Define the temperature adjustment factor (positive for warmer, negative for cooler)
temperature_factor = -0.2  # You can adjust this value as needed

# Increase the blue channel (for warmth) and decrease the blue channel (for coolness)
blue_channel = np.clip(image[:, :, 0] * (1 + temperature_factor), 0, 255).astype(np.uint8)
red_channel = np.clip(image[:, :, 2] * (1 - temperature_factor), 0, 255).astype(np.uint8)

# Create the output image with adjusted channels
adjusted_image = image.copy()
adjusted_image[:, :, 0] = blue_channel
adjusted_image[:, :, 2] = red_channel

# Display the original and adjusted images
cv2.imshow('Original Image', image)
cv2.imshow('Adjusted Image (Warmer)', adjusted_image)

# Wait for a key press and then close the windows
cv2.waitKey(0)
cv2.destroyAllWindows()