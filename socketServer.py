import socket
import cv2
import struct
import numpy as np
from ultralytics import YOLO
import math
# Port to listen on
SERVER_PORT = 5555
#creating YOLO object model
dict = {}

model = YOLO("./Yolo-Weights/yolov8n.pt")
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"
              ]










# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("", SERVER_PORT))
server_socket.listen(1)

# Accept client connection
client_socket, client_address = server_socket.accept()
print(f"Connected to client {client_address}")
count =0
while True:
    print('recievving')
    # Receive frame size (4 bytes integer)
    frame_size_bytes = client_socket.recv(4)
    frame_size = struct.unpack("I", frame_size_bytes)[0]

    # Receive frame data
    frame_bytes = b''
    while len(frame_bytes) < frame_size:
        received_bytes = client_socket.recv(65536)
        frame_bytes += received_bytes

    # Decode frame from bytes
    decoded_frame = cv2.imdecode(np.frombuffer(frame_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Display the frame (optional, can be replaced with server-side processing)
    cv2.imshow('Frame', decoded_frame)
    cv2.imwrite(f'./imagesMQZ/frame{count}.jpeg',decoded_frame)
    results = model(decoded_frame, stream=True)
    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1

            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            currentClass = classNames[cls]

            if conf > 0.3:
                # cvzone.putTextRect(img, f'{currentClass} {conf}', (max(0, x1), max(35, y1)),
                #                    scale=0.6, thickness=1, offset=3)
                # cvzone.cornerRect(img, (x1, y1, w, h), l=9, rt=5)
                
                print("person detected")
                cv2.rectangle(decoded_frame, (x1, y1), (x2, y2), (255, 0, 255), 3)
                cv2.putText(decoded_frame, f'{currentClass} {conf}', (max(0, x1), max(35, y1)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 1, cv2.LINE_AA)

    count+=1

    if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

    # Check for client disconnect
    if not frame_bytes:
        break

# Release resources
server_socket.close()
cv2.destroyAllWindows()
