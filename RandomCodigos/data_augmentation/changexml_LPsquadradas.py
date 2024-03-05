import os
import xml.etree.ElementTree as ET
import numpy as np
import cv2

#username = "Santi LM"
#xml_file = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/XML/annotations.xml"
#images_folder = f"C:/Users/{username}/Documents/GitHub/Tese/cropped/"
#txt_path = f"C:/Users/{username}/Documents/GitHub/Tese/cropped/labels/"

username = "Vastingood"
xml_file = f"C:/Users/{username}/Downloads/LPs_quadradas/annotations_cropped.xml"

# Load the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

for image in root.findall('image'):
    image_id = image.get('id')
    image_name = image.get('name')

    # Get the LP polygon points
    polygons = image.findall("polygon[@label='LP_Quadrada']")
    name_to_save = image_name.split('.')[0]

    for polygon in polygons:
        points_str = polygon.get('points').split(';')
        points = np.array([list(map(float, point.split(','))) for point in points_str], dtype=np.float32)
        label = polygon.get('label')

        # Calculate the min and max of the points
        min_x = np.min(points[:, 0])
        max_x = np.max(points[:, 0])
        min_y = np.min(points[:, 1])
        max_y = np.max(points[:, 1])

        points[:, 0] = points[:, 0] - min_x
        points[:, 1] = points[:, 1] - min_y
        print(points)
        new_points_str = ';'.join([f"{point[0]},{point[1]}" for point in points])
        print(new_points_str)
        polygon.set('points', new_points_str)

    tree.write(xml_file)

    print("Transformed points saved for image", image_id)
