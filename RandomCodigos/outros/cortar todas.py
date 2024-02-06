import os
import cv2

def resize_and_rename_images(input_folder, output_folder, max_width=75, max_height=85):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for folder_name in os.listdir(input_folder):
        folder_path = os.path.join(input_folder, folder_name)

        if os.path.isdir(folder_path):
            for idx, file_name in enumerate(os.listdir(folder_path)):
                file_path = os.path.join(folder_path, file_name)
                output_folder_current = os.path.join(output_folder, folder_name)
                if not os.path.exists(output_folder_current):
                    os.makedirs(output_folder_current)

                if os.path.isfile(file_path) and file_name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    img = cv2.imread(file_path)

                    img_resized = img[7:78, 7:78]
                    output_file_path = os.path.join(output_folder_current, file_name)
                    
                    cv2.imwrite(output_file_path, img_resized)

if __name__ == "__main__":
    input_folder = "C:/Users/Vastingood/Documents/GitHub/Tese/RandomCodigos/data_augmentation/Fnt2/"
    output_folder = "C:/Users/Vastingood/Documents/GitHub/Tese/RandomCodigos/data_augmentation/Fnt3/"
    resize_and_rename_images(input_folder, output_folder)

