import os
import numpy as np
import cv2
import xml.etree.ElementTree as ET
import random
from tqdm import tqdm
from image_transformations import apply_random_transformations
from txt_processor import save_txt_file
from label_count import get_label_counts
from choose_label import choose_label

# Define paths
username = "Santi LM"
xml_file = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/filtered_annotations.xml"
images_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/"#bright_redux/"
templates_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/templates/"
positions_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/templates/positions/"
synthetic_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/synthetic/images"
txt_path = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/synthetic/labels/"
#binary_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/transformed_images/binary_otsu"

# Set the random seed for reproducibility
random_seed = 64  # You can use any integer value you prefer
random.seed(random_seed)
np.random.seed(random_seed)

# Load the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

global_array, label_image_ids = get_label_counts(root)

# List all available template images
template_images = [file for file in os.listdir(templates_folder) if file.lower().endswith(('.png', '.jpg', '.jpeg'))]

# List all available images for polygon extraction
image_elements = root.findall('image')

# Number of synthetic images to generate
num_synthetic_images = 50000
progress_bar = tqdm(total=num_synthetic_images, desc=f"Creating {num_synthetic_images} synthetic images. Progress:")

#ids_not_found = []

# Iterate over each synthetic image
for synthetic_image_counter in range(num_synthetic_images):
    # Choose a random template image
    template_image_name = random.choice(template_images)
    template_image_path = os.path.join(templates_folder, template_image_name)
    template = cv2.imread(template_image_path)

    # Initialize the name of the synthetic image and the array to save the id and label
    #name_to_save = ""
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
            # Choose a random label based on the frequency of each label (less frequent labels are more likely to be chosen)
            label, global_array = choose_label(int(num_synthetic_images/34), global_array)
            id = random.choice(label_image_ids[label])  # Choose a random image that contains the chosen label
            # Find the image element with the chosen id
            for image_element in image_elements:
                image_id = image_element.get("id")
                if image_id == id:
                    image = image_element
                    break

            # Find the polygon element with the chosen label (if there are more than one with the same label, choose one at random)
            polygons = image.findall(f"polygon[@label='{label}']")
            polygon = random.choice(polygons)
                #print(f"More than one polygon with the same label in image {image_id}")

            # Load the image, check if it exists and if the polygon is not occluded
            image_name = "transformed_" + image.get('name')
            original_image = cv2.imread(os.path.join(images_folder, image_name))
            if polygon.get('occluded') == "0" and original_image is not None:
                successful = True

                points_str = polygon.get('points').split(';')
                points = np.array([list(map(float, point.split(','))) for point in points_str], dtype=np.float32)

                # Calculate the bounding box of the polygon
                min_x = int(np.min(points[:, 0]))
                max_x = int(np.max(points[:, 0]))
                min_y = int(np.min(points[:, 1]))
                max_y = int(np.max(points[:, 1]))

                points_extremos = np.array([[min_x, min_y], [max_x, min_y], [max_x, max_y], [min_x, max_y]])

                # Create a mask for the polygon area
                polygon_mask = np.zeros(original_image.shape[:2], dtype=np.uint8)
                cv2.fillPoly(polygon_mask, [points_extremos.astype(int)], (255))

                # Choose a random position from a position file and calculate the position on the template
                random_position = positions[i]
                x = int(random_position[0] * template.shape[1]) + random.randint(-2, 2)
                y = int(random_position[1] * template.shape[0]) + random.randint(-2, 2)

                # "seamlessly" paste the character onto the template
                synthetic_image = cv2.seamlessClone(original_image, synthetic_image, polygon_mask, (x, y), cv2.MIXED_CLONE)

                # Join the label, points and position to the array
                labels_used.append([label, points, (x, y)])

            #elif original_image is None:
            #    ids_not_found.append(id)



    progress_bar.update(1)
    name_to_save = synthetic_image_counter  # This variable only exists to make it easier if we want to use a different naming convention            
    # Save the synthetic image with a unique filename
    final_image, homography_matrix = apply_random_transformations(synthetic_image)
    synthetic_image_path = os.path.join(synthetic_folder, f"{name_to_save}.jpg")
    cv2.imwrite(synthetic_image_path, final_image)

    # Save the modified polygons' bounding boxes to a txt file
    save_txt_file(name_to_save, txt_path, labels_used, homography_matrix, final_image.shape)

# Close the progress bar and show not found images without duplicates
progress_bar.close()
#print("\n IDs not found:")
#print(set(ids_not_found))
