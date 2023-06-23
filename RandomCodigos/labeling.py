import os
import cv2

def swap_character(key, position):
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVXZ0123456789'
    char = key[position]
    new_char = alphabet.index(char)
    return new_char

def process_image(image_path):
    image_name = os.path.basename(image_path)
    txt_path = 'D:/matric/labels/obj_train_data/' + os.path.splitext(image_name)[0] + '.txt'

    # Load and display the image
    image = cv2.imread(image_path)
    cv2.imshow('Image', image)

    # Read the number of lines from the corresponding text file
    with open(txt_path, 'r') as file:
        lines = len(file.readlines())
        print(f"{lines} characters")

    # Accept user input
    user_input = input("Enter a key: ")

    if user_input == 's':
        with open(txt_path, 'r+') as file:
            for line_number, line in enumerate(file, 1):
                new_char = swap_character(user_input, line_number - 1)
                file.seek(file.tell() - len(line), os.SEEK_SET)
                file.write(str(new_char) + line[1:])
    else:
        if len(user_input) != lines:
            print("# of characters doesn't match, try again")
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            return

        with open(txt_path, 'w') as file:
            for line_number in range(lines):
                new_char = swap_character(user_input, line_number)
                file.write(str(new_char) + '\n')

    cv2.destroyAllWindows()

# Iterate through every image in folder A
folder_A = 'D:/matric/images100'
for filename in os.listdir(folder_A):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        image_path = os.path.join(folder_A, filename)
        process_image(image_path)
