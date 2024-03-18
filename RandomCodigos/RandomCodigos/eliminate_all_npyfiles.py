import os

def remove_npy_files(directory):
    """
    Remove all .npy files in a given directory.

    Parameters:
        directory (str): The directory path.

    Returns:
        None
    """
    for filename in os.listdir(directory):
        if filename.endswith(".npy"):
            file_path = os.path.join(directory, filename)
            os.remove(file_path)
            print(f"Removed: {file_path}")

# Example usage:
# Specify the directory path where .npy files are located
directory_path = "/home/santilm/Desktop/Tese/datasets/PT_LP_Characters/train/images/"
remove_npy_files(directory_path)
