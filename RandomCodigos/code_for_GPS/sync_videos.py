'''
This script assumes that you show the time on camera and the goal is 
to press enter in the first frame that the clock changes the seconds 
value. Then type the shown time in the terminal with format HHMMSS 
and the code will automatically rename the video. This is all based
on the fps of the video.

Santi LM
'''

import cv2
import os

def seconds_to_hhmmss_milliseconds(total_seconds):
    # Calculate hours, minutes, and seconds
    hours = int(total_seconds // 3600)
    remaining_seconds = total_seconds % 3600
    minutes = int(remaining_seconds // 60)
    seconds = int(remaining_seconds % 60)

    # Extract milliseconds
    milliseconds = int((total_seconds - int(total_seconds)) * 1000)

    # Format the time as HH:MM:SS.mmm
    formatted_time = '{:02d}{:02d}{:02d}{:03d}'.format(hours, minutes, seconds, milliseconds)
    return formatted_time

video = "20240410_163721.MOV"
video_path= "/home/santilm/Desktop/Tese/datasets/Videos/"
fps = 30

cap = cv2.VideoCapture(video_path + video)
n_frame = 0

while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()

    if success:
        cv2.imshow("video_tosync", frame)
        key = cv2.waitKey(0)

        if key == 113:
            cv2.destroyAllWindows()
            cap.release()
            break
        elif key == 13:
            time = input("Time (HHMMSS):")
            hours = int(time[0:2])
            minutes = int(time[2:4])
            seconds = int(time[4:6])
            print(hours, minutes, seconds)
            total_seconds = hours*3600 + minutes*60 + seconds - n_frame/fps
            print(total_seconds)
            formatted_time = seconds_to_hhmmss_milliseconds(total_seconds)
            print(formatted_time)
            os.rename(video_path + video, video_path + f"{video.split('_')[0]}_{formatted_time}.MOV")
            cv2.destroyAllWindows()
            cap.release()
            break
    n_frame+=1

                    