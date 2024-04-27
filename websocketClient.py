import struct
import time
import socket
import cv2

SERVER_PORT={your server port }
SERVER_IP={your server ip}


cap=cv2.VideoCapture(0)
client_socket=socket.socket (socket.AF INET, socket.SOCK_STREAM)
client_socket.connect((SERVER_IP,SERVER_PORT))
while True:
  print('sending frame')
  ret,frame=cap.read()
  grey_frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  #0 is the worst quality and 90 the best quality
  ret,encoded_frame=cv2.imencode('.jpeg',grey_frame, [cv2.IMWRITE_JPEG_QUALITY, 45])
  frame_bytes=encoded_frame.tobytes()

  frame_size_bytes=struct.pack ("I" , len(frame bytes))
  print(frame bytes)
  client_socket.sendall((frame_size_bytes+frame_bytes))


  if cv2.waitKey(1)==ord('q'):
      break
cap.release()
client_socket.close()
cv2.destroyAllWindows( )
