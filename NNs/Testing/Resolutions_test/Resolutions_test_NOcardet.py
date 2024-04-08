from collections import defaultdict
import numpy as np
import cv2
import os
from ultralytics import YOLO
import time as timer

#####################################################################################################
class_labels = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"
min_height = 23/1080
min_width = 45/1920
n_video = 1
#####################################################################################################

#username , first_path = "planeamusafrente", "/home/planeamusafrente/Desktop/SANTI"
username, first_path = "santilm", "/home/santilm/Desktop"

Char_sizes = ["l", "x"]
LP_sizes = ["x", "m"]

skip = 0

# Open the video file
video_path = f"{first_path}/Tese/datasets/Videos/"
#videos = [["20240329_124851.MOV", "1st1080p30"], ["20240329_124852.MOV", "1st4K25"], ["20240329_124855.MOV", "1st27K30"], ["20240329_124859.MOV", "1st1080p60"], ["20240329_125220.MOV", "2nd1080p30"], ["20240329_125219.MOV", "2nd4K25"], ["20240329_125225.MOV", "2nd27K30"], ["20240329_125228.MOV", "2nd1080p60"]]
videos = ["3rd1080p30.MOV", "3rd1080p60.MOV", "3rd27K30.MOV", "3rd4K25.MOV", "4th1080p30.MOV", "4th1080p60.MOV", "4th27K30.MOV", "4th4K25.MOV", "5th1080p30.MOV", "5th1080p60.MOV", "5th27K30.MOV", "5th4K25.MOV"]

for char_size in Char_sizes:
    Char_path = f"/home/{username}/Documents/GitHub/Tese/runs/detect/PT_LP_Characters_{char_size}/weights/best.pt"
    Char = YOLO(Char_path)

    for lp_size in LP_sizes:
        LPs_path = f"/home/{username}/Documents/GitHub/Tese/runs/detect/License_Plates_1280_{lp_size}/weights/best.pt"

        for video in videos:
            LPs = YOLO(LPs_path)
            cap = cv2.VideoCapture(video_path + video)
            resolution = video.split(".MOV")[0]

            output_dir = f"/home/{username}/Desktop/Results_LPDet+OCR/NOCarDetect/{resolution}_{char_size}_{lp_size}/ids/"
            if not os.path.isdir(output_dir):
                os.makedirs(output_dir)

            # Loop through the video frames
            n_frame = 0
            initial = timer.time()

            while cap.isOpened() and n_video > skip:
                # Read a frame from the video
                success, frame = cap.read()

                if success:

                    result_strings = []
                    LP_results = LPs.track(frame, persist = True, max_det = 6, verbose = False)

                    if LP_results[0].boxes.id is not None:
                        # Get the boxes and track IDs
                        boxes = LP_results[0].boxes.xyxy.cpu()
                        track_ids = LP_results[0].boxes.id.int().cpu().tolist()

                        for box, track_id in zip(boxes, track_ids):

                            x1, y1, x2, y2 = map(int, box[:4])
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 255), 1)
                            lp_img = frame[y1:y2, x1:x2]

                            # Reject license plates that are too small or whose height is greater than width
                            if not lp_img.shape[0] > lp_img.shape[1] and not lp_img.shape[0]/frame.shape[0] < min_height/frame.shape[0] and not lp_img.shape[1]/frame.shape[1] < min_width/frame.shape[1]:
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

                                # Define the text to display (label and confidence)
                                if 8 > len(result_string) > 5:
                                    text = result_string
                                
                                    # Calculate the position for the text
                                    text_x = x1
                                    text_y = y1 - 5 if y1 - 5 > 5 else y1 + 20

                                    # Draw the text
                                    cv2.putText(frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)

                                    result_strings.append(result_string)

                        for string in result_strings:
                            text_file_name = os.path.join(output_dir, f"{track_id}.txt")
                            with open(text_file_name, "a") as text_file:
                                text_file.write(string + "\n")#" " + time_str + "\n")

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
            n_video += 1
            print(f"{round(n_frame/(timer.time() - initial), 2)} FPS")