import numpy as np
import cv2
import os
from ultralytics import YOLO
import time as timer

#####################################################################################################
class_labels = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"
min_height = 23
min_area = 1000
#####################################################################################################

# Load the YOLOv8 model
model = YOLO('yolov8x.pt')

username , first_path = "planeamusafrente", "/home/planeamusafrente/Desktop/SANTI"
#username, first_path = "santilm", "/home/santilm/Desktop"


LPs_path = f"/home/{username}/Documents/GitHub/Tese/runs/detect/LP_fromCars_480_n/weights/best.pt"
LPs = YOLO(LPs_path)
Char_path = f"/home/{username}/Documents/GitHub/Tese/runs/detect/PT_LP_Characters_n/weights/best.pt"
Char = YOLO(Char_path)

cap = cv2.VideoCapture(video_path + video)

# define paths for ground truth and predictions
#ground_truth = f"/home/{username}/Desktop/GroundTruth_LPDet+OCR/{video}.txt" 
output_dir = f"/home/{username}/Desktop/Results_LPDet+OCR/{video}/ids/"

if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

def check_LP(box, frame, annotated_frame):
    result_strings = []
    X1, Y1, X2, Y2 = map(int, box)

    cv2.rectangle(annotated_frame, (X1, Y1), (X2, Y2), (0, 255, 0), 2)

    car_img = frame[Y1:Y2, X1:X2]
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
                #validity, _ = validate_string(result_string, sorted_confidences, sorted_boxes)
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

def organize_ids(ids_path):
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

            # Get the boxes and track IDs
            boxes = results[0].boxes.xyxy.cpu()
            track_ids = results[0].boxes.id.int().cpu().tolist()

            # Visualize the results on the frame
            #annotated_frame = results[0].plot()

            # Plot the tracks
            for box, track_id in zip(boxes, track_ids):
                strings, annotated_frame = check_LP(box, frame, annotated_frame)
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
#output_dir = f"/home/{username}/Desktop/Results_LPDet+OCR/CarDetect/1st/retiro/"

#for filename in os.listdir(output_dir):
#    organize_ids(output_dir + filename + "/ids/")

#output_dir = f"/home/{username}/Desktop/Results_LPDet+OCR/CarDetect/2nd/"
#for filename in os.listdir(output_dir):
#    organize_ids(output_dir + filename + "/ids/")

ground_truth_path = f"/home/santilm/Desktop/GroundTruth_LPDet+OCR/resol_test/" 
predictions_path = f"/home/santilm/Desktop/Results_LPDet+OCR/CarDetect/1st/"



calculate_metrics(ground_truth_path, predictions_path)



#organize_ids("/home/santilm/Desktop/Results_LPDet+OCR/CarDetect/1st/1st4K25xxx/ids/")


#video  = "20240209_151447.mp4"

#ground_truth = f"/home/santilm/Desktop/GroundTruth_LPDet+OCR/{video}.txt" 
#predicted = f"/home/santilm/Desktop/Results_LPDet+OCR/{video}/ids/results.txt"

#compare_results(ground_truth, predicted)

# Release the video capture object and close the display window
#cap.release()
#cv2.destroyAllWindows()

#import numpy as np


Precision = np.zeros((4, 4))
Recall = np.zeros((4, 4))
F1 = np.zeros((4, 4))
print(F1)
print(f''' \\begin{{table}}[!htb]
   \\caption{{Results for the ALPR system \\textbf{{without}} car detection on various resolutions}}
   \\label{{tab:ALPR_QuestForOptimalResolution_NOcardet}}
   \\centering
   \\renewcommand{{\\arraystretch}}{{1.2}}
   \\begin{{tabular}}{{@{{}}ccrccccccc@{{}}}}
     \\toprule
       \\multicolumn{{2}}{{c}}{{Models (size)}}  && \\multicolumn{{3}}{{c}}{{1080p30 (\\%)}} & \\phantom{{abc}} & \\multicolumn{{3}}{{c}}{{1080p60 (\\%)}} \\\\
     \\cmidrule{{4-6}}
     \\cmidrule{{8-10}}
     \\cmidrule{{1-2}}
       Characters & LPs         &&  Precision        &  Recall        &  F1        &&  Precision        &  Recall        &  F1 \\\\
     \\midrule
       Large      & Medium      && {Precision[0][0]} & {Recall[0][0]} & {F1[0][0]} && {Precision[1][0]} & {Recall[1][0]} & {F1[1][0]} \\\\
       Large      & ExtraLarge  && {Precision[0][1]} & {Recall[0][1]} & {F1[0][1]} && {Precision[1][1]} & {Recall[1][1]} & {F1[1][1]} \\\\
       ExtraLarge & Medium      && {Precision[0][2]} & {Recall[0][2]} & {F1[0][2]} && {Precision[1][2]} & {Recall[1][2]} & {F1[1][2]} \\\\
       ExtraLarge & ExtraLarge  && {Precision[0][3]} & {Recall[0][3]} & {F1[0][3]} && {Precision[1][3]} & {Recall[1][3]} & {F1[1][3]} \\\\
    \\midrule
      \\multicolumn{{2}}{{c}}{{Models (size)}} && \\multicolumn{{3}}{{c}}{{2.7K30 (\\%)}} & \\phantom{{abc}} & \\multicolumn{{3}}{{c}}{{4K25 (\\%)}} \\\\
     \\cmidrule{{4-6}}
     \\cmidrule{{8-10}}
     \\cmidrule{{1-2}}
       Characters & LPs         &&  Precision        &  Recall        &  F1        &&  Precision        &  Recall        &  F1 \\\\
     \\midrule
       Large      & Medium      && {Precision[2][0]} & {Recall[2][0]} & {F1[2][0]} && {Precision[3][0]} & {Recall[3][0]} & {F1[3][0]} \\\\
       Large      & ExtraLarge  && {Precision[2][1]} & {Recall[2][1]} & {F1[2][1]} && {Precision[3][1]} & {Recall[3][1]} & {F1[3][1]} \\\\
       ExtraLarge & Medium      && {Precision[2][2]} & {Recall[2][2]} & {F1[2][2]} && {Precision[3][2]} & {Recall[3][2]} & {F1[3][2]} \\\\
       ExtraLarge & ExtraLarge  && {Precision[2][3]} & {Recall[2][3]} & {F1[2][3]} && {Precision[3][3]} & {Recall[3][3]} & {F1[3][3]} \\\\
     \\bottomrule
   \\end{{tabular}}
 \\end{{table}}''')