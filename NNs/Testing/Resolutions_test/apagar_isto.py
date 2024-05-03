import os
from heuristic import LP_val

mode = "/home/santilm/Desktop/Results_LPDet+OCR/Resolutions_test/NOcardet - planeamus/NOcardet/"

#for folder in os.listdir(mode):
#    for id in os.listdir(os.path.join(mode, folder, "ids")):
#        filename = os.path.join(mode, folder, "ids", id)
#        with open(filename, 'r') as file:
#            lines = file.readlines()
#        new_lines = []
#        for line in lines:
#            new_line = line.split(" ")[0]
#            new_lines.append(new_line)
#        with open(filename, 'w') as file:
#            for new_line in new_lines:
#                file.write(new_line + "\n")


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
                if line in line_counts:
                    line_counts[line] += 1
                else:
                    line_counts[line] = 1
        
        # Write unique lines and counts back to the file
        with open(file_path, 'w') as file:
            max_count = 0
            max_line = None
            for line, count in line_counts.items():
                line = line.split("\n")[0]
                file.write(f"{line} {count}\n")
                # Update max_line if necessary
                #print(line)
                if count > max_count and LP_val(line):
                    max_line = line
                    max_count = count

            # In case there is no valid PT LP inside the id txt
            if max_line is None:
                for line, count in line_counts.items():
                    # Update max_line if necessary
                    if count > max_count:
                        max_line = line
                        max_count = count
            # In case at least one valid PT LP is present in the id txt
            else:
                with open(predictions_path, 'a') as predictions_file:
                    predictions_file.write(max_line+"\n")

for folder in os.listdir(mode):
    ids_path = os.path.join(mode, folder, "ids")
    organize_ids(ids_path)
