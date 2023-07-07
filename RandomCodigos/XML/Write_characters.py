import os
import cv2
import xml.etree.ElementTree as ET

# Path to the XML file
#xml_file = "C:/Users/Vastingood/Documents/GitHub/Tese/RandomCodigos/XML/annotations.xml"
xml_file = "C:/Users/Santi LM/Documents/GitHub/Tese/RandomCodigos/XML/annotations.xml"

# Path to the images folder
#images_folder = "C:/Users/Vastingood/Documents/GitHub/Tese/cropped/"
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

    # Check if all polygons have label 'A'
    all_a_labels = all(polygon.get('label') == 'A' for polygon in image.findall('polygon'))

    if all_a_labels:
        # Open the image using OpenCV
        image_path = os.path.join(images_folder, image_name)
        img = cv2.imread(image_path)

        # Get the polygons with label 'A'
        polygons = [polygon for polygon in image.findall('polygon') if polygon.get('label') == 'A']

        # Sort the polygons based on the x-coordinate of their first point
        sorted_polygons = sorted(polygons, key=lambda polygon: float(polygon.get('points').split(';')[0].split(',')[0]))

        # Display the image
        cv2.imshow('Image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Prompt the user to input characters
        user_input = input("Enter characters: ")

        # Update the labels based on the order of the polygons
        for polygon, char in zip(sorted_polygons, user_input):
            if char == 'S':
                # Use previous input if 'S' is entered
                char = previous_input
            else:
                # Update previous input
                previous_input = char

            polygon.set('label', char)

        # Save the updated XML file
        tree.write(xml_file)

        print("Labels updated for image", image_id)
