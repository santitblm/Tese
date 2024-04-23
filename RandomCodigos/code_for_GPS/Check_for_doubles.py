from maps_processor import read_LPs_fromHTML
import os

directory = "/home/santilm/Desktop/Mapas/WithCD"

file_path = os.path.join(directory, "map_20240415_155436.html")

LPs = read_LPs_fromHTML(file_path)

repeated_entries = []

# Initialize an empty set to keep track of seen entries
seen_entries = set()
print(LPs)
# Iterate through each entry in the list
for entry in LPs:
    # Check if the entry has already been seen
    if entry in seen_entries:
        # If it has, add it to the list of repeated entries
        repeated_entries.append(entry)
    else:
        # If it hasn't, add it to the set of seen entries
        seen_entries.add(entry)

# Print the repeated entries, if any
if repeated_entries:
    print("Repeated entries:")
    for entry in repeated_entries:
        print(entry)
else:
    print("No repeated entries found.")