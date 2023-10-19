import os

def count_and_write_unique_lines(directory_path):
    # Iterate through files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory_path, filename)
            
            # Read the file and count unique lines
            line_counts = {}
            with open(file_path, 'r') as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line in line_counts:
                        line_counts[line] += 1
                    else:
                        line_counts[line] = 1
            
            # Write unique lines and counts back to the file
            with open(file_path, 'w') as file:
                for line, count in line_counts.items():
                    file.write(f"{line} {count}\n")

# Example usage:
directory_path = "ids/"
count_and_write_unique_lines(directory_path)
