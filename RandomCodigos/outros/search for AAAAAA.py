import os
from tqdm import tqdm
import cv2

folder_path = "/home/santilm/Desktop/Tese/datasets/PT_LP_Characters/train/labels/"

def check_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        all_lines_start_with_zero = all(float(line.split()[0]) == 0.0 for line in lines)
        if all_lines_start_with_zero:
            print(f"File with all lines starting with 0: {file_path}")

def check_files_in_folder(folder_path):
    n = 100000
    progress_bar = tqdm(total=n, desc="Progress")
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".txt"):
            file_path = os.path.join(folder_path, file_name)
            check_file(file_path)
        progress_bar.update(1)
    progress_bar.close()    

#if __name__ == "__main__":
#    check_files_in_folder(folder_path)

cv2.imshow("image", cv2.imread("/home/santilm/Desktop/Tese/datasets/PT_LP_Characters/train/images/1_vlcsnap-2023-05-23-22h40m25s720.jpg"))
cv2.waitKey(0)
cv2.destroyAllWindows()