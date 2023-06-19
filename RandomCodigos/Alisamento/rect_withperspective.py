import cv2
import numpy as np
import os

def draw_license_plate_edges(image):
    # Step 1: Convert image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Step 2: Apply edge detection
    edges = cv2.Canny(gray, 100, 200)
    kernel = np.ones((3, 3), np.uint8)  # Adjust the kernel size as needed

    # Dilate the binary image
    edges = cv2.dilate(edges, kernel, iterations=1)
    
    # Step 3: Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Step 4: Find the contour with the largest area
    max_area = 0
    max_area_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_area:
            max_area = area
            max_area_contour = contour

    # Step 5: Apply perspective transform
    if max_area_contour is not None:
        epsilon = 0.1 * cv2.arcLength(max_area_contour, True)
        approx = cv2.approxPolyDP(max_area_contour, epsilon, True)

        # Create a rectangular bounding box around the contour
        rect = cv2.minAreaRect(approx)
        box = cv2.boxPoints(rect)
        box = np.int0(box)

        # Perform perspective transform
        width = rect[1][0]
        height = rect[1][1]
        src_pts = box.astype("float32")
        dst_pts = np.array([[0, height-1],
                            [0, 0],
                            [width-1, 0],
                            [width-1, height-1]], dtype="float32")
        matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
        warped = cv2.warpPerspective(image, matrix, (int(width), int(height)))

        # Draw the warped image with the rectangle
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
