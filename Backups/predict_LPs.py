import os
import cv2
from ultralytics import YOLO

# Set the folder path containing the images
folder_path = 'datasets/License_Plates/train/images/'
LPs = YOLO("runs/detect/yolov8n_200e_12804/weights/best.pt")
Char = YOLO("runs/detect/LPChar_80e_384_5p_0mosaic/weights/best.pt")
image_files = [f for f in os.listdir(folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

#####################################################################################################
temp = "temp/temp.jpg"
class_labels = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"
target_width = 500
flag = False
#####################################################################################################

for image_file in image_files:
    source = folder_path + image_file
    LP_results = LPs(source)#, verbose = False)
    image = cv2.imread(source)
    for r in LP_results:
        data = r.boxes.data
        boxes_with_labels = data.tolist()
        for LP_box in boxes_with_labels:
            x1, y1, x2, y2 = map(int, LP_box[:4])
            cropped_image = image[y1:y2, x1:x2]
            cv2.imwrite(temp, cropped_image)
            Char_results = Char(temp, verbose = False)
            for r in Char_results:
                data = r.boxes.data
                # Combine data with their respective class labels
                boxes_with_labels = data.tolist()

                # Sort the boxes by their class (label, the last value in each row)
                sorted_boxes = sorted(boxes_with_labels, key=lambda x: x[0])

                sorted_labels = [class_labels[int(box[5])] for box in sorted_boxes]
                sorted_confidences = [int(box[4] * 100) for box in sorted_boxes]  # Multiply by 100 and round to int

                # Join the sorted labels into a single string
                result_string = "".join(sorted_labels)

                # Read and resize the cropped_image
                img = cropped_image
                resize_factor = target_width / img.shape[1]
                cropped_image = cv2.resize(img, (int(img.shape[1] * resize_factor), int(img.shape[0] * resize_factor)))

                # Show the resized image with rectangles and text
                cv2.imshow("image", img)
                print(result_string)
                print(sorted_confidences)
                key = cv2.waitKey(0)
                cv2.destroyAllWindows()

                if key == 27:
                    flag = True
                    break

            if flag:
                break
        if flag:
            break
    if flag:
        break