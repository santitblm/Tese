import os
import numpy as np
import cv2
import xml.etree.ElementTree as ET
import random
import math

# Define paths
username = "Santi LM"
xml_file = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/annotations.xml"
images_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/"
templates_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/templates/"
positions_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/templates/positions/"
synthetic_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/synthetic/"
binary_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/binary_otsu"

# Set the random seed for reproducibility
random_seed = 42  # You can use any integer value you prefer
random.seed(random_seed)
np.random.seed(random_seed)

# Load the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# List all available template images
template_images = [file for file in os.listdir(templates_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

# List all available images for polygon extraction
image_elements = root.findall('image')

# Number of synthetic images to generate
num_synthetic_images = 10

# Iterate over each synthetic image
for synthetic_image_counter in range(num_synthetic_images):
    # Choose a random template image
    template_image_name = random.choice(template_images)
    template_image_path = os.path.join(templates_folder, template_image_name)
    template = cv2.imread(template_image_path)

    # Get the positions from the positions' file
    template_base_name = os.path.splitext(template_image_name)[0]
    position_file_path = os.path.join(positions_folder, f"{template_base_name}.txt")
    with open(position_file_path, 'r') as f:
        positions = [list(map(float, line.strip().split())) for line in f.readlines()]

    # Create a copy of the template to work on
    synthetic_image = template.copy()
    
    # Randomize the positions chosen for the polygons
    order = [0, 1, 2, 3, 4, 5]
    random.shuffle(order)
    
    # Loop through the polygons and draw them onto the synthetic image
    for i in order:

        successful = False
        while not successful:

            random_image = random.choice(image_elements)
            random_image_name = "transformed_" + random_image.get('name')
            polygons = random_image.findall("polygon[@label!='LP']")

            if len(polygons) > 0 and os.path.exists(os.path.join(images_folder, random_image_name)):
                successful = True

                random_polygon = random.choice(polygons)
                points_str = random_polygon.get('points').split(';')
                points = np.array([list(map(float, point.split(','))) for point in points_str], dtype=np.float32)

                # Calculate the bounding box of the polygon
                min_x = int(np.min(points[:, 0]))
                max_x = int(np.max(points[:, 0]))
                min_y = int(np.min(points[:, 1]))
                max_y = int(np.max(points[:, 1]))
                w = max_x - min_x
                h = max_y - min_y

                # Choose a random position from a position file
                random_position = positions[i]

                # Load the binary image to be considered in the mask
                binary_image_name = os.path.join(binary_folder, random_image_name)
                binary_image = cv2.imread(binary_image_name)

                # Extract the ROI from the original image using the polygon's points
                roi = cv2.imread(os.path.join(images_folder, random_image_name))
                mask = np.zeros(roi.shape, dtype=np.uint8)
                cv2.fillPoly(mask, [points.astype(int)], (255, 255, 255))
                roi = cv2.bitwise_and(roi, mask)
                roi = cv2.bitwise_and(roi, ~binary_image)
                roi = roi[min_y:max_y, min_x:max_x]                

                # Calculate position on the template
                x = int(random_position[0]*template.shape[1])
                y = int(random_position[1]*template.shape[0])

                # Paste the ROI onto the template
                synthetic_image[int(y-h/2):int(y+h/2), int(x-w/2):int(x+w/2)] = roi
                
    # Save the synthetic image with a unique filename
    synthetic_image_path = os.path.join(synthetic_folder, f"{synthetic_image_counter}.jpg")
    cv2.imwrite(synthetic_image_path, synthetic_image)
