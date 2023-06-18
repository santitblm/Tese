import cv2
import numpy as np
import os

def draw_license_plate_edges(image):
    # Step 1: Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 2: Apply edge detection
    edges = cv2.Canny(gray, 100, 200)
    kernel = np.ones((1, 1), np.uint8)  # Adjust the kernel size as needed

    # Dilate the binary image
    edges = cv2.dilate(edges, kernel, iterations=1)
    cv2.imshow("Result", edges)
    cv2.waitKey(0)    
    # Step 3: Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Step 4: Find the rectangle with the largest area
    max_area = 0
    max_area_rectangle = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_area_rectangle = cv2.minAreaRect(contour)

    # Step 5: Draw lines on the edges of the largest rectangle
    if max_area_rectangle is not None:
        box = cv2.boxPoints(max_area_rectangle)
        box = np.int0(box)
        cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

    return image

# Folder containing the images
folder_path = "C:/Users/Santi LM/Downloads/cropped"


# Iterate over all the images in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".jpeg") or filename.endswith(".jpg") or filename.endswith(".png"):
        # Load the image
        image_path = os.path.join(folder_path, filename)
        image = cv2.imread(image_path)

        # Call the function to draw license plate edges
        result = draw_license_plate_edges(image)

        # Display the result
        cv2.imshow("Result", result)
        cv2.waitKey(0)

# Close all windows
cv2.destroyAllWindows()
