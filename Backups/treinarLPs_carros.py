from ultralytics import YOLO
 
# Load the model.
sizes = ["n", "s"]
imgsize = 480
for size in sizes:
   model = YOLO(f'yolov8{size}.pt')
   # Training.
   results = model.train(
      data='datasets/LPs_fromCars/LPs_Cars.yaml',
      imgsz=imgsize,
      epochs=200,
      batch=32,
      name=f'LP_fromCars_{imgsize}_{size}',
      patience = 50,
      close_mosaic = 100
   )

# Make sure you are in the Tese directory (not Github)