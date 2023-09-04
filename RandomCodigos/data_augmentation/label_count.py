def get_label_counts(root):
    # Initialize a dictionary to store label counts
    label_counts = {}
    global_array = {}

    # Initialize a dictionary to store image IDs for each label
    label_image_ids = {}

    # Iterate through the 'image' elements in the XML
    for image in root.findall('image'):
        image_id = image.get('id')

        # Iterate through the 'polygon' elements in each image
        for polygon in image.findall("polygon[@label!='LP']"):
            label = polygon.get('label')

            # Update label counts
            if label in label_counts:
                label_counts[label] += 1
            else:
                label_counts[label] = 1

            # Update label_image_ids dictionary
            if label in label_image_ids:
                label_image_ids[label].append(image_id)
            else:
                label_image_ids[label] = [image_id]

    # Convert label_counts dictionary to a list of tuples
    global_array = [(label, count) for label, count in label_counts.items()]
    return global_array, label_image_ids

# Now, label_image_ids contains image IDs for each label
# You can access image IDs for a specific label like this:
# image_ids_for_label_A = label_image_ids['A']

# Example output
#print("Global Array:")
#print(global_array)

# Example output for accessing image IDs for a specific label
#print("Image IDs for Label 'A':")
#print(label_image_ids['A'])
