import os
import numpy as np
import cv2
import xml.etree.ElementTree as ET
import random

# Define paths
username = "Vastingood"
xml_file = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/annotations.xml"
images_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/"
templates_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/templates/"
positions_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/templates/positions/"
synthetic_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/synthetic/"

# Load the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# List all available template images
template_images = [file for file in os.listdir(templates_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

# List all available images for polygon extraction
image_elements = root.findall('image')
# Initialize a counter for the synthetic image filenames
synthetic_image_counter = 1

# Iterate over each image element
for image in image_elements:
    polygons = image.findall('polygon')
    if len(polygons) >= 6:
        # Choose a random template image
        template_image_name = random.choice(template_images)
        template_image_path = os.path.join(templates_folder, template_image_name)
        template = cv2.imread(template_image_path)

        # Get the base name of the template image without the extension
        template_base_name = os.path.splitext(template_image_name)[0]

        # Choose a random position from a position file
        position_file_path = os.path.join(positions_folder, f"{template_base_name}.txt")
        with open(position_file_path, 'r') as f:
            positions = [list(map(float, line.strip().split())) for line in f.readlines()]
        random_position = random.choice(positions)

        # Create a copy of the template to work on
        synthetic_image = template.copy()

        # Choose and extract 6 random polygons
        random_polygons = random.sample(polygons, 6)
        for polygon in random_polygons:
            points_str = polygon.get('points').split(';')
            points = np.array([list(map(float, point.split(','))) for point in points_str], dtype=np.float32)

            # Calculate polygon center
            polygon_center = np.mean(points, axis=0)

            # Calculate position on the template
            x = int(random_position[0] + polygon_center[0])
            y = int(random_position[1] + polygon_center[1])

            # Draw the polygon on the synthetic image
            cv2.polylines(synthetic_image, [points.astype(int)], isClosed=True, color=(0, 255, 0), thickness=2)

        # Save the synthetic image with a unique filename
        synthetic_image_path = os.path.join(synthetic_folder, f"synthetic_{template_base_name}_{synthetic_image_counter}.jpg")
        cv2.imwrite(synthetic_image_path, synthetic_image)

        # Increment the counter for the next image
        synthetic_image_counter += 1
