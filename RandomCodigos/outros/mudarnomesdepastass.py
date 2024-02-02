import os

def change_folder_names(folders_path):
    valid_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVXZ"

    folders = sorted(os.listdir(folders_path))
    for index, folder_name in enumerate(folders):
        new_name = valid_chars[index]
        new_folder_path = os.path.join(folders_path, new_name)
        old_folder_path = os.path.join(folders_path, folder_name)

        os.rename(old_folder_path, new_folder_path)
        print(f"Renamed: {old_folder_path} to {new_folder_path}")

if __name__ == "__main__":
    folders_path = "C:/Users/Santi LM/Downloads/English/Fnt/"

    change_folder_names(folders_path)