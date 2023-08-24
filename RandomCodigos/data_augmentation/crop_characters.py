import os
import cv2
import xml.etree.ElementTree as ET
import numpy as np

username = "Santi LM"
#username = "Vastingood"

# Path to the XML file
xml_file = "C:/Users/" + username + "/Documents/GitHub/Tese/RandomCodigos/data_augmentation/annotations.xml"

# Path to the images folder
images_folder = "C:/Users/" + username + "/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images"

# Path to the folder to save transformed images
output_folder = "C:/Users/" + username + "/Documents/GitHub/Tese/RandomCodigos/data_augmentation/Labels/"

# Load the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# Iterate over each image element
for image in root.findall('image'):
    image_id = image.get('id')
    image_name = "transformed_" + image.get('name')

    # Get all polygons except 'LP'
    polygons = image.findall("polygon[@label!='LP']")

    i = 0
    for polygon in polygons:
        i += 1
        label = polygon.get('label')
        points_str = polygon.get('points').split(';')
        points = np.array([list(map(float, point.split(','))) for point in points_str], dtype=np.float32)
    
        # Calculate crop boundaries
        min_x = int(np.min(points[:, 0]))
        max_x = int(np.max(points[:, 0]))
        min_y = int(np.min(points[:, 1]))
        max_y = int(np.max(points[:, 1]))
        
        # Load the image
        image_path = os.path.join(images_folder, image_name)
        img = cv2.imread(image_path)
        if img is not None:
            # Crop the transformed image
            cropped_img = img[min_y:max_y, min_x:max_x]
    
            # Save the cropped image
            output_path = os.path.join(output_folder, label, f"cropped_{image_name}_{i}.jpg")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            cv2.imwrite(output_path, cropped_img)
