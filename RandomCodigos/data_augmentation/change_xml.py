import cv2
import xml.etree.ElementTree as ET
import numpy as np

# Username
username = "Santi LM"

# Path to the XML file
xml_file = "C:/Users/" + username + "/Documents/GitHub/Tese/RandomCodigos/data_augmentation/annotations_for_transformed.xml"

# Path to the folder to save transformed images
output_folder = "C:/Users/" + username + "/Documents/GitHub/Tese/RandomCodigos/data_augmentation/Labels/"

# Load the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# Define your reference points for homography
reference_points = np.array([[10, 110], [10, 10], [475, 10], [475, 110]], dtype=np.float32)

# Iterate over each image element
for image in root.findall('image'):
    image_id = image.get('id')
    image_name = image.get('name')

    # Get the LP polygon points
    lp_polygon = image.find("polygon[@label='LP']")
    if lp_polygon is not None:
        lp_points_str = lp_polygon.get('points').split(';')
        lp_points = np.array([list(map(float, point.split(','))) for point in lp_points_str], dtype=np.float32)

        homography_matrix, _ = cv2.findHomography(lp_points, reference_points)

        # Apply the homography transformation to the XML points
        for polygon in image.findall("polygon[@label!='LP']"):
            points_str = polygon.get('points').split(';')
            points = np.array([list(map(float, point.split(','))) for point in points_str], dtype=np.float32)

            # Apply the homography transformation to polygon points
            transformed_points = cv2.perspectiveTransform(points.reshape(-1, 1, 2), homography_matrix).reshape(-1, 2)

            # Update the XML points
            new_points_str = ';'.join([f"{point[0]},{point[1]}" for point in transformed_points])
            polygon.set('points', new_points_str)

        # Save the updated XML file
        tree.write(xml_file)

        print("Transformed points saved for image", image_id)
