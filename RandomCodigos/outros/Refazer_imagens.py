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

                    # Calculate new dimensions while maintaining aspect ratio
                    #aspect_ratio = img.shape[1] / img.shape[0]
                    new_width = 85
                    new_height = 85

                    # Resize image
                    img_resized = cv2.resize(img, (new_width, new_height))

                    output_file_path = os.path.join(output_folder_current, f"{idx}.png")
                    
                    cv2.imwrite(output_file_path, img_resized)

if __name__ == "__main__":
    input_folder = "C:/Users/Santi LM/Documents/GitHub/Tese/RandomCodigos/data_augmentation/Fnt/"
    output_folder = "C:/Users/Santi LM/Documents/GitHub/Tese/RandomCodigos/data_augmentation/Fnt2/"
    resize_and_rename_images(input_folder, output_folder)
