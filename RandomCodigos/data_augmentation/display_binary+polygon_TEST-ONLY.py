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
    image_name = image.get('name')

    # Load the normal image
    image_path = os.path.join(images_folder, image_name)
    img = cv2.imread(image_path)

    # Load the corresponding binary image
    binary_image_path = os.path.join(binary_images_folder, image_name)
    binary_img = cv2.imread(binary_image_path, cv2.IMREAD_GRAYSCALE)

    # Create a mask where the binary image is black
    mask = (binary_img == 0)

    # Iterate over each polygon except 'LP'
    polygons = image.findall("polygon[@label!='LP']")
    for polygon in polygons:
        points_str = polygon.get('points').split(';')
        points = np.array([list(map(float, point.split(','))) for point in points_str], dtype=np.int32)

        # Fill the polygon in the mask with white color
        cv2.fillPoly(mask, [points], 255)

    # Apply the mask to the normal image
    result_img = cv2.bitwise_and(img, img, mask=mask)

    # Set non-masked pixels to white
    result_img[~mask] = [255, 255, 255]

    # Display the resulting image
    cv2.imshow("Resulting Image", result_img)
    cv2.waitKey(0)

cv2.destroyAllWindows()
