from ultralytics import YOLO

model = YOLO("/home/santilm/Documents/GitHub/Tese/runs/detect/LP_fromCars_480_m/weights/best.pt")

model.val(data = "/home/santilm/Desktop/Tese/datasets/LPs_fromCars/LPs_fromCars_val.yaml")