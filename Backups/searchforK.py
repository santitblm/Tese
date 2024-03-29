import os
from tqdm import tqdm
import cv2

folder_path = "/home/santilm/Desktop/Tese/datasets/PT_LP_Characters_ORIGINALS/train/labels/"

def check_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if float(line.split()[0]) == 10.0:
                print("K found in", file_path)

def check_files_in_folder(folder_path):
    n = 1475
    progress_bar = tqdm(total=n, desc="Progress")
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            check_file(file_path)
        progress_bar.update(1)
    progress_bar.close()    

#if __name__ == "__main__":
#    check_files_in_folder(folder_path)

cv2.imshow("image", cv2.imread("/home/santilm/Desktop/Tese/datasets/PT_LP_Characters_ORIGINALS/train/images/1_vlcsnap-2023-05-05-19h11m04s619.jpg"))
cv2.waitKey(0)
cv2.destroyAllWindows()