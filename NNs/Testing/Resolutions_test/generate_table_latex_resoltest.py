import numpy as np
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

    for folder in os.listdir(predictions_path):

        TP = 0
        FP = 0
        FN = 0
        #compare_results(ground_truth_file, predictions_file)

        for ground_truth_file in os.listdir(ground_truth_path):
            ordinal = ground_truth_file.split(".txt")[0]

            new_predictions_path = predictions_path.split("1st/")[0] + f"{ordinal}/"
            video_folder = ordinal + folder.split("1st")[1]
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

        with open(os.path.join(new_predictions_path, video_folder, "results.txt"), 'w') as results_file:
            results_file.write(results)


Precision = np.zeros((4, 4))
Recall = np.zeros((4, 4))
F1 = np.zeros((4, 4))
print(F1)
print(f''' \\begin{{table}}[!htb]
   \\caption{{Results for the ALPR system \\textbf{{without}} car detection on various resolutions}}
   \\label{{tab:ALPR_QuestForOptimalResolution_NOcardet}}
   \\centering
   \\renewcommand{{\\arraystretch}}{{1.2}}
   \\begin{{tabular}}{{@{{}}ccrccccccc@{{}}}}
     \\toprule
       \\multicolumn{{2}}{{c}}{{Models (size)}}  && \\multicolumn{{3}}{{c}}{{1080p30 (\\%)}} & \\phantom{{abc}} & \\multicolumn{{3}}{{c}}{{1080p60 (\\%)}} \\\\
     \\cmidrule{{4-6}}
     \\cmidrule{{8-10}}
     \\cmidrule{{1-2}}
       Characters & LPs         &&  Precision        &  Recall        &  F1        &&  Precision        &  Recall        &  F1 \\\\
     \\midrule
       Large      & Medium      && {Precision[0][0]} & {Recall[0][0]} & {F1[0][0]} && {Precision[1][0]} & {Recall[1][0]} & {F1[1][0]} \\\\
       Large      & ExtraLarge  && {Precision[0][1]} & {Recall[0][1]} & {F1[0][1]} && {Precision[1][1]} & {Recall[1][1]} & {F1[1][1]} \\\\
       ExtraLarge & Medium      && {Precision[0][2]} & {Recall[0][2]} & {F1[0][2]} && {Precision[1][2]} & {Recall[1][2]} & {F1[1][2]} \\\\
       ExtraLarge & ExtraLarge  && {Precision[0][3]} & {Recall[0][3]} & {F1[0][3]} && {Precision[1][3]} & {Recall[1][3]} & {F1[1][3]} \\\\
    \\midrule
      \\multicolumn{{2}}{{c}}{{Models (size)}} && \\multicolumn{{3}}{{c}}{{2.7K30 (\\%)}} & \\phantom{{abc}} & \\multicolumn{{3}}{{c}}{{4K25 (\\%)}} \\\\
     \\cmidrule{{4-6}}
     \\cmidrule{{8-10}}
     \\cmidrule{{1-2}}
       Characters & LPs         &&  Precision        &  Recall        &  F1        &&  Precision        &  Recall        &  F1 \\\\
     \\midrule
       Large      & Medium      && {Precision[2][0]} & {Recall[2][0]} & {F1[2][0]} && {Precision[3][0]} & {Recall[3][0]} & {F1[3][0]} \\\\
       Large      & ExtraLarge  && {Precision[2][1]} & {Recall[2][1]} & {F1[2][1]} && {Precision[3][1]} & {Recall[3][1]} & {F1[3][1]} \\\\
       ExtraLarge & Medium      && {Precision[2][2]} & {Recall[2][2]} & {F1[2][2]} && {Precision[3][2]} & {Recall[3][2]} & {F1[3][2]} \\\\
       ExtraLarge & ExtraLarge  && {Precision[2][3]} & {Recall[2][3]} & {F1[2][3]} && {Precision[3][3]} & {Recall[3][3]} & {F1[3][3]} \\\\
     \\bottomrule
   \\end{{tabular}}
 \\end{{table}}''')