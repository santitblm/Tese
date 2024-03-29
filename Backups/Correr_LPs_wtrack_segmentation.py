from collections import defaultdict
import numpy as np
import cv2
import os
from ultralytics import YOLO
from heuristic import LP_validation_and_correction as validate_string
import time as timer

#####################################################################################################
class_labels = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"
#target_width = 500
#flag = False
min_height = 23
min_area = 1000
#inval = 0 # variable to count invalid images
#points_to_cover = np.array([[0, 600], [1920, 600], [1920, 1080], [0, 1080]], np.int32)#
#points_to_cover = np.array([[0, 1080], [0, 970], [1150, 530], [1920, 540], [1920, 1080]], np.int32)
#points_to_cover = np.array([[960, 1080], [1440, 480], [1500, 0], [1920, 0], [1920, 1080]], np.int32) #lado esquerdo
#points_to_cover = np.array([[960, 1080], [540, 720], [120, 0], [0, 0], [0, 1080]], np.int32) #lado direito
#####################################################################################################

# Load the YOLOv8 model
model = YOLO('yolov8x-seg.pt')

LPs_path = "/home/santilm/Documents/GitHub/Tese/runs/detect/LP_fromCars_480_x/weights/best.pt"
LPs = YOLO(LPs_path)
Char_path = "/home/santilm/Documents/GitHub/Tese/runs/detect/PT_LP_Characters_x/weights/best.pt"
Char = YOLO(Char_path)

# Open the video file
video_path = "/home/santilm/Desktop/Tese/datasets/Videos/"
#video  = "20240209_151447.mp4" #sem cobrir
#video = "20221026_141258.MOV" #lado esquerdo
#video = "20221026_125944.MOV" #lado direito
#ideo = "20221026_142307.MOV" #lado direito
#video = "20221026_151500.MOV" #lado direito
#video = "20230602_134058.mp4" 

video = "20240329_124851.MOV"
#video = ""
#video = ""
#video = ""

#video = ""
cap = cv2.VideoCapture(video_path + video)

# define paths for ground truth and predictions
ground_truth = f"/home/santilm/Desktop/GroundTruth_LPDet+OCR/{video}.txt" 
output_dir = f"/home/santilm/Desktop/Results_LPDet+OCR/{video}/ids/"
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

def check_LP(box, seg_mask, frame, annotated_frame):
    pol_points = np.array(seg_mask.xy, dtype = np.int32)
    # Paint the pixels outside the car black
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, [pol_points], (255, 255, 255))
    result = cv2.bitwise_and(frame, mask)

    result_strings = []
    X1, Y1, X2, Y2 = map(int, box)

    cv2.rectangle(annotated_frame, (X1, Y1), (X2, Y2), (0, 255, 0), 2)

    car_img = result[Y1:Y2, X1:X2]
    LP_results = LPs(car_img, verbose = False)
    LP_data = LP_results[0].boxes.data
    boxes_with_labels = LP_data.tolist()
    if len(boxes_with_labels) > 0:
        for box in boxes_with_labels:
            x1, y1, x2, y2 = map(int, box[:4])
            cv2.rectangle(annotated_frame, (X1+x1, Y1+y1), (X1+x2, Y1+y2), (0, 255, 255), 1)
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
                    text_x = x1+X1
                    text_y = Y1+y1 - 5# if Y1+y1 - 5 > 5 else Y1 + 20

                    # Draw the text
                    cv2.putText(annotated_frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

                #print(validity, str)
                #if validity:
                    result_strings.append(result_string)
    return result_strings, annotated_frame

def organize_ids(ids_path, FPS):
    # Iterate through files in the directory
    for filename in os.listdir(ids_path):

        file_path = os.path.join(ids_path, filename)

        predictions_path = os.path.join(ids_path.split("ids/")[0], "predictions.txt")
        # Read the file and count unique lines
        line_counts = {}
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line in line_counts:
                    line_counts[line] += 1
                else:
                    line_counts[line] = 1
        
        # Write unique lines and counts back to the file
        with open(file_path, 'w') as file:
            max_count = 0
            for line, count in line_counts.items():
                file.write(f"{line} {count}\n")
                # Update max_line if necessary
                if count > max_count:
                    max_line = line
                    max_count = count
    
        # Write the line with the maximum count to predictions.txt
        if max_line is not None:
            with open(predictions_path, 'a') as predictions_file:
                predictions_file.write(max_line + "\n")

    # When it is completed, write the number of FPS in the last line

    with open(os.path.join(ids_path.split("ids/")[0], "FPS.txt"), 'w') as FPS_file:
        FPS_file.write(str(FPS))


# Get the initial time of the video from its filename
#time_str = video.split('_')[1].split('.')[0]
#time_init = int(time_str[0:2])*3600 + int(time_str[2:4])*60 + int(time_str[4:6])

# Loop through the video frames
n_frame = 0
starting_time = timer.time()

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        #cv2.fillPoly(frame, pts = [points_to_cover], color=(0, 0, 0))
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, classes = [2, 7], verbose = False, max_det = 6)
        vehicle_data = results[0].boxes.data
        boxes_with_labels = vehicle_data.tolist()
        annotated_frame = frame.copy()
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
                strings, annotated_frame = check_LP(box, seg_mask, frame, annotated_frame)
                for string in strings:
                    text_file_name = os.path.join(output_dir, f"{track_id}.txt")
                #    time = time_init + n_frame/30
                #    time_str = f"{int(time)//3600:02d}:{int(time)%3600//60:02d}:{int(time)%60:02d}:{int((time - int(time))*1000):03d}"
                    with open(text_file_name, "a") as text_file:
                        #text_file.write(string + " " + time_str + "\n")
                        text_file.write(string + "\n")


        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)
        n_frame += 1

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    
    else:
        # Break the loop if the end of the video is reached
        end_time = timer.time()
        print("End of video, processing ids...")

        # Calculate the number of FPS
        FPS = n_frame/(end_time-starting_time)
        #organize_ids(output_dir, FPS)
        print(FPS)
        break

# Release the video capture object and close the display window
cap.release()
cv2.destroyAllWindows()

