
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
points_to_cover_r1 = np.array([[1200, 1524], [130, 900], [0, 520], [0, 1524]], np.int32) #lado direito
points_to_cover_l1 = np.array([[1800, 1524], [2500, 950], [2704, 250], [2704, 1524]], np.int32) #lado esquerdo
points_to_cover_r2 = np.array([[1300, 1524], [200, 900], [0, 450], [0, 1524]], np.int32) #lado direito
points_to_cover_l2 = np.array([[1750, 1524], [2500, 900], [2704, 200], [2704, 1524]], np.int32) #lado esquerdo
points_to_cover_r3 = np.array([[1400, 1524], [300, 900], [0, 100], [0, 1524]], np.int32) #lado direito
points_to_cover_l3 = np.array([[1850, 1524], [2500, 900], [2704, 10], [2704, 1524]], np.int32) #lado esquerdo
points_to_cover_r4 = np.array([[1000, 1524], [150, 1000], [0, 500], [0, 1524]], np.int32) #lado direito
points_to_cover_l4 = np.array([[1850, 1524], [2500, 900], [2704, 10], [2704, 1524]], np.int32) #lado esquerdo
points_to_cover_l5 = np.array([[1800, 1524], [2500, 900], [2704, 200], [2704, 1524]], np.int32) #lado esquerdo
points_to_cover_r5 = np.array([[1200, 1524], [100, 950], [0, 680], [0, 1524]], np.int32) #lado direito
#####################################################################################################
# 2704x1524


#def check_LP(box, frame, annotated_frame, seg_mask):
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
                    #text = result_string

                    # Calculate the position for the text
                    #text_x = x1+X1
                    #text_y = Y1+y1 - 5# if Y1+y1 - 5 > 5 else Y1 + 20

                    # Draw the text
                    #cv2.putText(annotated_frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
    #return result_strings, annotated_frame
    return result_strings

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


LPs_path = f"/home/{username}/Documents/GitHub/Tese/runs/detect/LP_fromCars_480_s/weights/best.pt"
LPs = YOLO(LPs_path)
Char_path = f"/home/{username}/Documents/GitHub/Tese/runs/detect/PT_LP_Characters_x/weights/best.pt"
Char = YOLO(Char_path)


videos = [
            ["20240415_155432266.MOV", points_to_cover_r1, 0*60+62, 2*60+52, []],       # Ready
            ["20240415_155436900.MOV", points_to_cover_l1, 0*60+54, 2*60+47, [3281]],   # Ready
            ["20240415_164646933.MOV", points_to_cover_l2, 0*60+55, 2*60+41, []],       # Ready
            ["20240415_164648500.MOV", points_to_cover_r2, 0*60+57, 2*60+40, []],       # Ready
            ["20240416_124741800.MOV", points_to_cover_r3, 5*60+26, 7*60+20, []],       # Ready
            ["20240416_124743199.MOV", points_to_cover_l3, 5*60+25, 7*60+ 8, [10536]],  # Ready
            ["20240416_144931533.MOV", points_to_cover_r4, 1*60+24, 3*60+43, []],       # Ready
            ["20240416_144935000.MOV", points_to_cover_l4, 1*60+20, 3*60+32, []],       # Ready
            ["20240416_155400300.MOV", points_to_cover_r5, 1*60+18, 3*60+21, []],       # Ready
            ["20240416_155401733.MOV", points_to_cover_l5, 1*60+17, 3*60+15, [2685, 4335, 5333]],   # Ready
        ]

for info in videos:
    video, points_to_cover, skip_first_seconds, process_until_seconds, core_dumped = info
    print(video)
    # Load the YOLOv8 model
    model = YOLO('yolov8x-seg.pt')

    # Open the video file
    video_path = f"{first_path}/Tese/datasets/Videos/"
    cap = cv2.VideoCapture(video_path + video)

    # Define path for predictions
    output_dir = f"/home/{username}/Desktop/Results_LPDet+OCR/Final_Tese/WithCD/{video}/ids/"

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)


    # Loop through the video frames
    n_frame = 0

    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()
        #print(n_frame)
        if success:
            if process_until_seconds*fps > n_frame > skip_first_seconds*fps and n_frame not in core_dumped:    
                cv2.fillPoly(frame, pts = [points_to_cover], color=(0, 0, 0))
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

                    # Plot the tracks
                    for box, track_id, seg_mask in zip(boxes, track_ids, seg_masks):
                        #strings, annotated_frame = check_LP(box, frame, annotated_frame, seg_mask)
                        strings = check_LP(box, frame, seg_mask)
                        for string in strings:
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
