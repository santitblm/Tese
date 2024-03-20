from ultralytics import YOLO
import cv2
import random
import os

# Load the YOLOv8 model
model = YOLO('yolov8x.pt')

# Define paths
images_path = "/home/santilm/Desktop/Tese/datasets/License_Plates/test/images"
labels_path = "/home/santilm/Desktop/Tese/datasets/License_Plates/test/labels"

new_images = "/home/santilm/Desktop/Tese/datasets/LPs_fromCars/test/images"
new_labels = "/home/santilm/Desktop/Tese/datasets/LPs_fromCars/test/labels"

#images_path = "C:/Users/Santi LM/Documents/GitHub/Backup_Linux/License_Plates/train/images/"
#labels_path = "C:/Users/Santi LM/Documents/GitHub/Backup_Linux/License_Plates/train/labels/"

#new_images = "C:/Users/Santi LM/Documents/GitHub/Backup_Linux/LPs_Cars/train/images/"
#new_labels = "C:/Users/Santi LM/Documents/GitHub/Backup_Linux/LPs_Cars/train/labels/"



n = 0
#while cap.isOpened():
    # Read a frame from the video
#    success, frame = cap.read()

#    if success:

for filename in os.listdir(images_path):
    try:
        if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
            # Read the image using OpenCV
            img_path = os.path.join(images_path, filename)
            frame = cv2.imread(img_path)
            imgsz = frame.shape

            # Run YOLOv8 tracking on the frame, persisting tracks between frames
            results = model(frame, classes = [2, 3, 5, 7], verbose = False)
            vehicle_data = results[0].boxes.data
            boxes_with_labels = vehicle_data.tolist()

            if results[0].boxes is not None:
                
                with open(os.path.join(labels_path, filename[:-4] + ".txt"), "r") as f:
                    lines = f.readlines()

                boxes = results[0].boxes.xyxy

                for box in boxes:
                    n+=1

                    x1, y1, x2, y2 = box
                    car_img = frame[int(y1):int(y2), int(x1):int(x2)]
                    cv2.imwrite(os.path.join(new_images, f"test_{n}.jpg"), car_img)
                    
                    if len(lines) == 0:
                        with open(os.path.join(new_labels, f"test_{n}.txt"), "w") as f: # Write an empty text file in case no objects are present in the image
                            f.write(f"")
                    else:
                        with open(os.path.join(new_labels, f"test_{n}.txt"), "w") as f:
                            for line in lines:
                                values = line.split()
                                label = int(values[0])
                                x_center = float(values[1]) * imgsz[1]
                                y_center = float(values[2]) * imgsz[0]
                                width    = float(values[3]) * imgsz[1]
                                height   = float(values[4]) * imgsz[0]

                                if x1 <= x_center <= x2 and y1 <= y_center <= y2: # Object present image, write label accordingly
                                    car_width = x2-x1
                                    car_height = y2-y1
                                    new_width_n = width / car_width
                                    new_height_n = height / car_height
                                    new_x_center_n = (x_center-x1) / car_width
                                    new_y_center_n = (y_center-y1) / car_height
                                    f.write(f"{label} {new_x_center_n} {new_y_center_n } {new_width_n} {new_height_n}\n")
    except:
        continue


                



#    else:
        # Break the loop if the end of the video is reached
#        break

# Release the video capture object and close the display window
#cap.release()
