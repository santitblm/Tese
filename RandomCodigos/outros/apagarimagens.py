import os

def delete_images(folder_path, start, end):
    for i in range(start, end + 1):
        #image_filename = f"img{folder_path[-3:]}-{i:05d}.png"
        image_filename = f"img036-{i:05d}.png"
        image_path = os.path.join(folder_path, image_filename)
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"Deleted: {image_path}")

def process_txt_file(txt_file, folders_path):
    with open(txt_file, 'r') as file:
        lines = file.readlines()

    folder_path = os.path.join(folders_path, 'Z')
    for line in lines:
        start, end = map(int, line.strip().split('-'))
        if os.path.exists(folder_path):
            delete_images(folder_path, start, end)
        else:
            break

if __name__ == "__main__":
    txt_file_path = "C:/Users/Santi LM/Desktop/nos.txt"
    folders_path = "C:/Users/Santi LM/Downloads/English/Fnt/"

    process_txt_file(txt_file_path, folders_path)
