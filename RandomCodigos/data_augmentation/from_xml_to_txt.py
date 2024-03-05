import os
import xml.etree.ElementTree as ET
import numpy as np
import cv2

#username = "Santi LM"
#xml_file = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/XML/annotations.xml"
#images_folder = f"C:/Users/{username}/Documents/GitHub/Tese/cropped/"
#txt_path = f"C:/Users/{username}/Documents/GitHub/Tese/cropped/labels/"

username = "Vastingood"
xml_file = f"C:/Users/{username}/Downloads/LPs_quadradas/annotations.xml"
images_folder = f"C:/Users/{username}/Downloads/LPs_quadradas/images/"
txt_path = f"C:/Users/{username}//Downloads/LPs_quadradas/obj_train_data/"

# Load the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

for image in root.findall('image'):
    image_name = image.get('name')

    # Get the LP polygon points
    polygons = image.findall("polygon[@label!='LP']")
    name_to_save = image_name.split('.')[0]
    if polygons is not None and os.path.exists(os.path.join(images_folder, image_name)): 
        img_shape = cv2.imread(os.path.join(images_folder, image_name)).shape
        with open(os.path.join(txt_path, f"{name_to_save}.txt"), "w") as f:
            for polygon in polygons:
                points_str = polygon.get('points').split(';')
                points = np.array([list(map(float, point.split(','))) for point in points_str], dtype=np.float32)
                label = polygon.get('label')
                # Calculate the min and max of the points
                min_x = int(np.min(points[:, 0]))
                max_x = int(np.max(points[:, 0]))
                min_y = int(np.min(points[:, 1]))
                max_y = int(np.max(points[:, 1]))

                center_x = (min_x + max_x) / 2
                center_y = (min_y + max_y) / 2
                
                # Get the position of the polygon_label in the key
                #key = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"
                if label == "LP_Quadrada":
                    position = 1
                elif label == "License_Plate":
                    position = 0
                else:
                    raise "Error"
                
                # Write the line to the file
                line = f"{position} {center_x/img_shape[1]} {center_y/img_shape[0]} {max_x/img_shape[1] - min_x/img_shape[1]} {max_y/img_shape[0] - min_y/img_shape[0]}\n"
                f.write(line)