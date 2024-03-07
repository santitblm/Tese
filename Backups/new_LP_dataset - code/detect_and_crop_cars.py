from ultralytics import YOLO
import cv2
import random
import os

# Load the YOLOv8 model
model = YOLO('yolov8n.pt')
LPs_path = "runs/detect/yolov8n_200e_12804/weights/best.pt"
LPs = YOLO(LPs_path)

# Open the video file
#video_path = "datasets/Videos/VID-20230602-WA0010.mp4"
#cap = cv2.VideoCapture(video_path)
folder_path = "datasets/Videos/Tese2/"

n = 5130
#while cap.isOpened():
    # Read a frame from the video
#    success, frame = cap.read()

#    if success:

for filename in os.listdir(folder_path):

    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
        # Read the image using OpenCV
        img_path = os.path.join(folder_path, filename)
        frame = cv2.imread(img_path)
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        results = model.track(frame, persist=True, classes = [2, 3, 5, 7], verbose = False)
        vehicle_data = results[0].boxes.data
        boxes_with_labels = vehicle_data.tolist()
        if results[0].boxes.id is not None:
            # Get the boxes and track IDs
            boxes = results[0].boxes.xyxy
            # 
            for box in boxes:
                
                x1, y1, x2, y2 = box
                car_img = frame[int(y1):int(y2), int(x1):int(x2)]
                LP_results = LPs(car_img, verbose = False)
                LP_data = LP_results[0].boxes.data
                boxes_with_labels = LP_data.tolist()
                if len(boxes_with_labels) > 0:
                    if random.random() < 0.2:
                        print(n)
                        cv2.imwrite(f"datasets/LPs/train/images/{n}.jpg", car_img)
                        n+=1
                elif random.random() < 0.01:
                    print(n)
                    cv2.imwrite(f"datasets/LPs/train/images/{n}.jpg", car_img)
                    n+=1
#    else:
        # Break the loop if the end of the video is reached
#        break

# Release the video capture object and close the display window
#cap.release()
