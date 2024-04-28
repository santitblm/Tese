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
    new_file1 = predicted + "FN.txt"
    new_file2 = predicted + "FP.txt"
    write_lines(new_file1, new_lines_file1)
    write_lines(new_file2, new_lines_file2)

    return


def calculate_metrics(ground_truth_path, predictions_path, Final_Results_path):

    for folder in os.listdir(predictions_path):
        if folder.startswith("1st"):
            TP = 0
            FP = 0
            FN = 0
            FPS_list = []
            #compare_results(ground_truth_file, predictions_file)

            for ground_truth_file in os.listdir(ground_truth_path):
                ordinal = ground_truth_file.split(".txt")[0]
                
                resolution_model = folder.split("1st")[1]
                video_folder = ordinal + resolution_model
                predictions_file = os.path.join(predictions_path, video_folder, "predictions.txt")
                
                with open(os.path.join(ground_truth_path, ground_truth_file), 'r') as gt_file, open(predictions_file, 'r') as pred_file:
                    gt_lines = set(gt_file.read().splitlines())
                    pred_lines = set(pred_file.read().splitlines())

                TP += len(gt_lines.intersection(pred_lines))
                FP += len(pred_lines - gt_lines)
                FN += len(gt_lines - pred_lines)
                fps_file = os.path.join(predictions_path, video_folder, "FPS.txt")
                with open(fps_file, 'r') as fps_f:
                    fps = fps_f.readlines()[0]
                FPS_list.append(float(fps))
                #print(TP, FP, FN)

            precision = TP / (TP + FP) if TP + FP != 0 else 0
            recall = TP / (TP + FN) if TP + FN != 0 else 0
            f1_score = 2 * (precision * recall) / (precision + recall) if precision + recall != 0 else 0
            FPS = sum(FPS_list)/len(FPS_list)
            results = f"Precision: {precision}, Recall: {recall}, F1 Score: {f1_score}. FPS: {FPS}"
            print(results)

            with open(os.path.join(Final_Results_path, f"{resolution_model}.txt"), 'w') as results_file:
                results_file.write(f"{precision}\n{recall}\n{f1_score}\n{FPS}")

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

#ground_truth_path = "/home/santilm/Desktop/GroundTruth_LPDet+OCR/resol_test/" 

#predictions_path = "/home/santilm/Desktop/Results_LPDet+OCR/Resolutions_test/NOCarDetect/"
#Final_Results_path = "/home/santilm/Desktop/Resultados/Resolutions_test/NOcardet/"
#predictions_path = "/home/santilm/Desktop/Results_LPDet+OCR/Resolutions_test/CarDetect/"
#Final_Results_path = "/home/santilm/Desktop/Resultados/Resolutions_test/CarDet/"
#predictions_path = "/home/santilm/Desktop/Results_LPDet+OCR/Resolutions_test/CarDetect - planeamus/CarDetect/"
#Final_Results_path = "/home/santilm/Desktop/Resultados/Resolutions_test/CarDet/planeamus/"

#predictions_path = "/home/santilm/Desktop/Results_LPDet+OCR/Resolutions_test/NOCarDetect/"
#Final_Results_path = "/home/santilm/Desktop/Resultados/Resolutions_test/NOcardet/"
username = "planeamusafrente"
#username = "santilm"

ground_truth_path = f"/home/{username}/Desktop/GroundTruth_LPDet+OCR/resol_test/" 
predictions_path = f"/home/{username}/Desktop/Results_LPDet+OCR/Resolutions_test/CarDetect/"
Final_Results_path = f"/home/{username}/Desktop/Resultados/Resolutions_test/CarDet/"
predictions_path_planeamus = f"/home/{username}/Desktop/Results_LPDet+OCR/Resolutions_test/CarDetect/CarDetect - planeamus/CarDetect/"
Final_Results_path_planeamus = f"/home/{username}/Desktop/Resultados/Resolutions_test/CarDet/planeamus"

#if not os.path.isdir(Final_Results_path):
#    os.makedirs(Final_Results_path)

#for folder in os.listdir(predictions_path):
#    ids_path = os.path.join(predictions_path, folder, "ids/")
#    organize_ids(ids_path)


calculate_metrics(ground_truth_path, predictions_path, Final_Results_path)
#calculate_metrics(ground_truth_path, predictions_path_planeamus, Final_Results_path_planeamus)

#for folder in os.listdir(predictions_path):
#folder = "1st27K30_l_s"
#predicted = os.path.join(predictions_path, folder, "predictions.txt")
#ground_truth = os.path.join(ground_truth_path, f"{folder[:3]}.txt")
#compare_results(ground_truth, predicted)


