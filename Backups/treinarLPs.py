from ultralytics import YOLO
 
# Load the model.
model = YOLO('yolov8n.pt')
 
# Training.
results = model.train(
   data='datasets/License_Plates/License_Plate.yaml',
   imgsz=1280,
   epochs=200,
   batch=8,
   name='yolov8s_200e_1280',
   patience = 5
)