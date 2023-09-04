import os
import cv2
import numpy as np

def save_txt_file(name_to_save, txt_path, labels_used, transformation_matrix, img_shape):
    with open(os.path.join(txt_path, f"{name_to_save}.txt"), "w") as f:
        for label, points, (x, y) in labels_used:
            # Calculate the min and max of the points
            min_x = int(np.min(points[:, 0]))
            max_x = int(np.max(points[:, 0]))
            min_y = int(np.min(points[:, 1]))
            max_y = int(np.max(points[:, 1]))

            # Translate the points to the center of the bounding box
            points[:, 0] += x - (min_x+max_x)/2
            points[:, 1] += y - (min_y+max_y)/2
            # Apply the homography matrix to the points
            transformed_points = apply_perspective_transformation(points, transformation_matrix)
            
            # Calculate the transformed center of the bounding box
            min_x = np.min(transformed_points[:, 0])
            max_x = np.max(transformed_points[:, 0])
            min_y = np.min(transformed_points[:, 1])
            max_y = np.max(transformed_points[:, 1])
            transformed_center_x = (min_x + max_x) / 2
            transformed_center_y = (min_y + max_y) / 2
            
            # Get the position of the polygon_label in the key
            key = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"
            position = key.index(label)
            
            # Write the line to the file
            line = f"{position} {transformed_center_x/img_shape[1]} {transformed_center_y/img_shape[0]} {max_x/img_shape[1] - min_x/img_shape[1]} {max_y/img_shape[0] - min_y/img_shape[0]}\n"
            f.write(line)

def apply_perspective_transformation(points, transformation_matrix):
    # Convert points to homogeneous coordinates
    homogeneous_points = np.hstack((points, np.ones((points.shape[0], 1))))

    # Apply the transformation matrix to the points
    transformed_points = np.dot(homogeneous_points, transformation_matrix.T)

    # Convert back to 2D coordinates
    #transformed_x = transformed_points[:, 0] / transformed_points[:, 2]
    #transformed_y = transformed_points[:, 1] / transformed_points[:, 2]

    #transformed_points_2d = np.column_stack((transformed_x, transformed_y))
    return transformed_points