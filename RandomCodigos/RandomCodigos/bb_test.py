import cv2
import os

# Define your label key
label_key = "ABCDEFGHIJKLMNOPQRSTUVXZ0123456789"

# Specify the folders containing images and text files
username = "Santi LM"
#image_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/synthetic/"
#txt_folder = f"C:/Users/{username}/Documents/GitHub/Tese/RandomCodigos/data_augmentation/synthetic/labels/"
image_folder = "/home/santilm/Desktop/Tese/datasets/PT_LP_Characters/train/images/"
txt_folder = "/home/santilm/Desktop/Tese/datasets/PT_LP_Characters/train/labels/"

# Iterate through the images in the image folder
for image_filename in os.listdir(image_folder):
    if image_filename.endswith((".jpg", ".png")):  # You can add more image formats as needed
        image_path = os.path.join(image_folder, image_filename)
        txt_filename = os.path.splitext(image_filename)[0] + ".txt"
        txt_path = os.path.join(txt_folder, txt_filename)
        # Read the image
        img = cv2.imread(image_path)

        # Read the corresponding text file
        with open(txt_path, "r") as txt_file:
            lines = txt_file.readlines()

        for line in lines:
            values = line.split()
            if len(values) == 5:
                label_idx = int(values[0])
                x_center = float(values[1])
                y_center = float(values[2])
                width = float(values[3])
                height = float(values[4])
                # Calculate bounding box coordinates
                x1 = int((x_center - width / 2) * img.shape[1])
                y1 = int((y_center - height / 2) * img.shape[0])
                x2 = int((x_center + width / 2) * img.shape[1])
                y2 = int((y_center + height / 2) * img.shape[0])

                # Get the label from the key
                label = label_key[label_idx]
                print(label, x_center, y_center, width, height)

                # Draw bounding box and label
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Save the annotated image
        cv2.imshow("Annotated image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

# Close all OpenCV windows (if any)
cv2.destroyAllWindows()
