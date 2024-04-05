import os
import cv2
from ultralytics import YOLO

model = YOLO("runs/detect/License_Plates_1280_x/weights/best.pt")

def draw_bounding_boxes_for_folder(images_folder, labels_folder):
    show = False
    for image_filename in os.listdir(images_folder):
        if image_filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(images_folder, image_filename)

            # Get the corresponding text file with bounding box information
            txt_filename = os.path.splitext(image_filename)[0] + '.txt'
            txt_path = os.path.join(labels_folder, txt_filename)

            # Check if the corresponding text file exists
            if os.path.isfile(txt_path):

                # Read the image and run inference
                image = cv2.imread(image_path)
                results = model(image, show = False)

                for r in results:
                    data = r.boxes.data

                    # Combine data with their respective class labels
                    boxes= data.tolist()
                    for box in boxes:
                        x1, y1, x2, y2 = map(int, box[:4])
                        label_pred = int(box[5])
                        if label_pred == 1:
                            show = True
                        # Draw a rectangle around the object
                        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 0, 255) if label_pred == 0 else (255, 0, 0), 2 )

                # Read the bounding box information from the text file
                with open(txt_path, 'r') as file:
                    lines = file.readlines()

                # Draw bounding boxes on the image
                for line in lines:
                    values = line.split()
                    label_true = int(values[0])
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
                    color = (255, 255, 255)  if label_true == 0 else (0, 255, 0)# Green color
                    thickness = 1
                    image = cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
                    if label_true == 1:
                        show = True

                # Display the image with bounding boxes
                if show:
                    cv2.imshow(image_filename, image)
                    key = cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    if key == 27:
                        break
                    show = False

# Example usage:
#username = "Vastingood"
#images_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/synthetic/images/"
#labels_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/synthetic/labels/"
#images_folder  = f"/home/santilm/Desktop/teste/images/"
#labels_folder = f"/home/santilm/Desktop/teste/labels/"
images_folder = "/home/santilm/Desktop/Tese/datasets/License_Plates/test/images/"#LPs_fromCars/train/images/"
labels_folder = "/home/santilm/Desktop/Tese/datasets/License_Plates/test/labels/"#LPs_fromCars/train/labels/"
#images_folder = "/home/santilm/Desktop/Tese/datasets/LPs_fromCars/test/images/"
#labels_folder = "/home/santilm/Desktop/Tese/datasets/LPs_fromCars/test/labels/"

draw_bounding_boxes_for_folder(images_folder, labels_folder)
