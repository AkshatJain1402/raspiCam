import cv2
import numpy
from flask import Flask, render_template, Response, stream_with_context, request
app=Flask('__name__')

video=cv2.VideoCapture(0)
global fps
fps=0
while True:
	
	ret,frame=video.read()
	if not ret:
		break
	fps=fps+1
	output_filePath=f'/home/kali/liveStream/demo{fps}.jpg'
	#try:
	#	cv2.imwrite(output_filePath,frame)
	#	print('done')
	#except Exception as e:
	#	print('error',e)
	if not ret:
		print('not ret')
		break
	else:
            ret,buffer=cv2.imencode('.jpeg',frame)
            frame=buffer.tobytes()
            yield (b' --frame\r\n' b'Content-type: imgae/jpeg\r\n\r\n' + frame +b'\r\n')	

@app.route('/camera')
def camera():
	return render_template('camera.html')

@app.route('video_feed')
def video_feed():
	return Response(video_stream(),mimetype='multipart.x-mixed-replace; boundary=frame$')

app.run(host='0.0.0.0',port='5000', debug=False)

#	cv2.imshow('video',frame)
