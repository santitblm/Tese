from ultralytics import YOLO

imgsize = 1280

models = ["s", "n"]

for size in models: 
   # Load the model.
   model = YOLO(f'yolov8{size}.pt')
   
   # Training.
   results = model.train(
      data='/home/planeamusafrente/Desktop/SANTI/Tese/datasets/License_Plates/License_Plate.yaml',
      imgsz=1280,
      epochs=200,
      batch=16,
      name=f'License_Plates_{imgsize}_{size}',
      patience = 50,
      close_mosaic = 100
   )


models = ["l", "m"]

for size in models: 
   # Load the model.
   model = YOLO(f'yolov8{size}.pt')
   
   # Training.
   results = model.train(
      data='/home/planeamusafrente/Desktop/SANTI/Tese/datasets/License_Plates/License_Plate.yaml',
      imgsz=imgsize,
      epochs=300,
      batch=16,
      name=f'License_Plates_{imgsize}_{size}',
      patience = 50,
      close_mosaic = 150
   )
