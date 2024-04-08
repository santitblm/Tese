from ultralytics import YOLO
import cv2
#username , first_path = "planeamusafrente", "/home/planeamusafrente/Desktop/SANTI"
username, first_path = "santilm", "/home/santilm/Desktop"

skip = 0

# Open the video file
video_path = f"{first_path}/Tese/datasets/Videos/3rd1080p30.MOV"


cap = cv2.VideoCapture(video_path)
            
model = YOLO('yolov8x-seg.pt')

results = model.track(video_path, show = True, verbose = False)

while False:# cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
    # Run YOLOv8 tracking on the frame, persisting tracks between frames
    
        results = model.track(frame, persist=True, classes = [2, 7], verbose = False, max_det = 6)#, show = True)
        annotated_frame = frame.copy()

        # Display the annotated frame
        cv2.imshow("YOLOv8 Tracking", annotated_frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
