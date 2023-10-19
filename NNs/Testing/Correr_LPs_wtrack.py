from collections import defaultdict

import cv2
import os
from ultralytics import YOLO
from heuristic import LP_validation_and_correction as validate_string

#####################################################################################################
class_labels = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"
target_width = 500
flag = False
min_height = 23
min_area = 1000
inval = 0 # variable to count invalid images
#####################################################################################################

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')

LPs_path = "runs/detect/yolov8n_200e_12804/weights/best.pt"
LPs = YOLO(LPs_path)
Char_path = "runs/detect/LPChar_80e_384_5p_0mosaic/weights/best.pt"
Char = YOLO(Char_path)

# Open the video file
video_path = "datasets/Videos/20221026_120014.MOV"
cap = cv2.VideoCapture(video_path)
output_dir = "ids/"

def check_str(box, frame):
    result_strings = []
    X1, Y1, X2, Y2 = box
    car_img = frame[int(Y1):int(Y2), int(X1):int(X2)]
    LP_results = LPs(car_img, verbose = False)
    LP_data = LP_results[0].boxes.data
    boxes_with_labels = LP_data.tolist()
    if len(boxes_with_labels) > 0:
        for box in boxes_with_labels:
            x1, y1, x2, y2 = map(int, box[:4])
            lp_img = car_img[y1:y2, x1:x2]
            if not lp_img.shape[0] > lp_img.shape[1] and not lp_img.shape[0] < min_height and not lp_img.shape[0] * lp_img.shape[1] < min_area:
                # Detect characters in the license plate
                Char_results = Char(lp_img, verbose = False)

                # Combine data with their respective class labels
                Char_data = Char_results[0].boxes.data
                boxes_with_labels = Char_data.tolist()

                # Sort the boxes by their class (label, the last value in each row)
                sorted_boxes = sorted(boxes_with_labels, key=lambda x: x[0])
                sorted_confidences = [int(box[4] * 100) for box in sorted_boxes]    # Multiply by 100 and round to int
                sorted_labels = [class_labels[int(box[5])] for box in sorted_boxes]

                # Join the sorted labels into a single string
                result_string = "".join(sorted_labels)
                validity, _, _ = validate_string(result_string, sorted_confidences, sorted_boxes)
                #print(validity, str)
                if validity:
                    result_strings.append(result_string)
    return result_strings


        


# Loop through the video frames
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, classes = [2, 3, 5, 7], verbose = False)
        vehicle_data = results[0].boxes.data
        boxes_with_labels = vehicle_data.tolist()
        if results[0].boxes.id is not None:
            # Get the boxes and track IDs
            boxes = results[0].boxes.xyxy.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()

            # Visualize the results on the frame
            annotated_frame = results[0].plot()

            # Plot the tracks
            for box, track_id in zip(boxes, track_ids):
                x1, y1, x2, y2 = box
                strings = check_str(box, frame)
                for string in strings:
                    text_file_name = os.path.join(output_dir, f"{track_id}.txt")
                    with open(text_file_name, "a") as text_file:
                        text_file.write(string + "\n")
                
        else:
            annotated_frame = frame
        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        print("End of video")
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()
