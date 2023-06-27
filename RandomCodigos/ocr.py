import cv2
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

# Directory containing the image files
directory = 'C:/Users/Santi LM/Documents/GitHub/Tese/cropped'

# Iterate through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.jpg') or filename.endswith('.png'):
        # Path to the image file
        image_path = os.path.join(directory, filename)

        # Read the image using OpenCV
        image = cv2.imread(image_path)

        # Check the height of the image
        height = image.shape[0]
        if height < 25:
            continue  # Skip the image if height is less than 25 pixels

        # Convert the image to the HSV color space
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Extract the V channel
        v_channel = hsv[:,:,2]

        # Binarize the V channel using thresholding
        _, binary_image = cv2.threshold(v_channel, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

        # Invert the binarized image
        inverted_image = cv2.bitwise_not(binary_image)

        # Apply a slight Gaussian blur
        blurred_image = cv2.GaussianBlur(inverted_image, (3, 3), 0)
        
        # Perform OCR using Tesseract on the blurred image
        text = pytesseract.image_to_string(blurred_image, config='--psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVXZ')

        # Print the extracted text
        print(f'File: {filename}')
        print(text)
        print('-' * 20)

        # Display the blurred image
        cv2.imshow('Blurred Image', blurred_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

