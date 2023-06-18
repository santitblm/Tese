import cv2
import os
import numpy as np

input_folder = "C:/Users/Santi LM/Downloads/cropped"
output_folder = "C:/Users/Santi LM/Downloads/rotated"

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

for image_file in os.listdir(input_folder):
    # Load the cropped license plate image
    print(image_file)
    image_path = os.path.join(input_folder, image_file)
    img = cv2.imread(image_path)

    # Apply blur to the image
    blurred_img = cv2.GaussianBlur(img, (9, 9), 0)

    # Convert to grayscale
    gray = cv2.cvtColor(blurred_img, cv2.COLOR_BGR2GRAY)

    # Perform edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours by area and keep the largest one
    
    #contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

    # Draw contours on the original image
    i = 0

########################################################################################################################

    for i in range(len(contours)):
        print(i)
        cv2.drawContours(img, contours[i], -1, (0, 255, 0), 1)
        cv2.imshow("Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
  
########################################################################################################################

#    for contour in contours:
#        print(i)
#        cv2.drawContours(img, contour, -1, (0, 255, 0), 1)
#        cv2.imshow("Image", img)
#        cv2.waitKey(0)
#        cv2.destroyAllWindows()
#        i += 1

    for contour in contours:
        # Approximate the contour's shape to get the plate's corners
        epsilon = 0.05 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)

        if len(approx) == 4:
            # Define target coordinates for warped plate
            target_coords = np.array([[0, 100], [300, 100], [300, 0], [0, 0]], dtype=np.float32)

            # Calculate homography matrix
            transform_matrix, _ = cv2.findHomography(approx.astype(np.float32), target_coords)

            # Warp the plate image using homography
            warped_plate = cv2.warpPerspective(img, transform_matrix, (300, 100))

            # Save the corrected plate image
            output_path = os.path.join(output_folder, f"corrected_{image_file}")
            cv2.imwrite(output_path, warped_plate)
