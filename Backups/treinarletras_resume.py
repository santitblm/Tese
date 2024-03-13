from ultralytics import YOLO
 
# Load the model.
model = YOLO('/home/planeamusafrente/Documents/GitHub/Tese/runs/detect/LPCharFinal_x3/weights/last.pt')

# Training.
results = model.train(
    data='/home/planeamusafrente/Desktop/SANTI/datasets/PT_LP_Characters/PT_LP_Characters.yaml',
    imgsz=320,
    epochs=500,
    batch=32,
    name='LPCharFinal_x3',
    patience=50,
    close_mosaic = 150,
    resume = True
)
