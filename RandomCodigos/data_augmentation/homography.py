import os
import cv2
import xml.etree.ElementTree as ET
import numpy as np

#username = "Santi LM"
username = "Vastingood"

# Path to the XML file
xml_file = "C:/Users/" + username + "/Documents/GitHub/Tese/RandomCodigos/XML/annotations.xml"

# Path to the images folder
images_folder = "C:/Users/" + username + "/Documents/GitHub/Tese/cropped/"

# Path to the folder to save transformed images
output_folder = "C:/Users/" + username + "/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/"

# Define your reference points for homography
reference_points = np.array([[20, 120], [20, 20], [485, 20], [485, 120]], dtype=np.float32)

# Load the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# Iterate over each image element
for image in root.findall('image'):
    image_id = image.get('id')
    image_name = image.get('name')

    # Get the LP polygon points
    lp_polygon = image.find("polygon[@label='LP']")
    if lp_polygon is not None:
        lp_points_str = lp_polygon.get('points').split(';')
        lp_points = np.array([list(map(float, point.split(','))) for point in lp_points_str], dtype=np.float32)

        # Load the image
        image_path = os.path.join(images_folder, image_name)
        img = cv2.imread(image_path)

        # Draw the LP polygon on the image
        #for i in range(len(lp_points)):
        #    pt1 = (int(lp_points[i][0]), int(lp_points[i][1]))
        #    pt2 = (int(lp_points[(i+1)%4][0]), int(lp_points[(i+1)%4][1]))
        #    cv2.line(img, pt1, pt2, (0, 255, 0), 1)


        # Calculate homography matrix
        homography_matrix, _ = cv2.findHomography(lp_points, reference_points)

        # Apply the homography transformation
        transformed_img = cv2.warpPerspective(img, homography_matrix, (500, 140))

        # Save the transformed image
        output_path = os.path.join(output_folder, f"transformed_{image_name}")
        cv2.imwrite(output_path, transformed_img)

        print("Transformed image saved for image", image_id)
