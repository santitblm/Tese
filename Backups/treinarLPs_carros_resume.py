from ultralytics import YOLO

model = YOLO('/home/santilm/Desktop/Tese/runs/detect/LP_Cars_s')
# Training.
results = model.train(
   data='datasets/LPs_Cars/LPs_Cars.yaml',
   imgsz=640,
   epochs=200,
   batch=16,
   name='LP_Cars_640_s',
   patience = 20,
   close_mosaic = 80,
   resume = True
)

# TODO Make sure you are in the Tese directory (not Github)
