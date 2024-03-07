from ultralytics import YOLO
import cv2
import os

# Iterate through a folder of images
LPs_path = "runs/detect/yolov8n_200e_12804/weights/best.pt"
LPs = YOLO(LPs_path)
images_path = "datasets/LPs/train/images/"
labels_path = "datasets/LPs/train/labels/"

for filename in os.listdir(images_path):
    if filename.endswith(('.jpg', '.jpeg', '.png', '.bmp', '.gif')):
        # Read the image using OpenCV
        img_path = os.path.join(images_path, filename)
        frame = cv2.imread(img_path)
        # Run YOLOv8 tracking on the frame, persisting tracks between frames
        LP_results = LPs(frame, verbose = False)
        LP_data = LP_results[0].boxes.data
        boxes_with_labels = LP_data.tolist()
        if len(boxes_with_labels) > 0:
            boxes = LP_results[0].boxes.xywhn

            for box in boxes:
                x, y, w, h = box
                # Open the corresponding txt file and write the label
                with open(os.path.join(labels_path, filename[:-4] + ".txt"), "w") as f:
                    f.write(f"0 {x} {y} {w} {h}\n")
                    print(filename)
        else:
            # Open the corresponding txt file and write the label
            with open(os.path.join(labels_path, filename[:-4] + ".txt"), "w") as f:
                f.write("")
                print(filename)

            
