from ultralytics import YOLO
 
# Load the model.
model = YOLO('/home/planeamusafrente/Desktop/SANTI/runs/detect/LPCharFinal_x3/weights/last.pt')

# Training.
results = model.train(
    data='/home/planeamusafrente/Desktop/SANTI/datasets/PT_LP_Characters/PT_LP_Characters.yaml',
    imgsz=320,
    epochs=400,
    batch=32,
    name='LPCharFinal_x3',
    patience=20,
    close_mosaic = 100,
    resume = True,
    verbose = True
)
