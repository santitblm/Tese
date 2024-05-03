import os

def organize_ids(ids_path):#, FPS):

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
        max_count = 0
        chosen_LP = None
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                LP = line.split(" ")[0]
                count = int(line.split(" ")[1])
                if count > max_count:
                    max_count = count
                    chosen_LP = LP

        if chosen_LP is not None:
            with open(predictions_path, 'a') as predictions_file:
                predictions_file.write(chosen_LP + "\n")

mode = "/home/santilm/Desktop/Results_LPDet+OCR/Resolutions_test/NOcardet - planeamus/NOcardet/"
for folder in os.listdir(mode):

    output_dir = os.path.join(mode, folder, "ids")


    organize_ids(output_dir)


