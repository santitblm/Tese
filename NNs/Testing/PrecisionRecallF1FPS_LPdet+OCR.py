import os

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


def calculate_metrics(ground_truth_path, predictions_path):

    TP = 0
    FP = 0
    FN = 0
    FPS = []

    for filename in os.listdir(ground_truth_path):
        ground_truth_file = os.path.join(ground_truth_path, filename)
        predictions_file = os.path.join(predictions_path, filename.split(".txt")[0], "predictions.txt")
        #compare_results(ground_truth_file, predictions_file)
        with open(ground_truth_file, 'r') as gt_file, open(predictions_file, 'r') as pred_file:
            gt_lines = set(gt_file.read().splitlines())
            pred_lines = set(pred_file.read().splitlines())

        TP += len(gt_lines.intersection(pred_lines))
        FP += len(pred_lines - gt_lines)
        FN += len(gt_lines - pred_lines)
        #print(TP, FP, FN)
        FPS_filename = os.path.join(predictions_path, filename.split(".txt")[0], "FPS.txt")
        with open(FPS_filename, 'r') as FPS_file:
            value = FPS_file.readlines()
            #print(type(value), type(FPS))
            FPS.append(value[0])

    precision = TP / (TP + FP) if TP + FP != 0 else 0
    recall = TP / (TP + FN) if TP + FN != 0 else 0
    f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall != 0 else 0

    FPS_float = [float(i) for i in FPS]
    fps = sum(FPS_float) / len(FPS_float) 

    return precision, recall, f1_score, fps


ground_truth_path = f"/home/santilm/Desktop/GroundTruth_LPDet+OCR/" 
predictions_path = f"/home/santilm/Desktop/Results_LPDet+OCR/"

precision, recall, f1_score, fps = calculate_metrics(ground_truth_path, predictions_path)#, fps
results = f"Precision: {precision}, Recall: {recall}, F1 Score: {f1_score}, FPS: {fps}"
print(results)
with open(os.path.join(predictions_path, "results.txt"), 'w') as results_file:
    results_file.write(results)




# The following code is to have a better understanding of what failed:
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


#video  = "20240209_151447.mp4"

#ground_truth = f"/home/santilm/Desktop/GroundTruth_LPDet+OCR/{video}.txt" 
#predicted = f"/home/santilm/Desktop/Results_LPDet+OCR/{video}/ids/results.txt"

#compare_results(ground_truth, predicted)
