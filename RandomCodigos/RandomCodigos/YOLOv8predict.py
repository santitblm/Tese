from ultralytics import YOLO
import cv2

model = YOLO('yolov8n.pt')
source = "C:/Users/Santi LM/Desktop/teste/vlcsnap-2023-06-02-10h50m29s408.png"
img = cv2.imread(source)
results = model(cv2.resize(img, (1280, 720)), show = True)
cv2.waitKey(0)
cv2.destroyAllWindows()