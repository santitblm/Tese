from ultralytics import YOLO

LPs = YOLO("runs/detect/yolov8n_200e_12804/weights/best.pt")
source = "datasets/20221026_120014.MOV"
results = LPs.track(source, show = True)