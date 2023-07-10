import cv2
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract.exe'

def delete_shapes(binary_image):
    # Find connected components in the binary image
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(binary_image)

    # Get the image dimensions
    height, width = binary_image.shape[:2]

    # Iterate over the connected components
    for label in range(1, num_labels):  # Exclude background label 0
        # Get the bounding box coordinates (x, y, width, height) of the shape
        x, y, w, h = stats[label, cv2.CC_STAT_LEFT], stats[label, cv2.CC_STAT_TOP], \
                    stats[label, cv2.CC_STAT_WIDTH], stats[label, cv2.CC_STAT_HEIGHT]
        
        # Check if the bounding box intersects with the image boundaries
        if x == 0 or y == 0 or (x + w) == width or (y + h) == height:
            # Remove the shape by setting its pixels to black
            binary_image[labels == label] = 0

    return binary_image

# Directory containing the image files
#directory = 'C:/Users/Vastingood/Documents/GitHub/Tese/cropped'
directory = 'C:/Users/Santi LM/Documents/GitHub/Tese/cropped'
further_processing = True
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
        img = cv2.bitwise_not(binary_image)

        # Perform opening operation (erode-dilate)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

        if further_processing:
            img = delete_shapes(img)

        # Perform blur on the image
        #img = cv2.GaussianBlur(img, (3, 3), 0)

        # Perform OCR using Tesseract on the image
        text = pytesseract.image_to_string(img, config='--psm 7 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVXZ')

        # Print the extracted text
        print(f'File: {filename}')
        print(text)
        print('-' * 20)

        # Display the image
        cv2.imshow('Blurred Image', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
