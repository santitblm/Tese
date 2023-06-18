import cv2

video_path = "C:/Users/Vastingood/Downloads/20230520_145807.mp4"  # Replace with your video file path
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error opening video file")

frame_count = 0
while cap.isOpened():
    ret, frame = cap.read()
    
    if ret:
        frame_path = f"frame_{frame_count}.jpg"  # Replace with your desired output path and filename
        cv2.imwrite(frame_path, frame)
        
        frame_count += 1
        print(frame_count)
    else:
        break

cap.release()
cv2.destroyAllWindows()