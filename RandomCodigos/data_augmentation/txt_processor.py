import os
import cv2
import numpy as np

def save_txt_file(name_to_save, txt_path, labels_used, homography_matrix):
    with open(os.path.join(txt_path, f"{name_to_save}.txt"), "w") as f:
        for label, points, (x, y) in labels_used:

            # Calculate the min and max of the points
            min_x = int(np.min(points[:, 0]))
            max_x = int(np.max(points[:, 0]))
            min_y = int(np.min(points[:, 1]))
            max_y = int(np.max(points[:, 1]))

            # Translate the points to the center of the bounding box
            print(points, x, y)
            points[:, 0] += x - (min_x+max_x)/2
            points[:, 1] += y - (min_y+max_y)/2
            print(points)
            # Apply the homography matrix to the points
            transformed_points = cv2.perspectiveTransform(points.reshape(-1, 1, 2), homography_matrix).reshape(-1, 2)
            
            # Calculate the transformed center of the bounding box
            min_x = int(np.min(transformed_points[:, 0]))
            max_x = int(np.max(transformed_points[:, 0]))
            min_y = int(np.min(transformed_points[:, 1]))
            max_y = int(np.max(transformed_points[:, 1]))
            transformed_center_x = (min_x + max_x) / 2
            transformed_center_y = (min_y + max_y) / 2
            
            # Get the position of the polygon_label in the key
            key = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"
            position = key.index(label)
            
            # Write the line to the file
            line = f"{position} {transformed_center_x} {transformed_center_y} {max_x - min_x} {max_y - min_y}\n"
            f.write(line)
