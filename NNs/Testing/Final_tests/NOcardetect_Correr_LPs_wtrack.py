
from ultralytics import YOLO
import numpy as np
import cv2
import os
import time as timer

from heuristic import LP_val


#####################################################################################################
class_labels = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"
flag = False
min_height = 20
min_area = 1000
fps = 30
#####################################################################################################
# 2704x1524



def organize_ids(ids_path, FPS, time_init):
    # Iterate through files in the directory
    for filename in os.listdir(ids_path):

        file_path = os.path.join(ids_path, filename)

        predictions_path = os.path.join(ids_path.split("ids/")[0], "predictions.txt")
        # Read the file and count unique lines
        line_counts = {}
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for full_line in lines:
                line = full_line.split(" ")[0]
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
                if count > max_count and LP_val(line):
                    max_line = line
                    max_count = count
            
            last_frame = int(full_line.split(" ")[1])

            time = time_init + last_frame/fps
            last_time = f"{int(time)//3600:02d}:{int(time)%3600//60:02d}:{int(time)%60:02d}:{int((time - int(time))*1000):03d}"
            
            file.write(last_time)

            # In case there is no valid PT LP inside the id txt
            if max_line is None:
                for line, count in line_counts.items():
                    # Update max_line if necessary
                    if count > max_count:
                        max_line = line
                        max_count = count
            # In case at least one valid PT LP is present in the id txt
            else:
                with open(predictions_path, 'a') as predictions_file:
                    predictions_file.write(max_line + f" {last_time}\n")
            


    # When it is completed, write the number of FPS in a separate file

    with open(os.path.join(ids_path.split("ids/")[0], "FPS.txt"), 'w') as FPS_file:
        FPS_file.write(str(FPS))



#username , first_path = "planeamusafrente", "/home/planeamusafrente/Desktop/SANTI"
username, first_path = "santilm", "/home/santilm/Desktop"

LPs_path = f"/home/{username}/Documents/GitHub/Tese/runs/detect/LP_fromCars_1280_s/weights/best.pt"
Char_path = f"/home/{username}/Documents/GitHub/Tese/runs/detect/PT_LP_Characters_x/weights/best.pt"
Char = YOLO(Char_path)


videos = [
            ["20240415_155432266.MOV", 0*60+62, 2*60+52],
            ["20240415_155436900.MOV", 0*60+54, 2*60+47],
            ["20240415_164646933.MOV", 0*60+55, 2*60+41],
            ["20240415_164648500.MOV", 0*60+57, 2*60+40],
            ["20240416_124741800.MOV", 5*60+26, 7*60+20],
            ["20240416_124743199.MOV", 5*60+25, 7*60+ 8],
            ["20240416_144931533.MOV", 1*60+24, 3*60+43],
            ["20240416_144935000.MOV", 1*60+20, 3*60+32],
            ["20240416_155400300.MOV", 1*60+18, 3*60+21],
            ["20240416_155401733.MOV", 1*60+17, 3*60+15],
        ]


for info in videos:
    video, skip_first_seconds, process_until_seconds = info
    print(video)
    LPs = YOLO(LPs_path)

    # Open the video file
    video_path = f"{first_path}/Tese/datasets/Videos/"
    cap = cv2.VideoCapture(video_path + video)

    # Define path for predictions
    output_dir = f"/home/{username}/Desktop/Results_LPDet+OCR/Final_Tese/NoCD/{video}/ids/"

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)


    # Loop through the video frames
    n_frame = 0

    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            if process_until_seconds*fps > n_frame > skip_first_seconds*fps:    
                
                result_strings = []
                LP_results = LPs.track(frame, persist = True, max_det = 6, verbose = False)

                if LP_results[0].boxes.id is not None:
                    boxes = LP_results[0].boxes.xyxy.cpu()
                    track_ids = LP_results[0].boxes.id.int().cpu().tolist()
                    for box, track_id in zip(boxes, track_ids):
                        x1, y1, x2, y2 = map(int, box[:4])
                        #cv2.rectangle(annotated_frame, (X1+x1, Y1+y1), (X1+x2, Y1+y2), (0, 255, 255), 1)
                        lp_img = frame[y1:y2, x1:x2]

                        if not lp_img.shape[0] > lp_img.shape[1] and not lp_img.shape[0] < min_height and not lp_img.shape[0] * lp_img.shape[1] < min_area:
                            # Detect characters in the license plate
                            Char_results = Char(lp_img, verbose = False)

                            # Combine data with their respective class labels
                            Char_data = Char_results[0].boxes.data
                            boxes_with_labels = Char_data.tolist()

                            # Sort the boxes by their class (label, the last value in each row)
                            sorted_boxes = sorted(boxes_with_labels, key=lambda x: x[0])
                            sorted_labels = [class_labels[int(box[5])] for box in sorted_boxes]

                            # Join the sorted labels into a single string
                            result_string = "".join(sorted_labels)
                            # Define the text to display (label and confidence)
                            if len(result_string) == 6:
                                result_strings.append(result_string)


                    
                    for string in result_strings:
                        text_file_name = os.path.join(output_dir, f"{track_id}.txt")
                        # Write the LP as well as the number of the last frame at which it was seen
                        with open(text_file_name, "a") as text_file:
                            text_file.write(string + " " + str(n_frame) + "\n")


                # Display the annotated frame
                #cv2.imshow("YOLOv8 Tracking", annotated_frame)


                # Break the loop if 'q' is pressed
                #if cv2.waitKey(1) & 0xFF == ord("q"):
                #    break


            elif n_frame == skip_first_seconds*fps:
                starting_time = timer.time()
            elif n_frame == process_until_seconds*fps:
                end_time = timer.time()
            n_frame += 1

        else:
            # Break the loop if the end of the video is reached
            print("End of video, processing ids...")

            # Calculate the number of FPS
            FPS = (process_until_seconds-skip_first_seconds)*fps/(end_time-starting_time)

            # Get the time at which the recording started
            time_str = video.split('_')[1].split('.')[0]
            time_init = int(time_str[0:2])*3600 + int(time_str[2:4])*60 + int(time_str[4:6]) + float(time_str[6:9])/1000
            organize_ids(output_dir, FPS, time_init)
            print(FPS)
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()
