from ultralytics import YOLO

#username, first_path = "santilm", "santilm/Desktop"
username, first_path = "planeamusafrente", "planeamusafrente/Desktop/SANTI"

model = YOLO(f"/home/{username}/Documents/GitHub/Tese/runs/detect/License_Plates_1280_x/weights/best.pt")

metrics = model.val(data = f"/home/{first_path}/Tese/datasets/License_Plates/License_Plates_val.yaml")

print(metrics.box)
