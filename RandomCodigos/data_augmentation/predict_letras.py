import os
import cv2
from ultralytics import YOLO
from heuristic import LP_validation_and_correction as validate_string

# Set the folder path containing the images
username = "Vastingood"
username = "Santi LM"
#folder_path = 'datasets/PT_LP_Characters/test_nolabels/images/'
folder_path = f'C:/Users/{username}/Documents/GitHub/Tese/cropped/'
#folder_path = f"C:/Users/{username}/Desktop/teste_cropped/"#for_testing/"

model = YOLO(f"C:/Users/{username}/Documents/Github/Tese/Backups/LPChar_80e_384_5p_0mosaic/weights/best.pt")

# Get a list of image file names in the folder
image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
class_labels = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"

# Set the target width for resizing the images for better visualization
target_width = 500
# Iterate through the image files
for image_file in image_files:
    # Get the path to the current image
    source = folder_path + image_file

    results = model(source, verbose=False)

    for r in results:
        data = r.boxes.data
        #print(data)
        # Combine data with their respective class labels
        boxes_with_labels = data.tolist()

        # Sort the boxes by their class (label, the last value in each row)
        sorted_boxes = sorted(boxes_with_labels, key=lambda x: x[0])

        sorted_labels = [class_labels[int(box[5])] for box in sorted_boxes]
        sorted_confidences = [int(box[4] * 100) for box in sorted_boxes]  # Multiply by 100 and round to int

        # Join the sorted labels into a single string
        result_string = "".join(sorted_labels)
        validity, reason, str = validate_string(result_string, sorted_confidences, sorted_boxes)
        # Read image and iterate through sorted boxes if the string is invalid
        if not validity:
            print(image_file)
            print("The corrected license plate turned out ", str)
            # Read and resize the image
            img = cv2.imread(source)
            resize_factor = target_width / img.shape[1]
            #print(resize_factor)
            img = cv2.resize(img, (int(img.shape[1] * resize_factor), int(img.shape[0] * resize_factor)))
            for box in sorted_boxes:
                x1, y1, x2, y2 = map(int, box[:4])

                # Resize the box coordinates
                x1, y1, x2, y2 = int(x1 * resize_factor), int(y1 * resize_factor), int(x2 * resize_factor), int(y2 * resize_factor)

                label = class_labels[int(box[5])]
                confidence = int(box[4] * 100)

                # Draw a rectangle around the object
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)

                # Define the text to display (label and confidence)
                text = f"{label} {confidence}"

                # Calculate the position for the text
                text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                text_x = x1
                text_y = y1 - 5 if y1 - 5 > 5 else y1 + 20

                # Draw the text
                cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        # Show the resized image with rectangles and text
        
        print(result_string)
        print(sorted_confidences)
        if not validity:
            cv2.imshow("image", img)
            print(reason)
            key = cv2.waitKey(0)
            cv2.destroyAllWindows()
            if key == 27:
                break
        else:
            key = None

    if key == 27:
        break


