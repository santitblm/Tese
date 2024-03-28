from ultralytics import YOLO

size = "n"

model = YOLO(f"/home/santilm/Documents/GitHub/Tese/runs/detect/LP_fromCars_480_{size}/weights/best.pt")

model.val(data = "/home/santilm/Desktop/Tese/datasets/LPs_fromCars/LPs_fromCars_val.yaml", project='TestValResults/LPs_fromCars', name=f'LPs_fromCars_{size}')