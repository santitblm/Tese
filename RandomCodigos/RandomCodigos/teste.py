#stra = 'olaghjgaaaa'
#print(stra[-7:-1])

#import numpy as np
#import cv2
#cv2.imshow("none", np.zeros(10))
#key = cv2.waitKey(0)
#print(key)
#n = 0
#for i in range(6):
#    print(i, n)
#    n+=3
import os
def organize_ids(ids_path):#, FPS):

    max_line = None
    max_count = 0
    # Iterate through files in the directory
    #for filename in os.listdir(ids_path):
    n = 0
    for i in range(len(os.listdir(ids_path))):
        filename = f'{i+n}.txt'
        file_path = os.path.join(ids_path, filename)
        while not os.path.isfile(file_path):
            n+=1
            filename = f'{i+n}.txt'
            file_path = os.path.join(ids_path, filename)
        print(file_path)


        predictions_path = os.path.join(ids_path.split("ids/")[0], "predictions.txt")
        # Read the file and count unique lines
        line_counts = {}
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line in line_counts:
                    line_counts[line] += 1
                else:
                    line_counts[line] = 1
        
        # Write unique lines and counts back to the file
        with open(file_path, 'w') as file:
            max_count = 0
            for line, count in line_counts.items():
                file.write(f"{line} {count}\n")
                # Update max_line if necessary
                if count > max_count:
                    max_line = line
                    max_count = count

        # Write the line with the maximum count to predictions.txt
        if max_line is not None:
            with open(predictions_path, 'a') as predictions_file:
                predictions_file.write(max_line + "\n")

    # When it is completed, write the number of FPS in the last line

    #with open(os.path.join(ids_path.split("ids/")[0], "FPS.txt"), 'w') as FPS_file:
    #    FPS_file.write(str(FPS))

    return predictions_path

#video = "20221026_125944.MOV"
#video = "20240329_125220.MOV"
#video = "20240329_124851.MOV"
video = "20240329_125219.MOV"
output_dir = f"/home/santilm/Desktop/Results_LPDet+OCR/{video}/ids/"


organize_ids(output_dir)#, FPS)

'''
def compare_results(ground_truth, predicted):
    def read_lines(filename):
        with open(filename, 'r') as file:
            return set(file.read().splitlines())

    def write_lines(filename, lines):
        with open(filename, 'w') as file:
            file.write('\n'.join(lines))

    lines_file1 = read_lines(ground_truth)
    lines_file2 = read_lines(predicted)
    
    new_lines_file1 = lines_file1 - lines_file2
    new_lines_file2 = lines_file2 - lines_file1
    new_file1 = predicted + "1.txt"
    new_file2 = predicted + "2.txt"
    write_lines(new_file1, new_lines_file1)
    write_lines(new_file2, new_lines_file2)

    return


video  = "20240209_151447.mp4"

ground_truth = f"/home/santilm/Desktop/GroundTruth_LPDet+OCR/{video}.txt" 
predicted = f"/home/santilm/Desktop/Results_LPDet+OCR/{video}/ids/results.txt"

compare_results(ground_truth, predicted)


def calculate_metrics(ground_truth_file, predictions_file):
    with open(ground_truth_file, 'r') as gt_file, open(predictions_file, 'r') as pred_file:
        gt_lines = set(gt_file.read().splitlines())
        pred_lines = set(pred_file.read().splitlines())

    TP = len(gt_lines.intersection(pred_lines))
    FP = len(pred_lines - gt_lines)
    FN = len(gt_lines - pred_lines)
    print(TP, FP, FN)
    precision = TP / (TP + FP) if TP + FP != 0 else 0
    recall = TP / (TP + FN) if TP + FN != 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall != 0 else 0

    return precision, recall, f1_score

video  = "20240209_151447.mp4"

ground_truth = f"/home/santilm/Desktop/GroundTruth_LPDet+OCR/{video}.txt" 
predicted = f"/home/santilm/Desktop/Results_LPDet+OCR/{video}/ids/results.txt"

#precision, recall, f1_score = calculate_metrics(ground_truth, predicted)
#print(f"{precision}, {recall}, {f1_score}")
'''