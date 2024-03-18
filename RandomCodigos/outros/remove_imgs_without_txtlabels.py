import os
import cv2

TXT_ROOT = "/home/santilm/Desktop/Tese/datasets/PT_LP_Characters/test/labels/"
IMG_ROOT = "/home/santilm/Desktop/Tese/datasets/PT_LP_Characters/test/images/"
#TXT_ROOT = "/home/santilm/Desktop/Tese/datasets/License_Plates/train/labels/"
#IMG_ROOT = "/home/santilm/Desktop/Tese/datasets/License_Plates/train/images/"


all_img_files = os.listdir(IMG_ROOT)
removed_image_counter  = 0
for i, file_name in enumerate(all_img_files):
    file_path = os.path.join(IMG_ROOT, file_name)
    name = os.path.join(TXT_ROOT, '.'.join(file_name.split('.')[:-1])+'.txt')
    #print(name)
    if not os.path.isfile(name):
        removed_image_counter += 1
        #with open(name, 'w') as f:
        #    f.write("")
        
        # image = cv2.imread(os.path.join(IMG_ROOT, file_name))
        # cv2.imshow('Image', image)
        # cv2.waitKey(0)

        #os.remove(file_path)

        #os.remove(os.path.join(TXT_ROOT, '.'.join(file_name.split('.')[:-1])+'.txt'))

print(removed_image_counter)