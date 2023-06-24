import os
import cv2

def swap_character(key, position):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVXZ0123456789'
    char = key[position]
    new_char = alphabet.index(char)
    return new_char

def process_image(image_path, last_input):
    image_name = os.path.basename(image_path)
    txt_path = 'D:/matric/labels/obj_train_data/' + os.path.splitext(image_name)[0] + '.txt'

    # Load the image
    image = cv2.imread(image_path)

    if image is None:
        print(f"Failed to load image: {image_path}")
        return

    # Display the image
    cv2.imshow('Image', image)
    cv2.waitKey(1)
    # Read the lines from the corresponding text file
    with open(txt_path, 'r') as file:
        lines = file.readlines()
        print(f"{len(lines)} characters")
    if len(lines) > 0:
        # Sort the lines based on the second number
        sorted_lines = sorted(lines, key=lambda line: float(line.split()[1]))

        # Accept user input
        user_input = input("Enter a key: ")

        if user_input == 's':
            user_input = last_input

        if len(user_input) != len(lines):
            print("# of characters doesn't match")
            return
        else:
            with open(txt_path, 'w') as file:
                for line, char_index in zip(sorted_lines, user_input):
                    char_index = swap_character(user_input, sorted_lines.index(line))
                    line_parts = line.strip().split()
                    if len(line_parts) >= 2:
                        new_line = f"{char_index} {' '.join(line_parts[1:])}\n"
                        file.write(new_line)

        cv2.destroyAllWindows()
        return user_input
    else:
        print('No characters, skipping...')
        cv2.destroyAllWindows()
        return last_input
    

# Iterate through every image in folder A
folder_A = 'D:/matric/images100'
last_input = ''
for filename in os.listdir(folder_A):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(folder_A, filename)
        current_input = process_image(image_path, last_input)
        last_input = current_input
