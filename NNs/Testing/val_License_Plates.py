from ultralytics import YOLO

#username, first_path = "santilm", "santilm/Desktop"
username, first_path = "planeamusafrente", "planeamusafrente/Desktop/SANTI"

sizes = ["n", "s", "m"]#, "l", "x"]

models = ["License_Plates_1280", "LP_fromCars_480", "PT_LP_Characters"]
vals = ["License_Plates", "LPs_fromCars", "PT_LP_Characters"]

sizes = ["l"]

models = ["License_Plates_1280"]
vals = ["License_Plates"]


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
                            , batch = 15
                            )
        #except:
            #print(system, "needs to be looked at\n")
        print(f"{(metrics.box.class_result(0)[2])*100:.2f} & {(metrics.box.class_result(0)[3])*100:.2f} & {(metrics.box.class_result(1)[2])*100:.2f} & {(metrics.box.class_result(1)[3])*100:.2f} & {(metrics.box.map50)*100:.2f} & {(metrics.box.map)*100:.2f}")

#print(metrics.box)
