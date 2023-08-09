import os
import matplotlib.pyplot as plt
import xml.etree.ElementTree as ET

# Path to the XML file
xml_file = "C:/Users/Vastingood/Documents/GitHub/Tese/RandomCodigos/XML/annotations.xml"
#xml_file = "C:/Users/Santi LM/Documents/GitHub/Tese/RandomCodigos/XML/annotations.xml"

# Load the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# Dictionary to store label counts
label_counts = {}

# Iterate over each image element
for image in root.findall('image'):
    # Iterate over each polygon element
    for polygon in image.findall('polygon'):
        label = polygon.get('label')
        if label in label_counts:
            label_counts[label] += 1
        else:
            label_counts[label] = 1

# Separate labels into letters and numbers
letters = []
numbers = []

for label, count in label_counts.items():
    if label.isalpha():
        letters.append((label, count))
    elif label.isdigit():
        numbers.append((label, count))

# Sort the letters and numbers in alphabetical and numerical order respectively
letters = sorted(letters, key=lambda x: x[0])
numbers = sorted(numbers, key=lambda x: int(x[0]))

# Extract labels and counts for plotting
letter_labels, letter_counts = zip(*letters)
number_labels, number_counts = zip(*numbers)

# Plotting the histogram
fig, ax = plt.subplots()
letter_bars = ax.bar(range(len(letter_labels)), letter_counts, color='blue')
number_bars = ax.bar(range(len(letter_labels), len(letter_labels) + len(number_labels)), number_counts, color='red')

# Customize the plot
ax.set_xlabel('Labels')
ax.set_ylabel('Count')
ax.set_xticks(range(len(letter_labels + number_labels)))
ax.set_xticklabels(letter_labels + number_labels)
ax.legend((letter_bars, number_bars), ('Letters', 'Numbers'))
ax.set_title('Label Histogram')

# Print the sum of each column
print("Sum of each column:")
print("Letters:")
for label, count in letters:
    print(label, ":", count)
print("Total:", sum(letter_counts))
for label, count in numbers:
    print(label, ":", count)
print("Total:", sum(number_counts))
print("Grand Total:", sum(letter_counts) + sum(number_counts))
# Show the plot
plt.show()
