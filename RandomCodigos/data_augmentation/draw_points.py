'''this code is used to draw the points on the transformed images, to check if the transformation is correct'''

import os
import cv2
import xml.etree.ElementTree as ET
import numpy as np

# Username
username = "Vastingood"

# Path to the XML file
xml_file = "C:/Users/" + username + "/Documents/GitHub/Tese/RandomCodigos/data_augmentation/annotations.xml"

# Path to the images folder
images_folder = "C:/Users/" + username + "/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/"

# Load the updated XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# Iterate over each image element
for image in root.findall('image'):
    image_id = image.get('id')
    image_name = image.get('name')

    # Get the polygon points
    polygons = image.findall("polygon[@label!='LP']")

    # Load the transformed image
    transformed_image_path = os.path.join(images_folder, "transformed_" + image_name)
    transformed_img = cv2.imread(transformed_image_path)

    for polygon in polygons:
        points_str = polygon.get('points').split(';')
        points = np.array([list(map(float, point.split(','))) for point in points_str], dtype=np.float32)

        # Draw the points on the image
        for point in points:
            cv2.circle(transformed_img, tuple(point.astype(int)), 2, (0, 255, 0), -1)  # Draw a green circle

    # Display the image with points
    cv2.imshow("Image with Points", transformed_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
