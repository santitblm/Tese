import os
import cv2
from ultralytics import YOLO
from heuristic import LP_validation_and_correction as validate_string

#####################################################################################################
class_labels = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"
target_width = 500
flag = False
#####################################################################################################

# Function to calculate if two boxes are overlapping
def overlapping(x1, y1, x2, y2, X1, Y1, X2, Y2, thresh = 0.9):
    i = max(0, min(x2, X2) - max(x1, X1)) * max(0, min(y2, Y2) - max(y1, Y1))
    a1, a2 = (x2 - x1) * (y2 - y1), (X2 - X1) * (Y2 - Y1)
    print(i, a1, a2)
    if i == 0:
        return False, None
    elif i >= thresh * a1:
        return True, 1
    elif i >= thresh * a2:
        return True, 0

username = "Vastingood"
#username = "Santi LM"

LPs_path = f"C:/Users/{username}/Documents/Github/Tese/Backups/yolov8n_200e_12804/weights/best.pt"
LPs = YOLO(LPs_path)

Char_path = f"C:/Users/{username}/Documents/Github/Tese/Backups/LPChar_80e_384_5p_0mosaic/weights/best.pt"
Char = YOLO(Char_path)

# Open the video file
video_path = f"C:/Users/{username}/Desktop/20230419_102412.mp4"
cap = cv2.VideoCapture(video_path)

# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 inference on the frame
        LP_results = LPs(frame, device = "cpu")
        for r in LP_results:

            data = r.boxes.data
            boxes_with_labels = data.tolist()
            if len(boxes_with_labels) > 1:
                X1, Y1, X2, Y2 = map(int, boxes_with_labels[0][:4])
                i = 0
                print(boxes_with_labels[1:])
                for LP_box in boxes_with_labels[1:]:
                    x1, y1, x2, y2 = map(int, LP_box[:4])
                    overlaps, box = overlapping(x1, y1, x2, y2, X1, Y1, X2, Y2)
                    X1, Y1, X2, Y2 = map(int, LP_box[:4])
                    print(i, box)
                    if overlaps:
                        boxes_with_labels.remove(boxes_with_labels[i+box:1+i+box][0])
                    i += 1

                    
            for LP_box in boxes_with_labels:
                
                x1, y1, x2, y2 = map(int, LP_box[:4])
                lp_img = frame[y1:y2, x1:x2]

                # If the image's dimensions are valid
                if not lp_img.shape[0] > lp_img.shape[1] or not lp_img.shape[0] < 20 or not lp_img.shape[0] * lp_img.shape[1] < 1000:

                    # Detect characters in the license plate
                    Char_results = Char(lp_img, verbose = False)

                    for r in Char_results:

                        # Combine data with their respective class labels
                        data = r.boxes.data
                        boxes_with_labels = data.tolist()

                        # Sort the boxes by their class (label, the last value in each row)
                        sorted_boxes = sorted(boxes_with_labels, key=lambda x: x[0])

                        sorted_labels = [class_labels[int(box[5])] for box in sorted_boxes]
                        sorted_confidences = [int(box[4] * 100) for box in sorted_boxes]  # Multiply by 100 and round to int

                        # Join the sorted labels into a single string
                        result_string = "".join(sorted_labels)
                        validity, reason, str = validate_string(result_string, sorted_confidences, sorted_boxes)

                        # Read and resize the cropped_image
                        img = lp_img
                        print(img.shape)

                        resize_factor = target_width / img.shape[1]
                        cropped_image = cv2.resize(img, (int(img.shape[1] * resize_factor), int(img.shape[0] * resize_factor)))

                        # Show the resized image with rectangles and text
                        cv2.imshow("image", img)
                        print(validity, str, reason)
                        print(sorted_confidences)
                        key = cv2.waitKey(0)
                        cv2.destroyAllWindows()

                    if key == 27:
                        flag = True
                        break
                else:
                    print("Conditions not met")
                if flag:
                    break
            if flag:
                break
        if flag:
            break
    else:
        # Break the loop if the end of the video is reached
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()