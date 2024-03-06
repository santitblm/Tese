from ultralytics import YOLO
 
# Load the model.
models = ["x"]

for size in models:
   model = YOLO(f'yolov8{size}.pt')
   
   # Training.
   results = model.train(
      data='/home/planeamusafrente/Desktop/SANTI/datasets/PT_LP_Characters/PT_LP_Characters.yaml',
      imgsz=320,
      epochs=500,
      batch=32,
      name=f'LPCharFinal_{size}',
      patience=50,
      close_mosaic = 150
   )
