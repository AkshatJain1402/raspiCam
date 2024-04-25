# import the necessary packages
from imutils import build_montages
from datetime import datetime
import numpy as np
import imagezmq
import argparse
import imutils
import cv2
mW=1


mH=1

# initialize the ImageHub object
imageHub= imagezmq.ImageHub()
frameDict = {}
print("[INFO] connecting to server...")
count=0
while True:
    count+=1
    try:

        (rpiName, frame) = imageHub.recv_image()
        imageHub.send_reply(b'OK')
        frame=imutils.resize(frame,width=400)
        (H,W)=frame.shape[:2]
    
        #save the frame locally
        cv2.imwrite(f'./imagesMQZ/frame{count}.jpeg',frame)
        #read frame from local storage
        cv2.imshow('Frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
        

    except Exception as e:
        print('error',e)
        continue
cv2.destroyAllWindows()
