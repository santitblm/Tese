import os
import cv2
from ultralytics import YOLO

# Set the folder path containing the images
#folder_path = 'datasets/PT_LP_Characters/test_nolabels/images/'
folder_path = 'C:/Users/Vastingood/Documents/GitHub/Tese/RandomCodigos/data_augmentation/synthetic/images/'

model = YOLO("C:/Users/Vastingood/Documents/GitHub/Tese/Backup/LPChar_50e_256_medium2/weights/best.pt")

# Get a list of image file names in the folder
image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
class_labels = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"

# Resize factor
resize_factor = 10

# Iterate through the image files
for image_file in image_files:
    # Get the path to the current image
    source = folder_path + image_file

    results = model(source)

    for r in results:
        data = r.boxes.data
        print(data)
        # Combine data with their respective class labels
        boxes_with_labels = data.tolist()

        # Sort the boxes by their class (label, the last value in each row)
        sorted_boxes = sorted(boxes_with_labels, key=lambda x: x[0])

        sorted_labels = [class_labels[int(box[5])] for box in sorted_boxes]
        sorted_confidences = [int(box[4] * 100) for box in sorted_boxes]  # Multiply by 100 and round to int

        # Join the sorted labels into a single string
        result_string = "".join(sorted_labels)

        # Read and resize the image
        img = cv2.imread(source)
        img = cv2.resize(img, (img.shape[1] * resize_factor, img.shape[0] * resize_factor))

        # Iterate through sorted boxes
        for box in sorted_boxes:
            x1, y1, x2, y2 = map(int, box[:4])

            # Resize the box coordinates
            x1, y1, x2, y2 = x1 * resize_factor, y1 * resize_factor, x2 * resize_factor, y2 * resize_factor

            label = class_labels[int(box[5])]
            confidence = int(box[4] * 100)

            # Draw a rectangle around the object
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # Define the text to display (label and confidence)
            text = f"{label} {confidence}"

            # Calculate the position for the text
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
            text_x = x1
            text_y = y1 - 5 if y1 - 5 > 5 else y1 + 20

            # Draw the text
            cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Show the resized image with rectangles and text
        cv2.imshow("image", img)
        print(result_string)
        print(sorted_confidences)
        key = cv2.waitKey(0)
        cv2.destroyAllWindows()

        if key == 27:
            break

    if key == 27:
        break
