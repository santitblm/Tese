import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import string

# Path to the XML file
xml_file = "C:/Users/Santi LM/Documents/GitHub/Tese/RandomCodigos/XML/annotations.xml"

# Load the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# Count the occurrences of each polygon label
label_counts = {}

for image in root.findall('image'):
    for polygon in image.findall('polygon'):
        label = polygon.get('label')
        if label in label_counts:
            label_counts[label] += 1
        else:
            label_counts[label] = 1

# Generate all letter labels from A to Z
letters = list(string.ascii_uppercase)

# Generate all number labels from 0 to 9
numbers = [str(i) for i in range(10)]

# Prepare data for plotting
x_labels = range(len(letters + numbers))
y_labels = [label_counts.get(label, 0) for label in letters + numbers]

# Plot the histogram
plt.figure(figsize=(10, 6))
plt.bar(x_labels[:26], y_labels[:26], color='blue', label='Letters')
plt.bar(x_labels[26:], y_labels[26:], color='red', label='Numbers')

# Customize the plot
plt.xlabel('Label')
plt.ylabel('Count')
plt.title('Occurrences of Polygon Labels')
plt.xticks(list(x_labels), letters + numbers)
plt.legend()

# Show the plot
plt.show()
