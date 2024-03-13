import os
import cv2

#TXT_ROOT = "/home/santilm/Desktop/Tese/datasets/PT_LP_Characters/train/labels/"
#IMG_ROOT = "/home/santilm/Desktop/Tese/datasets/PT_LP_Characters/train/images/"
TXT_ROOT = "/home/santilm/Desktop/labels/"
IMG_ROOT = "/home/santilm/Desktop/imagens para LPs dataset/"

all_txt_files = os.listdir(TXT_ROOT)

#zero_counter = 0
#txt_without_obj = []
#for i, file_name in enumerate(all_txt_files):
#    file_path = os.path.join(TXT_ROOT, file_name)
#    with open(file_path, 'r') as f:
#        lines = f.readlines()
#        if len(lines) == 0:
#            zero_counter += 1
#            txt_without_obj.append(file_name.split('.txt')[0])
#    f.close()

all_img_files = os.listdir(IMG_ROOT)
new_label_counter  = 0
for i, file_name in enumerate(all_img_files):
    file_path = os.path.join(IMG_ROOT, file_name)
    #print(file_path)
    name = os.path.join(TXT_ROOT, '.'.join(file_name.split('.')[:-1])+'.txt')
    print(name)
    if not os.path.isfile(name):
        new_label_counter += 1
        with open(name, 'w') as f:
            f.write("")
        # image = cv2.imread(os.path.join(IMG_ROOT, file_name))
        # cv2.imshow('Image', image)
        # cv2.waitKey(0)
        #os.remove(file_path)

        #os.remove(os.path.join(TXT_ROOT, '.'.join(file_name.split('.')[:-1])+'.txt'))

print(new_label_counter)