import os
import cv2
import xml.etree.ElementTree as ET
import numpy as np

# Username
username = "Vastingood"

# Path to the XML file
xml_file = "C:/Users/" + username + "/Documents/GitHub/Tese/RandomCodigos/data_augmentation/annotations.xml"

# Path to the normal images folder
images_folder = "C:/Users/" + username + "/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/"

# Path to the binary images folder
binary_images_folder = "C:/Users/" + username + "/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/binary_otsu/"

# Load the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# Iterate over each normal image
for image in root.findall('image'):
    image_id = image.get('id')
    image_name = "transformed_" + image.get('name')

    # Check if the binary image exists
    binary_image_path = os.path.join(binary_images_folder, image_name)
    if os.path.exists(binary_image_path):
        # Load the normal image
        image_path = os.path.join(images_folder, image_name)
        img = cv2.imread(image_path)

        # Load the corresponding binary image
        gray_img = cv2.imread(binary_image_path, cv2.IMREAD_GRAYSCALE)
        _, binary_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # Create a mask where the binary image is black
        mask = (binary_img == 0)

        # Create a mask for polygons
        polygons_mask = np.zeros_like(binary_img)

        # Iterate over each polygon except 'LP'
        polygons = image.findall("polygon[@label!='LP']")
        for polygon in polygons:
            points_str = polygon.get('points').split(';')
            points = np.array([list(map(float, point.split(','))) for point in points_str], dtype=np.int32)

            # Fill the polygon in the mask
            cv2.fillPoly(polygons_mask, [points], 255)

        # Combine the masks
        final_mask = np.logical_and(mask, polygons_mask)

        # Set pixels outside the mask to black
        #result_img = np.zeros_like(img)
        #result_img[final_mask] = img[final_mask]

        # Set pixels outside the mask to white
        result_img = np.copy(img)
        result_img[~final_mask] = [255, 255, 255]

        # Display the resulting image
        cv2.imshow("Resulting Image", result_img)
        cv2.waitKey(0)

cv2.destroyAllWindows()
