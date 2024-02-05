import cv2

# Function to capture image when 'p' key is pressed
def capture_image():
    # Open the default camera (camera index 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Read a frame from the camera
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        cap.release()
        return

    # Save the captured frame as an image file (you can customize the filename)
    cv2.imwrite("captured_image.jpg", frame)

    # Release the camera
    cap.release()

    print("Image captured successfully.")

# Main loop
#while True:
##    # Capture key press
 #   key = cv2.waitKey(1) & 0xFF
#
#    # Check if 'p' key is pressed (ASCII code for 'p' is 112)
#    if key == 112:
#        capture_image()
##    elif key == 27:  # Check if the 'Esc' key is pressed (ASCII code 27)
 #       break
capture_image()
# Destroy all OpenCV windows
cv2.destroyAllWindows()