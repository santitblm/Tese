# Function to extract the time from each line
def extract_time(line):
    return line.split()[1]

# Read lines from the input file
with open("/home/santilm/Desktop/Results_LPDet+OCR/Final_Tese/WithCD/20240415_155436900.MOV/predictions.txt", "r") as file:
    lines = file.readlines()

# Sort the lines based on the extracted time
sorted_lines = sorted(lines, key=extract_time)

# Write sorted lines to a new file
with open("/home/santilm/Desktop/Results_LPDet+OCR/Final_Tese/WithCD/20240415_155436900.MOV/predictionsfinal.txt", "w") as file:
    file.writelines(sorted_lines)
