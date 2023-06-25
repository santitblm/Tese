"""
Script to remove images without objects from the validation set.
"""

import os
import cv2

TXT_ROOT = os.path.join('valid', 'labels')
IMG_ROOT = os.path.join('valid', 'images')

all_txt_files = os.listdir(TXT_ROOT)

zero_counter = 0
txt_without_obj = []
for i, file_name in enumerate(all_txt_files):
    file_path = os.path.join(TXT_ROOT, file_name)
    with open(file_path, 'r') as f:
        lines = f.readlines()
        if len(lines) == 0:
            zero_counter += 1
            txt_without_obj.append(file_name.split('.txt')[0])
    f.close()

all_img_files = os.listdir(IMG_ROOT)
zero_img_counter = 0
for i, file_name in enumerate(all_img_files):
    file_path = os.path.join(IMG_ROOT, file_name)
    if '.'.join(file_name.split('.')[:-1]) in txt_without_obj:
        zero_img_counter += 1
        # image = cv2.imread(os.path.join(IMG_ROOT, file_name))
        # cv2.imshow('Image', image)
        # cv2.waitKey(0)
        os.remove(os.path.join(IMG_ROOT, file_name))
        os.remove(os.path.join(TXT_ROOT, '.'.join(file_name.split('.')[:-1])+'.txt'))

print(zero_img_counter)