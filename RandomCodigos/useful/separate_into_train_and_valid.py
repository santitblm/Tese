import os
import random
import shutil

# Set the value of r (0 <= r <= 1)
def separate():
    r = 0.2

    # Set the paths for the directories
    base_dir = "/home/santilm/Desktop/LPs_fromCars"
    #base_dir = "/home/santilm/Desktop/Tese/datasets/PT_LP_Characters"
    #base_dir = "/home/planeamusafrente/Desktop/SANTI/Tese/datasets/PT_LP_Characters"
    train_dir = os.path.join(base_dir, "train")
    valid_dir = os.path.join(base_dir, "valid")
    train_images_dir = os.path.join(train_dir, "images")
    valid_images_dir = os.path.join(valid_dir, "images")
    train_labels_dir = os.path.join(train_dir, "labels")
    valid_labels_dir = os.path.join(valid_dir, "labels")

    # Get the list of images in the train/images directory
    image_files = os.listdir(train_images_dir)

    # Calculate the number of images to move
    num_images_to_move = int(r * len(image_files))

    # Randomly select the images to move
    images_to_move = random.sample(image_files, num_images_to_move)

    # Move the selected images and their labels
    for image_file in images_to_move:
        # Move the image file
        src_image_path = os.path.join(train_images_dir, image_file)
        dst_image_path = os.path.join(valid_images_dir, image_file)
        shutil.move(src_image_path, dst_image_path)

        # Move the corresponding label file
        label_file = os.path.splitext(image_file)[0] + ".txt"
        src_label_path = os.path.join(train_labels_dir, label_file)
        dst_label_path = os.path.join(valid_labels_dir, label_file)
        shutil.move(src_label_path, dst_label_path)


separate()
