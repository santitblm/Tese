import os
import numpy as np
import xml.etree.ElementTree as ET

# Define paths
username = "Santi LM"
xml_file = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/annotations.xml"
output_xml_file = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/filtered_annotations.xml"

# IDs to keep (as a numpy array)
ids_to_keep = np.array([0, 2561, 2, 3, 4, 2563, 6, 1025, 2568, 1, 523, 2572, 2573, 14, 15, 12, 17, 18, 2574, 20, 2580, 2582, 23, 2581, 26, 27, 2588, 28, 31, 32, 3103, 34, 33, 1060, 3109, 3104, 552, 3114, 3115, 1579, 2604, 2606, 2607, 560, 3119, 2608, 2096, 2612, 566, 2103, 2104, 2105, 2106, 2111, 2115, 3145, 3150, 3151, 2126, 2640, 3154, 3155, 3157, 2647, 3160, 601, 2659, 2660, 2661, 2662, 2663, 2664, 3178, 2667, 1642, 2666, 2163, 3700, 2166, 2167, 2170, 1146, 3710, 2174, 1667, 1673, 2187, 1676, 3214, 1679, 2192, 145, 660, 150, 1687, 2198, 1693, 2207, 2209, 2210, 2211, 1701, 2218, 2220, 1708, 1710, 1711, 2224, 3249, 1713, 3246, 2228, 2225, 2229, 2231, 2233, 1724, 3262, 3266, 1736, 3281, 3286, 1752, 1248, 225, 1767, 1770, 1771, 1772, 1774, 1777, 3318, 3319, 3320, 3321, 3323, 3848, 1802, 1810, 1812, 1814, 1823, 2338, 2340, 2341, 2346, 2348, 1837, 2350, 2352, 1841, 1842, 2355, 2359, 2360, 2366, 2374, 2376, 2379, 2385, 2387, 1882, 2395, 2396, 2398, 351, 2404, 1895, 361, 2412, 364, 3436, 367, 2415, 876, 2418, 2421, 1912, 2431, 2432, 2433, 387, 2436, 1412, 1413, 2437, 1925, 1417, 3463, 392, 1932, 1938, 1946, 2460, 1439, 2472, 2473, 2474, 2477, 1455, 2479, 1457, 1458, 3506, 1460, 3510, 1463, 1464, 3016, 3018, 3537, 2515, 981, 2519, 2528, 1508, 2021, 2532, 2539, 3567, 2032, 2033, 2034, 2555, 3849, 3850, 3851, 3852, 3853, 3854, 3855, 3856, 3857, 3858, 3859, 3860, 3861, 3862, 3863])

# Load the XML file
tree = ET.parse(xml_file)
root = tree.getroot()

# Find all image elements in the XML
image_elements = root.findall('image')

# Filter images based on IDs
images_to_keep = [image for image in image_elements if int(image.get('id')) in ids_to_keep]

# Create a new XML tree with filtered images
filtered_root = ET.Element('annotation')
for image in images_to_keep:
    filtered_root.append(image)

# Save the new XML tree to the output file
filtered_tree = ET.ElementTree(filtered_root)
filtered_tree.write(output_xml_file)
print("Filtered annotations saved to", output_xml_file)
