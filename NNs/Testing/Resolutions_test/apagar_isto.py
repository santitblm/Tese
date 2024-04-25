import os

mode = "/home/planeamusafrente/Desktop/Results_LPDet+OCR/Resolutions_test/NOcardet"

for folder in os.listdir(mode):
    filename = os.path.join(mode, folder, "predictions.txt")
    with open(filename, 'r') as file:
        lines = file.readlines()
    new_lines = []
    for line in lines:
        new_line = line.split(" ")[0]
        new_lines.append(new_line)
    with open(filename, 'w') as file:
        for new_line in new_lines:
            file.write(new_line + "\n")
    continue