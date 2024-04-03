from ultralytics import YOLO

model = YOLO("/home/santilm/Documents/GitHub/Tese/runs/detect/License_Plates_1280_x/weights/best.pt")

metrics = model.val(data = "/home/santilm/Desktop/Tese/datasets/License_Plates/License_Plates_val.yaml")

print(metrics.box)
