import numpy as np
import os

#username = "santilm"
username = "planeamusafrente"

results_path = f"/home/{username}/Desktop/Resultados/Resolutions_test/CarDet/"

Resolutions = ["1080p30", "1080p60", "27K30", "4K25"]
Char_sizes = ["l", "x"]
LP_sizes = ["s", "l"]


Precision = np.zeros((4, 5))
Recall = np.zeros((4, 5))
F1 = np.zeros((4, 5))
FPS1 = np.zeros((4, 5))
FPS2 = np.zeros((4, 5)) # planeamus

R = 0

for resolution in Resolutions:
    M = 0

    for char_model in Char_sizes:
        for lp_model in LP_sizes:
            results_file = f"{resolution}_{char_model}_{lp_model}.txt" 
            results_file_path = os.path.join(results_path, results_file)
            with open(results_file_path, 'r') as f:
                lines = f.readlines()

            # planeamus results file
            #with open(os.path.join(results_path, "planeamus", results_file)) as pl:
            #    planeamus = pl.readlines()

            Precision[R][M] = round(float(lines[0])*100, 2)
            Recall[R][M] = round(float(lines[1])*100, 2)
            F1[R][M] = round(float(lines[2])*100, 2)
            FPS1[R][M] = float(lines[3])
            #FPS2[R][M] = float(planeamus[3])

            M+=1


    R+=1


n_models = len(Char_sizes)*len(LP_sizes)
FPS2 = FPS1
for i in range(n_models):
    Precision[i][-1] = round(sum(Precision[i][:n_models])/len(Precision[i][:n_models]), 2)
    Recall[i][-1] = round(sum(Recall[i][:n_models])/len(Recall[i][:n_models]), 2)
    F1[i][-1] = round(sum(F1[i][:n_models])/len(F1[i][:n_models]), 2)
    FPS1[i][-1] = sum(FPS1[i][:n_models])/len(FPS1[i][:n_models])
    FPS2[i][-1] = sum(FPS2[i][:n_models])/len(FPS2[i][:n_models])


print(f''' \\begin{{table}}[!htb]
   \\caption{{Results for the ALPR system \\textbf{{with}} car detection on various resolutions}}
   \\label{{tab:ALPR_QuestForOptimalResolution_CarDet}}
   \\centering
   \\renewcommand{{\\arraystretch}}{{1.2}}
   \\begin{{tabular}}{{@{{}}ccrcccrccrcccrcc@{{}}}}
     \\toprule
       \\multicolumn{{2}}{{c}}{{Models (size)}}  && \\multicolumn{{3}}{{c}}{{1080p30 (\\%)}} && \\multicolumn{{2}}{{c}}{{FPS(\\%)}} && \\multicolumn{{3}}{{c}}{{1080p60 (\\%)}} && \\multicolumn{{2}}{{c}}{{FPS(\\%)}} \\\\
     \\cmidrule{{4-6}}
     \\cmidrule{{8-9}}
     \\cmidrule{{1-2}}
     \\
       Characters & LPs    &&  Precision  &  Recall  &  F1  &&  Precision  &  Recall  &  F1 \\\\
     \\midrule
       Large  & Small      && {Precision[0][0]} & {Recall[0][0]} & {F1[0][0]} &&  {Precision[1][0]} & {Recall[1][0]} & {F1[1][0]} \\
       Large  & Large      && {Precision[0][1]} & {Recall[0][1]} & {F1[0][1]} &&  {Precision[1][1]} & {Recall[1][1]} & {F1[1][1]} \\
       XLarge & Small      && {Precision[0][2]} & {Recall[0][2]} & {F1[0][2]} &&  {Precision[1][2]} & {Recall[1][2]} & {F1[1][2]} \\
       XLarge & Large      && {Precision[0][3]} & {Recall[0][3]} & {F1[0][3]} &&  {Precision[1][3]} & {Recall[1][3]} & {F1[1][3]} \\
     \\cmidrule{{1-2}}
       \\multicolumn{{2}}{{c}}{{Average}} && {Precision[0][4]} & {Recall[0][4]} & {F1[0][4]} &&  {Precision[1][4]} & {Recall[1][4]} & {F1[1][4]} \\
    \\midrule
      \\multicolumn{{2}}{{c}}{{Models (size)}} && \\multicolumn{{3}}{{c}}{{2.7K30 (\\%)}} && \\multicolumn{{2}}{{c}}{{FPS(\\%)}} && \\multicolumn{{3}}{{c}}{{4K25 (\\%)}} && \\multicolumn{{2}}{{c}}{{FPS(\\%)}} \\\\
     \\cmidrule{{4-6}}
     \\cmidrule{{8-9}}
     \\cmidrule{{1-2}}
     \\cmidrule{{11-12}}
       Characters & LPs    &&  Precision  &  Recall  &  F1  &&  Precision  &  Recall  &  F1 \\\\
     \\midrule
       Large  & Small      && {Precision[2][0]} & {Recall[2][0]} & {F1[2][0]} &&  {Precision[3][0]} & {Recall[3][0]} & {F1[3][0]} \\
       Large  & Large      && {Precision[2][1]} & {Recall[2][1]} & {F1[2][1]} &&  {Precision[3][1]} & {Recall[3][1]} & {F1[3][1]} \\
       XLarge & Small      && {Precision[2][2]} & {Recall[2][2]} & {F1[2][2]} &&  {Precision[3][2]} & {Recall[3][2]} & {F1[3][2]} \\
       XLarge & Large      && {Precision[2][3]} & {Recall[2][3]} & {F1[2][3]} &&  {Precision[3][3]} & {Recall[3][3]} & {F1[3][3]} \\
     \\cmidrule{{1-2}}
       \\multicolumn{{2}}{{c}}{{Average}} && {Precision[2][4]} & {Recall[2][4]} & {F1[2][4]} &&  {Precision[3][4]} & {Recall[3][4]} & {F1[3][4]} \\
     \\bottomrule
   \\end{{tabular}}
 \\end{{table}}''')



print(f''' \\begin{{table}}[!htb]
   \\caption{{Results for the ALPR system \\textbf{{with}} car detection on various resolutions}}
   \\label{{tab:ALPR_QuestForOptimalResolution_CarDet}}
   \\centering
   \\renewcommand{{\\arraystretch}}{{1.2}}
   \\begin{{tabular}}{{@{{}}ccrcccc@{{}}}}
     \\toprule
     \\multicolumn{{7}}{{c}}{{PC1}}
      \\midrule
       \\multicolumn{{2}}{{c}}{{Models (size)}}  && 1080p30  & 1080p60  & 2.7K30  & 4K25 \\\\
     \\cmidrule{{1-2}}
     \\cmidrule{{4-7}}
     \\
       Characters & LPs        && &&& \\\\
     \\midrule
       Large      & Small      && {round((FPS1[0][0]/30)*100, 2)} & {round((FPS1[1][0]/60)*100, 2)} & {round((FPS1[2][0]/30)*100, 2)} & {round((FPS1[3][0]/25)*100, 2)} \\\\
       Large      & Large      && {round((FPS1[0][1]/30)*100, 2)} & {round((FPS1[1][1]/60)*100, 2)} & {round((FPS1[2][1]/30)*100, 2)} & {round((FPS1[3][1]/25)*100, 2)} \\\\
       XLarge     & Small      && {round((FPS1[0][2]/30)*100, 2)} & {round((FPS1[1][2]/60)*100, 2)} & {round((FPS1[2][2]/30)*100, 2)} & {round((FPS1[3][2]/25)*100, 2)} \\\\
       XLarge     & Large      && {round((FPS1[0][3]/30)*100, 2)} & {round((FPS1[1][3]/60)*100, 2)} & {round((FPS1[2][3]/30)*100, 2)} & {round((FPS1[3][3]/25)*100, 2)} \\\\
    \\midrule
    \\multicolumn{{7}}{{c}}{{PC1}}
      \\midrule
      \\multicolumn{{2}}{{c}}{{Models (size)}}  && 1080p30 & 1080p60 & 2.7K30 & 4K25 \\\\
     \\cmidrule{{1-2}}
     \\cmidrule{{4-7}}
     \\
       Characters & LPs        &&  &&& \\\\
     \\midrule
       Large      & Small      && {round((FPS2[0][0]/30)*100, 2)} & {round((FPS2[1][0]/60)*100, 2)} & {round((FPS2[2][0]/30)*100, 2)} & {round((FPS2[3][0]/25)*100, 2)} \\\\
       Large      & Large      && {round((FPS2[0][1]/30)*100, 2)} & {round((FPS2[1][1]/60)*100, 2)} & {round((FPS2[2][1]/30)*100, 2)} & {round((FPS2[3][1]/25)*100, 2)} \\\\
       XLarge     & Small      && {round((FPS2[0][2]/30)*100, 2)} & {round((FPS2[1][2]/60)*100, 2)} & {round((FPS2[2][2]/30)*100, 2)} & {round((FPS2[3][2]/25)*100, 2)} \\\\
       XLarge     & Large      && {round((FPS2[0][3]/30)*100, 2)} & {round((FPS2[1][3]/60)*100, 2)} & {round((FPS2[2][3]/30)*100, 2)} & {round((FPS2[3][3]/25)*100, 2)} \\\\
    \\bottomrule
   \\end{{tabular}}
 \\end{{table}}''')
