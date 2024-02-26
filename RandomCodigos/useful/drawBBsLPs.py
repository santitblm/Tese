import os
import cv2

def draw_bounding_boxes_for_folder(images_folder, labels_folder):

    for image_filename in os.listdir(images_folder):
        if image_filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(images_folder, image_filename)

            # Get the corresponding text file with bounding box information
            txt_filename = os.path.splitext(image_filename)[0] + '.txt'
            txt_path = os.path.join(labels_folder, txt_filename)

            # Check if the corresponding text file exists
            if os.path.isfile(txt_path):
                # Read the image
                image = cv2.imread(image_path)

                # Read the bounding box information from the text file
                with open(txt_path, 'r') as file:
                    lines = file.readlines()

                # Draw bounding boxes on the image
                for line in lines:
                    values = line.split()
                    x_center = float(values[1])
                    y_center = float(values[2])
                    width = float(values[3])
                    height = float(values[4])

                    # Calculate bounding box coordinates
                    x1 = int((x_center - width / 2) * image.shape[1])
                    y1 = int((y_center - height / 2) * image.shape[0])
                    x2 = int((x_center + width / 2) * image.shape[1])
                    y2 = int((y_center + height / 2) * image.shape[0])

                    # Draw bounding box on the image
                    color = (0, 255, 0)  # Green color
                    thickness = 1
                    image = cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)

                # Display the image with bounding boxes
                cv2.imshow(image_filename, image)
                key = cv2.waitKey(0)
                cv2.destroyAllWindows()
                if key == 27:
                    break

# Example usage:
#username = "Vastingood"
#images_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/synthetic/images/"
#labels_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/synthetic/labels/"
#images_folder  = f"/home/santilm/Desktop/teste/images/"
#labels_folder = f"/home/santilm/Desktop/teste/labels/"
images_folder = f"/home/santilm/Desktop/Tese/datasets/LPs_Cars/train/images/"
labels_folder = f"/home/santilm/Desktop/Tese/datasets/LPs_Cars/train/labels/"
draw_bounding_boxes_for_folder(images_folder, labels_folder)
