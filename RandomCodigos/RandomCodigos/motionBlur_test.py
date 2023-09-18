#https://www.geeksforgeeks.org/opencv-motion-blur-in-python/

# loading library
import cv2
import numpy as np
  
img = cv2.imread('C:/Users/Santi LM/Documents/GitHub/Tese/RandomCodigos/data_augmentation/synthetic/images/99.jpg')
  
# Specify the kernel size.
# The greater the size, the more the motion.
kernel_size = 11
  
# Create the vertical kernel.
kernel_h = np.zeros((kernel_size, kernel_size))
  
# Fill the middle row with ones.
kernel_h[int((kernel_size - 1)/2), :] = np.ones(kernel_size)
  
# Normalize.
kernel_h /= kernel_size

# Apply the horizontal kernel.
horizonal_mb = cv2.filter2D(img, -1, kernel_h)
blurred_image = cv2.blur(img, (kernel_size, kernel_size))
# Save the outputs.
cv2.imshow('car_horizontal.jpg', horizonal_mb)
cv2.imshow('car_blurred.jpg', img)
cv2.waitKey(0)
cv2.destroyAllWindows()