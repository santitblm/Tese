import os
import cv2
import xml.etree.ElementTree as ET
import numpy as np

#username = "Santi LM"
username = "Vastingood"

# Path to the XML file
xml_file = "C:/Users/" + username + "/Documents/GitHub/Tese/RandomCodigos/XML/annotations.xml"

# Path to the images folder
images_folder = "C:/Users/" + username + "/Documents/GitHub/Tese/cropped/"

# Path to the folder to save transformed images
output_folder = "C:/Users/" + username + "/Documents/GitHub/Tese/RandomCodigos/data_augmentation/Labels/"

# Load the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# Define your reference points for homography
reference_points = np.array([[20, 120], [20, 20], [485, 20], [485, 120]], dtype=np.float32)


# Iterate over each image element
for image in root.findall('image'):
    image_id = image.get('id')
    image_name = image.get('name')

    # Get the LP polygon points
    lp_polygon = image.find("polygon[@label='LP']")
    if lp_polygon is not None:
        lp_points_str = lp_polygon.get('points').split(';')
        lp_points = np.array([list(map(float, point.split(','))) for point in lp_points_str], dtype=np.float32)

        # Load the image
        image_path = os.path.join(images_folder, image_name)
        img = cv2.imread(image_path)

        # Calculate homography matrix
        homography_matrix, _ = cv2.findHomography(lp_points, reference_points)

        # Apply the homography transformation
        transformed_img = cv2.warpPerspective(img, homography_matrix, (500, 140))


        

        # Get all polygons except 'LP'
        polygons = image.findall("polygon[@label!='LP']")
        i = 0
        for polygon in polygons:
            i += 1
            label = polygon.get('label')
            points_str = polygon.get('points').split(';')
            points = np.array([list(map(float, point.split(','))) for point in points_str], dtype=np.float32)

            # Apply the homography transformation to polygon points
            transformed_points = cv2.perspectiveTransform(points.reshape(-1, 1, 2), homography_matrix).reshape(-1, 2)
            
            # Adjust the transformed points to the new image size
            transformed_points[:, 0] *= transformed_img.shape[1] / img.shape[1]
            transformed_points[:, 1] *= transformed_img.shape[0] / img.shape[0]

            for point in transformed_points:
                cv2.circle(transformed_img, tuple(point.astype(int)), 2, (0, 255, 0), -1)  # Draw a green circle
            cv2.imshow("Transformed Image", transformed_img)
            cv2.waitKey(0)
            
            # Calculate crop boundaries
            min_x = int(np.min(transformed_points[:, 0]))
            max_x = int(np.max(transformed_points[:, 0]))
            min_y = int(np.min(transformed_points[:, 1]))
            max_y = int(np.max(transformed_points[:, 1]))
            
            print("Label:", label)
            print("Transformed Points:", transformed_points)
            print("Crop Coordinates:", min_x, max_x, min_y, max_y)
            
            if min_x < max_x and min_y < max_y:
                # Crop the transformed image
                cropped_img = transformed_img[min_y:max_y, min_x:max_x]
                
                # Save the cropped image
                output_path = os.path.join(output_folder, label, f"cropped_{image_name}_{i}.jpg")
                os.makedirs(os.path.dirname(output_path), exist_ok=True)
                cv2.imwrite(output_path, cropped_img)
                print("Cropped image saved for label", label, "in image", image_id)
            else:
                print("Invalid cropping coordinates. Skipping label", label, "in image", image_id)
