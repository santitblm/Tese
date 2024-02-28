import cv2

def play_and_rotate_video(video_path):
    # Open the video file
    cap = cv2.VideoCapture(video_path)

    # Check if the video file was successfully opened
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Get the total number of frames in the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    # Set the starting frame position to the middle of the video
    start_frame = int(total_frames*0.584)
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_frame)

    # Get the frames per second (fps) of the video
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Create a window for video playback
    cv2.namedWindow("Video Player", cv2.WINDOW_NORMAL)

    while True:
        # Read a frame from the video
        ret, frame = cap.read()

        # If the video has ended, break out of the loop
        if not ret:
            break

        # Rotate the frame 90 degrees to the right
        rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)

        # Display the rotated frame in the window
        cv2.imshow("Video Player", rotated_frame)

        # Break the loop if the user presses the 'q' key
        if cv2.waitKey(0) & 0xFF == ord('q'):
            break

        # Wait for the next frame according to the fps
        #cv2.waitKey(0)

    # Release the video capture object and close the window
    cap.release()
    cv2.destroyAllWindows()

# Example usage:
# Replace 'path/to/your/video.mp4' with the actual path to your video file
video_path = ''
play_and_rotate_video(video_path)
