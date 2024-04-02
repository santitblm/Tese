from collections import defaultdict
import numpy as np
import cv2
import os
from ultralytics import YOLO
import time as timer

#####################################################################################################
class_labels = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"
target_width = 500
flag = False
min_height = 23
min_area = 1000
inval = 0 # variable to count invalid images
#points_to_cover = np.array([[0, 390], [1920, 1020], [1920, 1080], [0, 1080]], np.int32)#[[0, 1080], [0, 970], [1150, 530], [1920, 540], [1920, 1080]], np.int32)
#####################################################################################################

#username , first_path = "planeamusafrente", "/home/planeamusafrente/Desktop/SANTI"
username, first_path = "santilm", "/home/santilm/Desktop"

size = "m"


Char_path = f"/home/{username}/Documents/GitHub/Tese/runs/detect/PT_LP_Characters_{size}/weights/best.pt"
Char = YOLO(Char_path)

# Open the video file
video_path = f"{first_path}/Tese/datasets/Videos/"

#video  = "20240209_151447.mp4" #sem cobrir
#video = "20221026_141258.MOV" #lado esquerdo
#video = "20221026_125944.MOV" #lado direito
#ideo = "20221026_142307.MOV" #lado direito
#video = "20221026_151500.MOV" #lado direito
#video = "20230602_134058.mp4" 


# 1st resolution test videos
#video = ["20240329_124851.MOV", "1st1080p30"]
#video = ["20240329_124852.MOV", "1st4K25"]


videos = [["20240329_124851.MOV", "1st1080p30"], ["20240329_124852.MOV", "1st4K25"], ["20240329_124855.MOV", "1st27K30"], ["20240329_124859.MOV", "1st1080p60"], ["20240329_125220.MOV", "2nd1080p30"], ["20240329_125219.MOV", "2nd4K25"], ["20240329_125225.MOV", "2nd27K30"], ["20240329_125228.MOV", "2nd1080p60"]]

for video in videos:

    LPs_path = f"/home/{username}/Documents/GitHub/Tese/runs/detect/LP_fromCars_480_{size}/weights/best.pt"
    LPs = YOLO(LPs_path)
    cap = cv2.VideoCapture(video_path + video[0])

    # define paths for ground truth and predictions
    #ground_truth = f"/home/{username}/Desktop/GroundTruth_LPDet+OCR/{video}.txt" 
    output_dir = f"/home/{username}/Desktop/Results_LPDet+OCR/NOCarDetect/{video[1]}{size}/ids/"

    if not os.path.isdir(output_dir):
        os.makedirs(output_dir)

    # Get the initial time of the video from its filename
    #time_str = video.split('_')[1].split('.')[0]
    #time_init = int(time_str[0:2])*3600 + int(time_str[2:4])*60 + int(time_str[4:6])

    # Loop through the video frames
    n_frame = 0
    initial = timer.time()
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:

            result_strings = []
            LP_results = LPs.track(frame, persist = True, max_det = 6, verbose = False)
            #LP_data = LP_results[0].boxes.data
            #boxes_with_labels = LP_data.tolist()
            #if len(boxes_with_labels) > 0:

            if LP_results[0].boxes.id is not None:


                # Get the boxes and track IDs
                boxes = LP_results[0].boxes.xyxy.cpu()
                track_ids = LP_results[0].boxes.id.int().cpu().tolist()

                for box, track_id in zip(boxes, track_ids):

                    x1, y1, x2, y2 = map(int, box[:4])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 1)
                    lp_img = frame[y1:y2, x1:x2]

                    # Reject license plates that are too small or whose height is greater than width
                    if not lp_img.shape[0] > lp_img.shape[1] and not lp_img.shape[0] < min_height and not lp_img.shape[0] * lp_img.shape[1] < min_area:
                    #    
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
                    #    validity, _ = validate_string(result_string, sorted_confidences, sorted_boxes)
                        # Define the text to display (label and confidence)
                        if len(result_string) > 4:
                            text = result_string
                        #
                        #    # Calculate the position for the text
                            #text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
                            text_x = x1
                            text_y = y1 - 5 if y1 - 5 > 5 else y1 + 20

                            # Draw the text
                            cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

                        #print(validity, str)
                        #if validity:
                            result_strings.append(result_string)

                for string in result_strings:
                    text_file_name = os.path.join(output_dir, f"{track_id}.txt")
                #    time = time_init + n_frame/30
                #    time_str = f"{int(time)//3600:02d}:{int(time)%3600//60:02d}:{int(time)%60:02d}:{int((time - int(time))*1000):03d}"
                    with open(text_file_name, "a") as text_file:
                        text_file.write(string + "\n")#" " + time_str + "\n")
                    
            #annotated_frame = frame
            # Display the annotated frame
            cv2.imshow("YOLOv8 Tracking", frame)
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

    print(f"{round(n_frame/(timer.time() - initial), 2)} FPS")