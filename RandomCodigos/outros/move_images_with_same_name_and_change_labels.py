import os
import random
import shutil

# Set the value of r (0 <= r <= 1)
def separate():
    n = 265
    for i in range(n):
        # Move the image file
        src_image_path = "/home/santilm/Desktop/paramudar/" + f"{i}.jpg"
        dst_image_path = "/home/santilm/Desktop/LPs_fromCars/train/images/" + f"Q{i}.jpg"
        shutil.move(src_image_path, dst_image_path)

        # Move the corresponding label file
        src_label_path = "/home/santilm/Desktop/paramudar/labels/" + f"{i}.txt"
        dst_label_path = "/home/santilm/Desktop/LPs_fromCars/train/labels/" + f"Q{i}.txt"
        shutil.move(src_label_path, dst_label_path)


separate()
