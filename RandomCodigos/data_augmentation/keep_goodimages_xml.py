import os
import numpy as np
import xml.etree.ElementTree as ET

# Define paths
username = "Santi LM"
xml_file = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/XML/annotations.xml"
output_xml_file = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/filtered_annotations.xml"

# IDs to keep (as a numpy array)
ids_to_keep = np.array([1417, 2104, 2106, 2436, 2661, 3155, 3160, 0, 1412, 1673, 1710, 1814, 2350, 2359, 2412, 2515, 3150, 361, 1679, 1810, 1882, 2126, 2421, 2431, 2474, 3214, 523, 981, 1693, 1711, 1772, 2192, 2519, 2568, 2572, 351, 364, 367, 1508, 1676, 2228, 2338, 2341, 2396, 2573, 2582, 2606, 2659, 3115, 3154, 2, 560, 1463, 1812, 1837, 2103, 2432, 2460, 2561, 2667, 20, 27, 1458, 1895, 2379, 2418, 2519, 2612, 3710, 3, 1687, 1842, 2163, 2218, 2220, 2348, 2580, 2661, 3155, 3700, 145, 150, 1767, 1777, 2355, 2472, 2473, 2640, 3249, 3319, 3321, 3506, 0, 1439, 1667, 1687, 1752, 1932, 2103, 2174, 2395, 2431, 2437, 2528, 2607, 3160, 3262, 3510, 3848, 0, 4, 6, 14, 15, 20, 23, 27, 31, 32, 34, 18, 1417, 1770, 1774, 1841, 2582, 2374, 2376, 2398, 2667, 4, 1814, 2661, 3018, 3145, 1676, 1713, 2187, 2387, 2433, 2573, 552, 2021, 2207, 2209, 2224, 2340, 2359, 3109, 2233, 2105, 3103, 2662, 3016, 1460, 1708, 2166, 2167, 2555, 3286, 1060, 1137, 1736, 2404, 12, 15, 17, 18, 26, 28, 32, 34, 361, 364, 387, 3157, 3848, 23, 33, 660, 1455, 1711, 2032, 2415, 2431, 1774, 2170, 2532, 2539, 3246, 3266, 1701, 1802, 2225, 2664, 3119, 3178, 3281, 566, 2346, 3114, 601, 1895, 2555, 2572, 2573, 2574, 1413, 1912, 2033, 2115, 2477, 2479, 2563, 2604, 3145, 3323, 3506, 1025, 2198, 2366, 2608, 3, 225, 1642, 1771, 2096, 2126, 2231, 2360, 2385, 2582, 3104, 2, 17, 32, 2229, 2359, 3320, 1938, 1146, 1464, 1724, 2606, 3537, 1, 392, 1457, 2034, 2198, 2352, 2395, 3318, 3436, 876, 2111, 2210, 2211, 2581, 2660, 2663, 2666, 3849, 3850, 3851, 3853, 3854, 3855, 3856, 3858, 3859, 3860, 3861, 3862, 3863])


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
