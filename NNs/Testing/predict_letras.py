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

model = YOLO(f"C:/Users/{username}/Documents/Github/Tese/Backups/LPCharFinal_l/weights/best.pt")
model2 = YOLO(f"C:/Users/{username}/Documents/Github/Tese/Backups/LPChar_200e_320_5p_autobatch_0mosaic_newdataugmentation2/weights/best.pt")

# Get a list of image file names in the folder
image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]
class_labels = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"

# Set the target width for resizing the images for better visualization
target_width = 320
# Iterate through the image files
for image_file in image_files:
    # Get the path to the current image
    source = folder_path + image_file

    results = model(source, verbose=False)
    results2 = model2(source, verbose=False)

    for (r, r2) in zip(results, results2):
        data = r.boxes.data
        data2 = r2.boxes.data

        # Combine data with their respective class labels
        boxes_with_labels = data.tolist()
        boxes_with_labels2 = data2.tolist()

        # Sort the boxes by their class (label, the last value in each row)
        sorted_boxes = sorted(boxes_with_labels, key=lambda x: x[0])
        sorted_boxes2 = sorted(boxes_with_labels2, key=lambda x: x[0])

        sorted_labels = [class_labels[int(box[5])] for box in sorted_boxes]
        sorted_confidences = [int(box[4] * 100) for box in sorted_boxes]  # Multiply by 100 and round to int
        sorted_labels2 = [class_labels[int(box[5])] for box in sorted_boxes2]
        sorted_confidences2 = [int(box[4] * 100) for box in sorted_boxes2]

        # Join the sorted labels into a single string
        result_string = "".join(sorted_labels)
        result_string2 = "".join(sorted_labels2)

        if result_string != result_string2:
            validity, _, _ = validate_string(result_string, sorted_confidences, sorted_boxes)
            validity2, _, _ = validate_string(result_string2, sorted_confidences2, sorted_boxes2)
            if (validity and not validity2) or (validity2 and not validity): 
                img = cv2.imread(source)
                resize_factor = target_width / img.shape[1]
                img = cv2.resize(img, (int(img.shape[1] * resize_factor), int(img.shape[0] * resize_factor)))
                img2 = img.copy()

                for box in sorted_boxes:
                    x1, y1, x2, y2 = map(int, box[:4])
                    x1, y1, x2, y2 = int(x1 * resize_factor), int(y1 * resize_factor), int(x2 * resize_factor), int(y2 * resize_factor)
                    label = class_labels[int(box[5])]
                    confidence = int(box[4] * 100)
                    cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 1)
                    text = f"{label} {confidence}"
                    text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                    text_x = x1
                    text_y = y1 - 5 if y1 - 5 > 5 else y1 + 20
                    cv2.putText(img, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

                for box in sorted_boxes2:
                    x1, y1, x2, y2 = map(int, box[:4])
                    x1, y1, x2, y2 = int(x1 * resize_factor), int(y1 * resize_factor), int(x2 * resize_factor), int(y2 * resize_factor)
                    label = class_labels[int(box[5])]
                    confidence = int(box[4] * 100)
                    cv2.rectangle(img2, (x1, y1), (x2, y2), (0, 255, 0), 1)
                    text = f"{label} {confidence}"
                    text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                    text_x = x1
                    text_y = y1 - 5 if y1 - 5 > 5 else y1 + 20
                    cv2.putText(img2, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
                cv2.imshow("latest", img)
                cv2.imshow("oldest", img2)
                print(result_string, " / ", result_string2)
                key = cv2.waitKey(0)
                cv2.destroyAllWindows()
                if key == 27:
                    break
        else:
            key = None
        continue
        #str = result_string
        validity, reason, str = validate_string(result_string, sorted_confidences, sorted_boxes)
        # Read image and iterate through sorted boxes if the string is invalid
        if not validity:# True:#
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
        if not validity:#True:#
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


