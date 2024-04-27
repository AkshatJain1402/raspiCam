from imutils . video import Videostream
import imagezmq
import argparse
import socket
import time
import cv2

video = cv2. Videocapture (0)
sender=imagezmq.Imagesender (connect to='tcp://{your server ip }:{your server port})

rpiName=socket.gethostname( )
time.sleep(2.O)
while True:
  ret, frame= video.read()
  #reducing the size of image
  grayscale=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  sender.send_image (rpiName,grayscale)
  print('sent one frame')
