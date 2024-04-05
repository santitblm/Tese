from ultralytics import YOLO

class_labels = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"

#username, first_path = "santilm", "santilm/Desktop"
username, first_path = "planeamusafrente", "planeamusafrente/Desktop/SANTI"

sizes = ["n", "s", "m", "l", "x"]

models = ["PT_LP_Characters"]
vals = ["PT_LP_Characters"]


#models = ["LP_fromCars_480"]
#vals = ["LPs_fromCars"]



for model, val in zip(models, vals):
    for size in sizes:
        system = f"{model}_{size}"
        #try:
        print(f"MODEL BEING TESTED: {system}")

        net = YOLO(f"/home/{username}/Documents/GitHub/Tese/runs/detect/{system}/weights/best.pt")
        
        metrics = net.val(data = f"/home/{first_path}/Tese/datasets/{val}/{val}_val.yaml", 
                            name = f"VAL_{system}",
                            exist_ok = True
                            #, batch = 15
                            )
        #except:
            #print(system, "needs to be looked at\n")
        
        map50_worstClass = 100
        map50_95_worstClass = 100
        map50_bestClass = 0
        map50_95_bestClass = 0

        for i in range(34):
            map50_newValue = metrics.box.class_result(i)[2]
            map50_95_newValue = metrics.box.class_result(i)[3]
            # Check if the new value is smaller than the current worst value
            if map50_newValue < map50_worstClass:
                map50_worstClass = map50_newValue
                map50_95_worstClass = map50_95_newValue
                worst_class = class_labels[i]

            # Check if the new value is bigger than the current best value
            elif map50_newValue > map50_bestClass:
                map50_bestClass = map50_newValue
                map50_95_bestClass = map50_95_newValue
                best_class = class_labels[i]
            



        print(f"({best_class}, {worst_class})      & {(map50_bestClass)*100:.2f} & {(map50_95_bestClass)*100:.2f} & {(map50_worstClass)*100:.2f} & {(map50_95_worstClass)*100:.2f} & {(metrics.box.map50)*100:.2f} & {(metrics.box.map)*100:.2f}\n")

#print(metrics.box)
