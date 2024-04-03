from ultralytics import YOLO

model = YOLO("/home/santilm/Documents/GitHub/Tese/runs/detect/PT_LP_Characters_m/weights/best.pt")

model.val(data = "/home/santilm/Desktop/Tese/datasets/PT_LP_Characters/PT_LP_Characters_val.yaml")