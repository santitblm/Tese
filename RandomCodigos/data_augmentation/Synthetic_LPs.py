import os
import numpy as np
import cv2
import xml.etree.ElementTree as ET
import random
import math
from tqdm import tqdm
from image_transformations import apply_random_transformations
from txt_processor import save_txt_file

# Define paths
username = "Santi LM"
xml_file = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/filtered_annotations.xml"
images_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/"#bright_redux/"
templates_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/templates/"
positions_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/templates/positions/"
synthetic_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/synthetic/"
txt_path = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/synthetic/labels/"
#binary_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/binary_otsu"

# Set the random seed for reproducibility
random_seed = 477  # You can use any integer value you prefer
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
#progress_bar = tqdm(total=num_synthetic_images, desc=f"Creating {num_synthetic_images} synthetic images. Progress:")

# Iterate over each synthetic image
for synthetic_image_counter in range(num_synthetic_images):
    # Choose a random template image
    template_image_name = random.choice(template_images)
    print(template_image_name)
    template_image_path = os.path.join(templates_folder, template_image_name)
    template = cv2.imread(template_image_path)

    # Initialize the name of the synthetic image and the array to save the id and label
    name_to_save = ""
    labels_used = []
    # Get the positions from the positions' file
    template_base_name = os.path.splitext(template_image_name)[0]
    position_file_path = os.path.join(positions_folder, f"{template_base_name}.txt")
    with open(position_file_path, 'r') as f:
        positions = [list(map(float, line.strip().split())) for line in f.readlines()]

    # Create a copy of the template to work on
    synthetic_image = template.copy()
    synthetic_image = cv2.convertScaleAbs(synthetic_image, alpha=1, beta=random.randint(-20, 0))

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

            if len(polygons) > 0 and os.path.exists(os.path.join(images_folder, random_image_name)):# and int(random_image.get('id')) > 3848:
                random_polygon = random.choice(polygons)
                if random_polygon.get('occluded') == "0":
                    
                    successful = True
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

                    points_extremos = np.array([[min_x, min_y], [max_x, min_y], [max_x, max_y], [min_x, max_y]])
                    # Extract the roi from the original image using the polygon's points
                    original_image = cv2.imread(os.path.join(images_folder, random_image_name))
                    # Create a mask for the polygon area
                    polygon_mask = np.zeros(original_image.shape[:2], dtype=np.uint8)
                    cv2.fillPoly(polygon_mask, [points_extremos.astype(int)], (255))

                    # Create a mask for the polygon area
                    polygon_mask = np.zeros(original_image.shape[:2], dtype=np.uint8)
                    cv2.fillPoly(polygon_mask, [points_extremos.astype(int)], (255))
                    # Calculate position on the template
                    x = int(random_position[0] * template.shape[1])
                    y = int(random_position[1] * template.shape[0])

                    # Calculate the original_image's dimensions
                    h, w = original_image.shape[:2]
                    
                    synthetic_image = cv2.seamlessClone(original_image, synthetic_image, polygon_mask, (x, y), cv2.MIXED_CLONE)
                    
                    # Join the id and label to the array
                    image_id = random_image.get('id')
                    polygon_label = random_polygon.get('label')
                    name_to_save += image_id + "_" + polygon_label + "___"
                    labels_used.append([polygon_label, points, (x, y)])
                    

    #progress_bar.update(1)
                
    # Save the synthetic image with a unique filename
    final_image, homography_matrix = apply_random_transformations(synthetic_image)
    synthetic_image_path = os.path.join(synthetic_folder, f"{name_to_save}.jpg")
    cv2.imwrite(synthetic_image_path, final_image)
    print(f"Image {name_to_save} saved successfully.")
    
    # Save the modified polygons' bounding boxes to a txt file
    save_txt_file(name_to_save, txt_path, labels_used, homography_matrix)

