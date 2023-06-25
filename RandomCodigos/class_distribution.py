import os
import re
import matplotlib.pyplot as plt

def extract_first_number(line):
    # Use regular expression to extract the first number from a line
    match = re.match(r"^(\d+)", line)
    if match:
        return int(match.group(1))
    else:
        return None

def get_label(number):
    # Map numbers 0-34 to letters A-Z and digits 0-9
    labels = 'ABCDEFGHIJKLMNOPQRSTUVXZ0123456789'
    if 0 <= number <= 34:
        return labels[number]
    else:
        return None

n = 34

def process_text_files(directory):
    number_counts = [0] * n  # Initialize count for numbers 0 to 33

    # Iterate through each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)

            # Read lines from the file
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Extract first number from each line and update count
            for line in lines:
                number = extract_first_number(line)
                if number is not None and 0 <= number <= n - 1:
                    number_counts[number] += 1

    return number_counts

def create_histogram(number_counts):
    numbers = range(n)
    frequencies = number_counts

    # Calculate the average of the last 10 bars and the remaining bars
    last_10_average = sum(frequencies[-10:]) / 10
    other_average = sum(frequencies[:-10]) / (n - 10)

    # Create the histogram
    bars = plt.bar(numbers, frequencies)
    plt.xlabel('Numbers')
    plt.ylabel('Frequency')
    plt.title('Number Frequency Histogram')

    # Add count labels with letters/digits vertically aligned with y-axis
    for i, frequency in enumerate(frequencies):
        if frequency > 0:
            label = get_label(i)
            if label is not None:
                label = label + '_' + str(frequency)
            else:
                label = str(frequency)
            plt.text(i, frequency, label, ha='center', va='bottom', rotation='vertical')

    # Highlight the last 10 bars in red
    for i in range(n - 10, n):
        bars[i].set_color('red')

    # Add dashed lines for the average values
    plt.axhline(last_10_average, color='blue', linestyle='dashed', linewidth=1.5, label='Numbers Average')
    plt.axhline(other_average, color='green', linestyle='dashed', linewidth=1.5, label='Letters Average')

    plt.legend()

    plt.show()

# Specify the directory containing the text files
directory = 'D:/matric/train/labels'

# Process the text files and create the histogram
number_counts = process_text_files(directory)
create_histogram(number_counts)
