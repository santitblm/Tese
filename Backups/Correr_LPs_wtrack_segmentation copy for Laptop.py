from collections import defaultdict
import numpy as np
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
#points_to_cover = np.array([[0, 390], [1920, 1020], [1920, 1080], [0, 1080]], np.int32)#[[0, 1080], [0, 970], [1150, 530], [1920, 540], [1920, 1080]], np.int32)
#####################################################################################################

# Load the YOLOv8 model
model = YOLO('yolov8n-seg.pt')

LPs_path = "Backups/yolov8n_200e_12804/weights/best.pt"
LPs = YOLO(LPs_path)
Char_path = "Backups/LPChar_80e_384_5p_0mosaic/weights/best.pt"
Char = YOLO(Char_path)

# Open the video file
video_path = "C:/Users/Santi LM/Downloads/"
video  = "20240209_151447.mp4"
cap = cv2.VideoCapture(video_path + video)
output_dir = "ids/"

def check_LP(box, seg_mask, frame):

    pol_points = np.array(seg_mask.xy, dtype = np.int32)
    # Paint the pixels outside the car black
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, [pol_points], (255, 255, 255))
    result = cv2.bitwise_and(frame, mask)

    result_strings = []
    X1, Y1, X2, Y2 = map(int, box)

    cv2.rectangle(frame, (X1, Y1), (X2, Y2), (0, 255, 0), 2)

    car_img = result[Y1:Y2, X1:X2]
    LP_results = LPs(car_img, verbose = False)
    LP_data = LP_results[0].boxes.data
    boxes_with_labels = LP_data.tolist()
    if len(boxes_with_labels) > 0:
        for box in boxes_with_labels:
            x1, y1, x2, y2 = map(int, box[:4])
            cv2.rectangle(frame, (X1+x1, Y1+y1), (X1+x2, Y1+y2), (0, 255, 255), 1)
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
                validity, _ = validate_string(result_string, sorted_confidences, sorted_boxes)
                # Define the text to display (label and confidence)
                if len(result_string) > 4:
                    text = result_string

                    # Calculate the position for the text
                    #text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                    text_x = X1+x1
                    text_y = Y1 + y1 - 5 if Y1 + y1 - 5 > 5 else Y1 + y1 + 20

                    # Draw the text
                    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 4)

                #print(validity, str)
                if validity:
                    result_strings.append(result_string)
    return result_strings

# Get the initial time of the video from its filename
time_str = video.split('_')[1].split('.')[0]
time_init = int(time_str[0:2])*3600 + int(time_str[2:4])*60 + int(time_str[4:6])

# Loop through the video frames
n_frame = 0
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        #cv2.fillPoly(frame, pts = [points_to_cover], color=(0, 0, 0))
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, classes = [2, 5, 7], verbose = False, max_det = 6)
        vehicle_data = results[0].boxes.data
        boxes_with_labels = vehicle_data.tolist()

        if results[0].boxes.id is not None:

            # Get the masks
            seg_masks = results[0].masks

            # Get the boxes and track IDs
            boxes = results[0].boxes.xyxy.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()

            # Visualize the results on the frame
            #annotated_frame = results[0].plot()

            # Plot the tracks
            for box, seg_mask, track_id in zip(boxes, seg_masks, track_ids):
                strings = check_LP(box, seg_mask, frame)
                for string in strings:
                    text_file_name = os.path.join(output_dir, f"{track_id}.txt")
                    time = time_init + n_frame/30
                    time_str = f"{int(time)//3600:02d}:{int(time)%3600//60:02d}:{int(time)%60:02d}:{int((time - int(time))*1000):03d}"
                    #with open(text_file_name, "a") as text_file:
                    #    text_file.write(string + " " + time_str + "\n")
              
        annotated_frame = frame
        # Display the annotated frame
        w = int(frame.shape[1]*0.6)
        h = int(frame.shape[0]*0.6)
        res = cv2.resize(annotated_frame, (w, h)) 
        cv2.imshow("YOLOv8 Tracking", res)
        n_frame += 1

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

