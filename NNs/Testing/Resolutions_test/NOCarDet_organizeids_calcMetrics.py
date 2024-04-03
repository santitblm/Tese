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


def calculate_metrics(ground_truth_path, predictions_path, Final_Results_path):

    for folder in os.listdir(os.path.join(predictions_path, "1st/")):

        TP = 0
        FP = 0
        FN = 0
        #compare_results(ground_truth_file, predictions_file)

        for ground_truth_file in os.listdir(ground_truth_path):
            ordinal = ground_truth_file.split(".txt")[0]

            new_predictions_path = predictions_path.split("1st/")[0] + f"{ordinal}/"
            resolution = folder.split("1st")[1]
            video_folder = ordinal + resolution
            predictions_file = os.path.join(new_predictions_path, video_folder, "predictions.txt")
            
            with open(os.path.join(ground_truth_path, ground_truth_file), 'r') as gt_file, open(predictions_file, 'r') as pred_file:
                gt_lines = set(gt_file.read().splitlines())
                pred_lines = set(pred_file.read().splitlines())

            TP += len(gt_lines.intersection(pred_lines))
            FP += len(pred_lines - gt_lines)
            FN += len(gt_lines - pred_lines)
            #print(TP, FP, FN)

        precision = TP / (TP + FP) if TP + FP != 0 else 0
        recall = TP / (TP + FN) if TP + FN != 0 else 0
        f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall != 0 else 0

        results = f"Precision: {precision}, Recall: {recall}, F1 Score: {f1_score}"
        print(results)

        with open(os.path.join(Final_Results_path, f"{resolution}.txt"), 'w') as results_file:
            results_file.write(results)

def organize_ids(ids_path):
    # Iterate through files in the directory
    for filename in os.listdir(ids_path):

        file_path = os.path.join(ids_path, filename)

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

ground_truth_path = "/home/santilm/Desktop/GroundTruth_LPDet+OCR/resol_test/" 
predictions_path = "/home/santilm/Desktop/Results_LPDet+OCR/NOCarDetect/"
Final_Results_path = "/home/santilm/Desktop/Resultados/NO_CAR-DET/"

#for folder_ordinal in os.listdir(predictions_path):
##    for folder in os.listdir(os.path.join(predictions_path, folder_ordinal)):
#        ids_path = os.path.join(predictions_path, folder_ordinal, folder, "ids/")
#        organize_ids(ids_path)


calculate_metrics(ground_truth_path, predictions_path, Final_Results_path)

