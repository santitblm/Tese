import cv2
import numpy as np

# Load the image
image = cv2.imread('C:/Users/Santi LM/Downloads/cropped/vlcsnap-2023-06-02-10h50m29s408 (3).png')

# Convert the image to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Split the HSV image into channels
h, s, v = cv2.split(hsv)

# Display the HSV channels
cv2.imshow('H Channel', h)
cv2.imshow('S Channel', s)
cv2.imshow('V Channel', v)
cv2.waitKey(0)
cv2.destroyAllWindows()


# Convert the image to grayscale
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Subtract the grayscale image from the original image
subtracted = cv2.subtract(image, cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR))

# Convert the resulting image to grayscale
subtracted_gray = cv2.cvtColor(subtracted, cv2.COLOR_BGR2GRAY)

# Threshold the subtracted image
_, thresholded = cv2.threshold(subtracted_gray, 1, 255, cv2.THRESH_BINARY)

# Invert the thresholded image
inverted = cv2.bitwise_not(thresholded)

# Create a black image
result = np.zeros_like(image)

# Set white pixels in the result image where the original image had black pixels
#result[inverted > 0] = 255

# Display the resulting image
cv2.imshow('Result', subtracted)
cv2.waitKey(0)
cv2.destroyAllWindows()
