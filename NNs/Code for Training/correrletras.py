from ultralytics import YOLO
 
# Load the model.
model = YOLO('yolov8m.pt')
 
# Training.
results = model.train(
   data='datasets/PT_LP_Characters/PT_LP_Characters.yaml',
   imgsz=384,
   epochs=80,
   batch=16,
   patience=5,
   close_mosaic = 0,
   name='LPChar_80e_384_5p_closemosaic',
)
