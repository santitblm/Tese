import cv2
import os
from ultralytics import YOLO
import time as timer
import numpy as np

from heuristic import LP_val

#####################################################################################################
class_labels = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"
min_height = 23/1080
min_width = 45/1920
n_video = 1
#####################################################################################################
#1920*1080
#2704*1524
#3840*2160
#username , first_path = "planeamusafrente", "/home/planeamusafrente/Desktop/SANTI"
username, first_path = "santilm", "/home/santilm/Desktop"

Char_sizes = ["l", "x"]
LP_sizes = ["m", "x"]


skip = 0

# Open the video file
video_path = f"{first_path}/Tese/datasets/Videos/"

#TODO: apagar todos os ids anteriores depois de testar todos os core dumps TODO TODO TODO !!!!!!!!!!!!!!!!!!!!!!!

videos = [
            ["1st1080p30.MOV",  30, 33, 2*60+41],
            ["1st1080p60.MOV",  60, 30, 2*60+38],
            ["1st27K30.MOV",    30, 30, 2*60+38],
            ["1st4K25.MOV",     25, 30, 2*60+39],
            ["2nd1080p30.MOV",  30, 27, 2*60+20],
            ["2nd1080p60.MOV",  60, 25, 2*60+23],
            ["2nd27K30.MOV",    30, 28, 2*60+22],
            ["2nd4K25.MOV",     25, 28, 2*60+22],
            ["3rd1080p30.MOV",  30, 48, 2*60+38],
            ["3rd1080p60.MOV",  60, 47, 2*60+38],
            ["3rd27K30.MOV",    30, 50, 2*60+40],
            ["3rd4K25.MOV",     25, 46, 2*60+38],
            ["4th1080p30.MOV",  30, 59, 4*60+ 6],
            ["4th1080p60.MOV",  60, 59, 4*60+ 1],
            ["4th27K30.MOV",    30, 59, 4*60+ 3],
            ["4th4K25.MOV",     25, 59, 4*60+ 1],
            ["5th1080p30.MOV",  30, 30, 5*60+11],
            ["5th1080p60.MOV",  60, 20, 5*60+ 1],
            ["5th27K30.MOV",    30, 33, 5*60+12],
            ["5th4K25.MOV",     25, 22, 5*60+ 1]
        ]


def check_LP(box, frame, seg_mask):
    pol_points = np.array(seg_mask.xy, dtype = np.int32)
    # Paint the pixels outside the car black
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, [pol_points], (255, 255, 255))
    result = cv2.bitwise_and(frame, mask)

    result_strings = []
    X1, Y1, X2, Y2 = map(int, box)

    # Draw a rectangle around the car
    #cv2.rectangle(annotated_frame, (X1, Y1), (X2, Y2), (0, 255, 0), 2)

    car_img = result[Y1:Y2, X1:X2]
    LP_results = LPs(car_img, verbose = False)
    LP_data = LP_results[0].boxes.data
    boxes_with_labels = LP_data.tolist()
    if len(boxes_with_labels) > 0:
        for box in boxes_with_labels:
            x1, y1, x2, y2 = map(int, box[:4])
            #cv2.rectangle(annotated_frame, (X1+x1, Y1+y1), (X1+x2, Y1+y2), (0, 255, 255), 1)
            lp_img = car_img[y1:y2, x1:x2]
            if not lp_img.shape[0] > lp_img.shape[1] and not lp_img.shape[0]/frame.shape[0] < min_height/frame.shape[0] and not lp_img.shape[1]/frame.shape[1] < min_width/frame.shape[1]:
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
                    #text = result_string

                    # Calculate the position for the text
                    #text_x = x1+X1
                    #text_y = Y1+y1 - 5# if Y1+y1 - 5 > 5 else Y1 + 20

                    # Draw the text
                    #cv2.putText(annotated_frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    #return result_strings, annotated_frame
    return result_strings


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
                if line in line_counts:
                    line_counts[line] += 1
                else:
                    line_counts[line] = 1
        
        # Write unique lines and counts back to the file
        with open(file_path, 'w') as file:
            max_count = 0
            for line, count in line_counts.items():
                line = line.split("\n")[0]
                file.write(f"{line} {count}\n")
                # Update max_line if necessary
                #print(line)
                if count > max_count and LP_val(line):
                    max_line = line
                    max_count = count

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
                    predictions_file.write(max_line+"\n")
            


    # When it is completed, write the number of FPS in a separate file

    with open(os.path.join(ids_path.split("ids/")[0], "FPS.txt"), 'w') as FPS_file:
        FPS_file.write(str(FPS))



for char_size in Char_sizes:
    Char_path = f"/home/{username}/Documents/GitHub/Tese/runs/detect/PT_LP_Characters_{char_size}/weights/best.pt"
    Char = YOLO(Char_path)

    for lp_size in LP_sizes:
        LPs_path = f"/home/{username}/Documents/GitHub/Tese/runs/detect/License_Plates_1280_{lp_size}/weights/best.pt"
        

        for info in videos:
            LPs = YOLO(LPs_path)
            video, fps, skip_first_seconds, process_until_seconds = info
            print(video)

            # Open the video file
            video_path = f"{first_path}/Tese/datasets/Videos/"
            cap = cv2.VideoCapture(video_path + video)

            # Define path for predictions
            resolution = video.split(".MOV")[0]
            output_dir = f"/home/{username}/Desktop/Results_LPDet+OCR/Resolutions_test/NOcardet/{resolution}_{char_size}_{lp_size}/ids/"

            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)


            # Loop through the video frames
            n_frame = 0

            while cap.isOpened() and n_video > skip:
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

                                if not lp_img.shape[0] > lp_img.shape[1] and not lp_img.shape[0]/frame.shape[0] < min_height/frame.shape[0] and not lp_img.shape[1]/frame.shape[1] < min_width/frame.shape[1]:
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
                        #cv2.imshow("YOLOv8 Tracking", frame)


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
                    print(FPS, "\n")
                    # Get the time at which the recording started
                    #time_str = video.split('_')[1].split('.')[0]
                    #time_init = int(time_str[0:2])*3600 + int(time_str[2:4])*60 + int(time_str[4:6]) + float(time_str[6:9])/1000
                    organize_ids(output_dir, FPS)#, time_init)
                    break

            # Release the video capture object and close the display window
            cap.release()
            cv2.destroyAllWindows()
            n_video+=1

