from ultralytics import YOLO
 
# Load the model.
models = ["l", "x"]

for size in models:
   model = YOLO(f'yolov8{size}.pt')
   
   # Training.
   results = model.train(
      data='datasets/PT_LP_Characters/PT_LP_Characters.yaml',
      imgsz=320,
      epochs=200,
      batch=24,
      name=f'LPCharFinal_{size}',
      patience=20,
      close_mosaic = 0
   )
