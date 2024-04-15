from ultralytics import YOLO
import os
import cv2
import numpy as np

import os
import cv2
import numpy as np

def calculate_iou(gt_box, pred_box):
    """
    Calculate intersection over union (IoU) between two bounding boxes.

    Args:
    - gt_box: Ground truth bounding box coordinates in the format [xt1, yt1, xt2, yt2]
    - pred_box: Predicted bounding box coordinates in the format [xp1, yp1, xp2, yp2]

    Returns:
    - iou: Intersection over union (IoU) score
    """

    # Coordinates of intersection rectangle
    x1 = max(gt_box[0], pred_box[0])
    y1 = max(gt_box[1], pred_box[1])
    x2 = min(gt_box[2], pred_box[2])
    y2 = min(gt_box[3], pred_box[3])

    # Calculate area of intersection rectangle
    intersection_area = max(0, x2 - x1 + 1) * max(0, y2 - y1 + 1)

    # Calculate area of both bounding boxes
    gt_area = (gt_box[2] - gt_box[0] + 1) * (gt_box[3] - gt_box[1] + 1)
    pred_area = (pred_box[2] - pred_box[0] + 1) * (pred_box[3] - pred_box[1] + 1)

    # Calculate intersection over union
    iou = intersection_area / float(gt_area + pred_area - intersection_area)

    return iou

def calculate_ap(gt_boxes, pred_boxes, iou_threshold=0.5):
    """
    Calculate Average Precision (AP) for a single class.

    Args:
    - gt_boxes: Ground truth bounding boxes for a single class in the format [[xt1, yt1, xt2, yt2], ...]
    - pred_boxes: Predicted bounding boxes for a single class in the format [[xp1, yp1, xp2, yp2, confidence], ...]
    - iou_threshold: IoU threshold for considering a detection as correct

    Returns:
    - ap: Average Precision (AP) score
    """

    # Sort predictions by confidence score in descending order
    pred_boxes.sort(key=lambda x: x[4], reverse=True)

    tp = np.zeros(len(pred_boxes))
    fp = np.zeros(len(pred_boxes))
    gt_matched = np.zeros(len(gt_boxes))

    for i, pred_box in enumerate(pred_boxes):
        for j, gt_box in enumerate(gt_boxes):
            iou = calculate_iou(gt_box, pred_box[:4])
            if iou >= iou_threshold and not gt_matched[j]:
                tp[i] = 1
                gt_matched[j] = 1
                break
        else:
            fp[i] = 1

    # Calculate precision and recall
    tp_cumsum = np.cumsum(tp)
    fp_cumsum = np.cumsum(fp)
    recall = tp_cumsum / len(gt_boxes)
    precision = tp_cumsum / (tp_cumsum + fp_cumsum)

    # Calculate Average Precision (AP)
    ap = 0
    for i in range(len(recall) - 1):
        ap += (recall[i+1] - recall[i]) * precision[i+1]

    return ap

def calculate_mAP(gt_data, pred_data, num_classes, iou_threshold=0.5):
    """
    Calculate mean Average Precision (mAP) across multiple classes.

    Args:
    - gt_data: Ground truth data in the format {class_id: [[xt1, yt1, xt2, yt2], ...], ...}
    - pred_data: Predicted data in the format {class_id: [[xp1, yp1, xp2, yp2, confidence], ...], ...}
    - num_classes: Number of classes
    - iou_threshold: IoU threshold for considering a detection as correct

    Returns:
    - mAP: Mean Average Precision (mAP) score
    """

    ap_sum = 0

    for class_id in range(num_classes):
        if class_id not in gt_data or class_id not in pred_data:
            continue

        gt_boxes = gt_data[class_id]
        pred_boxes = pred_data[class_id]

        ap = calculate_ap(gt_boxes, pred_boxes, iou_threshold)
        ap_sum += ap

    mAP = ap_sum / num_classes

    return mAP

if __name__ == "__main__":
    images_folder = "C:/Users/Santi LM/Github/Tese/datasets/License_Plates/test/images/"
    labels_folder = "C:/Users/Santi LM/Github/Tese/datasets/License_Plates/test/labels/"

    gt_data = {}
    pred_data = {}

    # Iterate through each image in the images folder
    for image_filename in os.listdir(images_folder):
        if image_filename.endswith(('.jpg', '.jpeg', '.png')):
            image_path = os.path.join(images_folder, image_filename)

            # Get the corresponding text file with bounding box information
            txt_filename = os.path.splitext(image_filename)[0] + '.txt'
            txt_path = os.path.join(labels_folder, txt_filename)

            # Check if the corresponding text file exists
            if os.path.isfile(txt_path):
                # Read the image
                image = cv2.imread(image_path)
                results = model(image, verbose=False)
                data = results[0].boxes.data
                boxes = data.tolist()

                # Read the bounding box information from the text file
                with open(txt_path, 'r') as file:
                    lines = file.readlines()

                gt_boxes = []
                for line in lines:
                    values = line.split()
                    class_id = int(values[0])
                    x_center = float(values[1])
                    y_center = float(values[2])
                    width = float(values[3])
                    height = float(values[4])

                    # Calculate true box coordinates
                    xt1 = int((x_center - width / 2) * image.shape[1])
                    yt1 = int((y_center - height / 2) * image.shape[0])
                    xt2 = int((x_center + width / 2) * image.shape[1])
                    yt2 = int((y_center + height / 2) * image.shape[0])

                    gt_boxes.append([xt1, yt1, xt2, yt2])

                # Assuming class_id is 0 for simplicity
                gt_data[0] = gt_boxes
                pred_data[0] = boxes

    num_classes = 1  # Assuming there's only one class
    mAP = calculate_mAP(gt_data, pred_data, num_classes)
    print("mAP:", mAP)


