import os
import cv2
from ultralytics import YOLO


precision = 0.95880695
recall = 0.8857478
F1 = 0.90001

string = f"{precision}\n{recall}\n{F1}"

print(string)