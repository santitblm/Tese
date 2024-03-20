from ultralytics import YOLO
#from RandomCodigos.data_augmentation.Synthetic_LPs import create_images
#from RandomCodigos.useful.separate_into_train_and_valid import separate
# Load the model.

#create_images()

#separate()

models = ["m"]

for size in models:
   #model = YOLO(f'/home/planeamusafrente/Documents/GitHub/Tese/runs/detect/LPCharFinal_l/weights/last.pt')
   model = YOLO(f"yolov8{size}.pt")
   # Training.
   results = model.train(
      data='/home/santilm/Desktop/Tese/datasets/PT_LP_Characters_ORIGINALS/PT_LP_Characters_ORIGINALS.yaml',
      imgsz=320,
      epochs=200,
      batch=32,
      name=f'PT_LP_Characters_ORIGINALS_{size}',
      patience=50,
      close_mosaic = 100
   )
