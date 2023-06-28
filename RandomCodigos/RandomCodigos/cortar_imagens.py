# Import packages
import cv2
import numpy as np
import os
path = '/home/santilm/Desktop/Tese/datasets/License_Plates/train/'
path_images = path + 'images/'
path_labels = path + 'labels/'


for image_name in os.listdir(path_images):
    img = cv2.imread(path_images + image_name)
    print(image_name)
    with open(path_labels + image_name.rsplit(".", 1)[0] + ".txt") as annotations:
        lines = annotations.readlines()
    i = 0        
    for l in lines:
        print(i)
        label = l.split(" ")

        Cx = img.shape[1]*float(label[1])
        Cy = img.shape[0]*float(label[2])
        Lx = img.shape[1]*float(label[3])
        Ly = img.shape[0]*float(label[4].replace("\n", ""))
        x1 = round(Cx - Lx/2)
        x2 = round(Cx + Lx/2)
        y1 = round(Cy - Ly/2)
        y2 = round(Cy + Ly/2)
        cropped_image = img[y1:y2, x1:x2]
        cv2.imwrite("datasets/License_Plates/Cropped/" + str(i) + image_name, cropped_image)
        i += 1
