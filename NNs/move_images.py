import os
import shutil

def copy_files(source_dir, destination_dir):
    try:
        # List all files in the source directory
        files = os.listdir(source_dir)

        # Copy each file from the source to the destination directory
        for file in files:
            source_path = os.path.join(source_dir, file)
            destination_path = os.path.join(destination_dir, file)
            shutil.copy2(source_path, destination_path)  # Use shutil.copy2 to preserve metadata

        print("Files copied successfully.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    source_directory = "/home/santilm/Documents/GitHub/Tese/RandomCodigos/data_augmentation/synthetic/labels"

    #source_directory = "/dev/nvme0n1p4/Users/Vastingood/Documents/Github/Tese/RandomCodigos/data_augmentation/synthetic/images/"
    destination_directory = "/home/santilm/Desktop/Tese/datasets/PT_LP_Characters/train/labels"

    copy_files(source_directory, destination_directory)
