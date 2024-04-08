import numpy as np
import os

results_path = "/home/santilm/Desktop/Resultados/CarDet/"

Resolutions = ["1080p30", "1080p60", "27K30", "4K25"]
Char_sizes = ["l", "x"]
LP_sizes = ["s", "l"]


Precision = np.zeros((4, 5))
Recall = np.zeros((4, 5))
F1 = np.zeros((4, 5))

R = 0

for resolution in Resolutions:
    M = 0

    for char_model in Char_sizes:
        for lp_model in LP_sizes:
            results_file_path = os.path.join(results_path, f"{resolution}_{char_model}_{lp_model}.txt")
            with open(results_file_path, 'r') as f:
                lines = f.readlines()

            Precision[R][M] = round(float(lines[0])*100, 2)
            Recall[R][M] = round(float(lines[1])*100, 2)
            F1[R][M] = round(float(lines[2])*100, 2)


            M+=1


    R+=1


n_models = len(Char_sizes)+len(LP_sizes)

for i in range(n_models):
    Precision[i][-1] = round(sum(Precision[i][:n_models])/len(Precision[i][:n_models]), 2)
    Recall[i][-1] = round(sum(Recall[i][:n_models])/len(Recall[i][:n_models]), 2)
    F1[i][-1] = round(sum(F1[i][:n_models])/len(F1[i][:n_models]), 2)


print(f''' \\begin{{table}}[!htb]
   \\caption{{Results for the ALPR system \\textbf{{with}} car detection on various resolutions}}
   \\label{{tab:ALPR_QuestForOptimalResolution_CarDet}}
   \\centering
   \\renewcommand{{\\arraystretch}}{{1.2}}
   \\begin{{tabular}}{{@{{}}ccrccccccc@{{}}}}
     \\toprule
       \\multicolumn{{2}}{{c}}{{Models (size)}}  && \\multicolumn{{3}}{{c}}{{1080p30 (\\%)}} & \\phantom{{abc}} & \\multicolumn{{3}}{{c}}{{1080p60 (\\%)}} \\\\
     \\cmidrule{{4-6}}
     \\cmidrule{{8-10}}
     \\cmidrule{{1-2}}
       Characters & LPs        &&  Precision        &  Recall        &  F1        &&  Precision        &  Recall        &  F1 \\\\
     \\midrule
       Large      & Small      && {Precision[0][0]} & {Recall[0][0]} & {F1[0][0]} && {Precision[1][0]} & {Recall[1][0]} & {F1[1][0]} \\\\
       Large      & Large      && {Precision[0][1]} & {Recall[0][1]} & {F1[0][1]} && {Precision[1][1]} & {Recall[1][1]} & {F1[1][1]} \\\\
       ExtraLarge & Small      && {Precision[0][2]} & {Recall[0][2]} & {F1[0][2]} && {Precision[1][2]} & {Recall[1][2]} & {F1[1][2]} \\\\
       ExtraLarge & Large      && {Precision[0][3]} & {Recall[0][3]} & {F1[0][3]} && {Precision[1][3]} & {Recall[1][3]} & {F1[1][3]} \\\\
     \\cmidrule{{1-2}}
       \\multicolumn{{2}}{{c}}{{Average}} && {Precision[0][4]} & {Recall[0][4]} & {F1[0][4]} && {Precision[1][4]} & {Recall[1][4]} & {F1[1][4]} \\\\
    \\midrule
      \\multicolumn{{2}}{{c}}{{Models (size)}} && \\multicolumn{{3}}{{c}}{{2.7K30 (\\%)}} & \\phantom{{abc}} & \\multicolumn{{3}}{{c}}{{4K25 (\\%)}} \\\\
     \\cmidrule{{4-6}}
     \\cmidrule{{8-10}}
     \\cmidrule{{1-2}}
       Characters & LPs        &&  Precision        &  Recall        &  F1        &&  Precision        &  Recall        &  F1 \\\\
     \\midrule
       Large      & Small      && {Precision[2][0]} & {Recall[2][0]} & {F1[2][0]} && {Precision[3][0]} & {Recall[3][0]} & {F1[3][0]} \\\\
       Large      & Large      && {Precision[2][1]} & {Recall[2][1]} & {F1[2][1]} && {Precision[3][1]} & {Recall[3][1]} & {F1[3][1]} \\\\
       ExtraLarge & Small      && {Precision[2][2]} & {Recall[2][2]} & {F1[2][2]} && {Precision[3][2]} & {Recall[3][2]} & {F1[3][2]} \\\\
       ExtraLarge & Large      && {Precision[2][3]} & {Recall[2][3]} & {F1[2][3]} && {Precision[3][3]} & {Recall[3][3]} & {F1[3][3]} \\\\
     \\cmidrule{{1-2}}
       \\multicolumn{{2}}{{c}}{{Average}} && {Precision[2][4]} & {Recall[2][4]} & {F1[2][4]} && {Precision[3][4]} & {Recall[3][4]} & {F1[3][4]} \\\\
     \\bottomrule
   \\end{{tabular}}
 \\end{{table}}''')