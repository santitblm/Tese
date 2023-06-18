import cv2
import time
 
capture = cv2.VideoCapture('C:/Users/Vastingood/Downloads/20230602_134058.mp4')
 
frameNr = 0
 
while (True):
 
    success, frame = capture.read()
 
    if success:
        
        #print(framestr[-7:-1])
        if frameNr > 6574:
            framestr = '00000' + str(frameNr) + '.'
            cv2.imwrite(f'C:/Users/Vastingood/Desktop/output1/frame_' + framestr[-7:-1] + '.jpg', frame)
            print(frameNr, 'written')
        else:
            print(frameNr)
 
    else:
        break
    #time.sleep(0.2)
    frameNr += 1
    
    
 
capture.release()