import os
import cv2
import xml.etree.ElementTree as ET

# Path to the XML file
xml_file = "C:/Users/Santi LM/Documents/GitHub/Tese/RandomCodigos/XML/annotations.xml"

# Path to the images folder
images_folder = "C:/Users/Santi LM/Documents/GitHub/Tese/cropped/"

# Load the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# Keep track of previous input
previous_input = ""

# Iterate over each image element
for image in root.findall('image'):
    image_id = image.get('id')
    image_name = image.get('name')

    # Check if the image has exactly 4 OR 6 polygons with label 'A'
    polygons_with_label_a = image.findall("polygon[@label='A']")
    if len(polygons_with_label_a) >= 4 and len(image.findall('polygon')) == 6:
        # Open the image using OpenCV
        image_path = os.path.join(images_folder, image_name)
        img = cv2.imread(image_path)

        # Sort the polygons based on the x-coordinate of their first point
        sorted_polygons = sorted(polygons_with_label_a, key=lambda polygon: float(polygon.get('points').split(';')[0].split(',')[0]))

        # Display the image
        cv2.imshow('Image', img)
        cv2.waitKey(1)

        # Prompt the user to input characters
        user_input = input("Enter characters: ")

        if user_input == 'S':
            user_input = previous_input
        else:
            previous_input = user_input

        cv2.destroyAllWindows()
        # Update the labels based on the order of the polygons
        for polygon, char in zip(sorted_polygons, user_input):
            polygon.set('label', char)

        # Save the updated XML file
        tree.write(xml_file)

        print("Labels updated for image", image_id)
