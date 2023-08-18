import os
import numpy as np
import cv2
import xml.etree.ElementTree as ET
import random

# Define paths
username = "Santi LM"
xml_file = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/annotations.xml"
images_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/"
templates_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/templates/"
positions_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/templates/positions/"
synthetic_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/synthetic/"

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
# Initialize a counter for the synthetic image filenames
synthetic_image_counter = 0

# ... (previous code)

# Number of synthetic images to generate
num_synthetic_images = 100

# Iterate over each synthetic image
for synthetic_image_counter in range(num_synthetic_images):
    # Choose a random template image
    template_image_name = random.choice(template_images)
    template_image_path = os.path.join(templates_folder, template_image_name)
    template = cv2.imread(template_image_path)

    # Get the base name of the template image without the extension
    template_base_name = os.path.splitext(template_image_name)[0]

    # Create a copy of the template to work on
    synthetic_image = template.copy()
    
    # Choose and extract 6 random polygons from different images
    random_polygons = []
    while len(random_polygons) < 6:
        # Choose a random image element
        random_image = random.choice(image_elements)
        polygons = random_image.findall("polygon[@label!='LP']")
        if len(polygons) > 0:
            random_polygon = random.choice(polygons)
            random_polygons.append(random_polygon)
    
    # Randomize the positions chosen for the polygons
    order = [0, 1, 2, 3, 4, 5]
    random.shuffle(order)
    
    # Loop through the polygons and draw them onto the synthetic image
    for i, polygon in enumerate(random_polygons):
        points_str = polygon.get('points').split(';')
        points = np.array([list(map(float, point.split(','))) for point in points_str], dtype=np.float32)

        # Calculate the bounding box of the polygon
        min_x = int(np.min(points[:, 0]))
        max_x = int(np.max(points[:, 0]))
        min_y = int(np.min(points[:, 1]))
        max_y = int(np.max(points[:, 1]))

        # Choose a random position from a position file
        position_file_path = os.path.join(positions_folder, f"{template_base_name}.txt")
        with open(position_file_path, 'r') as f:
            positions = [list(map(float, line.strip().split())) for line in f.readlines()]
        random_position = positions[order[i]]

        # Extract the ROI from the original image
        random_image_name = random_image.get('name')
        roi = cv2.imread(os.path.join(images_folder, "transformed_" + random_image_name))
        roi = roi[min_y:max_y, min_x:max_x]

        # Resize the ROI to match the size of the polygon in the template
        polygon_width = max_x - min_x
        polygon_height = max_y - min_y
        roi = cv2.resize(roi, (polygon_width, polygon_height))

        # Calculate position on the template
        x = int(random_position[0]*template.shape[1] + (min_x - int(np.min(points[:, 0]))))
        y = int(random_position[1]*template.shape[0] + (min_y - int(np.min(points[:, 1]))))
        
        # Paste the resized ROI onto the template
        synthetic_image[int(y-polygon_height/2):int(y+polygon_height/2), int(x-polygon_width/2):int(x+polygon_width/2)] = roi

    # Save the synthetic image with a unique filename
    synthetic_image_path = os.path.join(synthetic_folder, f"synthetic_{template_base_name}_{synthetic_image_counter}.jpg")
    cv2.imwrite(synthetic_image_path, synthetic_image)
