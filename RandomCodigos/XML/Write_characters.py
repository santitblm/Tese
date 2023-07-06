import os
import cv2
import xml.etree.ElementTree as ET

# Path to the XML file
xml_file = "C:\\Users\\Vastingood\\Documents\\GitHub\\Tese\\RandomCodigos\\XML\\annotations.xml"

# Path to the images folder
images_folder = "C:/Users/Vastingood/Documents/GitHub/Tese/cropped/"

# Load the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

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

        # Display the image
        cv2.imshow('Image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Prompt the user to input 6 characters
        user_input = input("Enter 6 characters: ")

        # Update each polygon label with the user input
        for polygon in image.findall('polygon'):
            polygon.set('label', user_input[0])
            user_input = user_input[1:]  # Move to the next character

        # Save the updated XML file
        tree.write(xml_file)

        print("Labels updated for image", image_id)
