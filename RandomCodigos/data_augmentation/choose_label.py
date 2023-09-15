import random


# Function to choose a random label based on the number in the 2nd column
def choose_label(goal_number, global_array):
    
    # Calculate weights based on the inverse of the numbers in the 2nd column
    weights = [1 / col2 for _, col2 in global_array]

    # Normalize weights so they sum up to 1
    total_weight = sum(weights)
    normalized_weights = [weight / total_weight for weight in weights]

    # Use random.choices to select a label with the specified weights
    chosen_label = random.choices([row[0] for row in global_array], weights=normalized_weights)[0]

    # Increment the number in the 2nd column corresponding to the chosen label
    for i, (label, col2) in enumerate(global_array):
        if label == chosen_label and col2<goal_number:
            global_array[i] = (label, col2 + 1)
            break

    return chosen_label, global_array

