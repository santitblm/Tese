import cv2
import os
from ultralytics import YOLO
import time as timer
import numpy as np

#####################################################################################################
class_labels = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"
min_height = 23/1080
min_width = 45/1920
n_video = 1
#####################################################################################################

#username , first_path = "planeamusafrente", "/home/planeamusafrente/Desktop/SANTI"
username, first_path = "santilm", "/home/santilm/Desktop"

Char_sizes = ["l", "x"]
LP_sizes = ["s", "l"]

skip = 24

# Open the video file
video_path = f"{first_path}/Tese/datasets/Videos/"
#videos = [["20240329_124851.MOV", "1st1080p30"], ["20240329_124852.MOV", "1st4K25"], ["20240329_124855.MOV", "1st27K30"], ["20240329_124859.MOV", "1st1080p60"], ["20240329_125220.MOV", "2nd1080p30"], ["20240329_125219.MOV", "2nd4K25"], ["20240329_125225.MOV", "2nd27K30"], ["20240329_125228.MOV", "2nd1080p60"]]
videos = ["3rd1080p30.MOV", "3rd1080p60.MOV", "3rd27K30.MOV", "3rd4K25.MOV", "4th1080p30.MOV", "4th1080p60.MOV", "4th27K30.MOV", "4th4K25.MOV", "5th1080p30.MOV", "5th1080p60.MOV", "5th27K30.MOV", "5th4K25.MOV"]


def check_LP(box, frame, annotated_frame, seg_mask):
    result_strings = []
    X1, Y1, X2, Y2 = map(int, box)

    cv2.rectangle(annotated_frame, (X1, Y1), (X2, Y2), (0, 255, 0), 2)
    pol_points = np.array(seg_mask.xy, dtype = np.int32)
    # Paint the pixels outside the car black
    mask = np.zeros_like(frame)
    cv2.fillPoly(mask, [pol_points], (255, 255, 255))
    result = cv2.bitwise_and(frame, mask)

    car_img = result[Y1:Y2, X1:X2]
    LP_results = LPs(car_img, verbose = False)
    LP_data = LP_results[0].boxes.data
    boxes_with_labels = LP_data.tolist()
    if len(boxes_with_labels) > 0:
        for box in boxes_with_labels:
            x1, y1, x2, y2 = map(int, box[:4])
            cv2.rectangle(annotated_frame, (X1+x1, Y1+y1), (X1+x2, Y1+y2), (0, 255, 255), 1)
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
                if 8 > len(result_string) > 5:
                    text = result_string
                    text_x = x1+X1
                    text_y = Y1+y1 - 5
                    # Draw the text
                    cv2.putText(annotated_frame, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 3)
                    result_strings.append(result_string)
    return result_strings, annotated_frame



for char_size in Char_sizes:
    Char_path = f"/home/{username}/Documents/GitHub/Tese/runs/detect/PT_LP_Characters_{char_size}/weights/best.pt"
    Char = YOLO(Char_path)

    for lp_size in LP_sizes:
        LPs_path = f"/home/{username}/Documents/GitHub/Tese/runs/detect/LP_fromCars_480_{lp_size}/weights/best.pt"
        LPs = YOLO(LPs_path)

        for video in videos:
            cap = cv2.VideoCapture(video_path + video)
            resolution = video.split(".MOV")[0]
            #output_dir = f"/home/{username}/Desktop/Results_LPDet+OCR/CarDetect/{resolution}_{char_size}_{lp_size}/ids/"
            #if not os.path.isdir(output_dir):
            #    os.makedirs(output_dir)

            model = YOLO('yolov8x-seg.pt')

            n_frame = 0
            starting_time = timer.time()

            while cap.isOpened() and n_video > skip:
                # Read a frame from the video
                success, frame = cap.read()

                if success:
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
                        #for box, track_id, seg_mask in zip(boxes, track_ids, seg_masks):
                            #strings, annotated_frame = check_LP(box, frame, annotated_frame, seg_mask)
                            #for string in strings:
                            #    text_file_name = os.path.join(output_dir, f"{track_id}.txt")
                            #    with open(text_file_name, "a") as text_file:
                                    #text_file.write(string + " " + time_str + "\n")
                            #        text_file.write(string + "\n")


                    # Display the annotated frame
                    cv2.imshow("YOLOv8 Tracking", annotated_frame)
                    n_frame += 1

                    # Break the loop if 'q' is pressed
                    if cv2.waitKey(1) & 0xFF == ord("q"):
                        break
                
            
                else:
                    # Break the loop if the end of the video is reached
                    print("End of video")
                    end_time = timer.time()
                    print(n_frame/(end_time-starting_time))
                    #print(output_dir, "\n")
                    break
        
            n_video += 1
            cap.release()
            cv2.destroyAllWindows()
