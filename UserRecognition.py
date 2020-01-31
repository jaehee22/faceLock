import cv2
import numpy as np
import os
import sys
import pyrebase
import time
from datetime import datetime
import json
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
door = 24

GPIO.setup(door,GPIO.OUT,initial=GPIO.LOW)


recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "haarcascade/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);
font = cv2.FONT_HERSHEY_SIMPLEX

config ={
        "apiKey":"faceKey.json",
        "authDomain":"facelock-39a53.firebaseapp.com",
        "databaseURL":"https://facelock-39a53.firebaseio.com/",
        "storageBucket":"facelock-39a53.appspot.com"
}


id = 0
count = 0

names = ['Guest','1', '2', '3', '4', '5', '6', '7', '8', '9', '10']

cam = cv2.VideoCapture(-1)
cam.set(3,640)
cam.set(4,480)

minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

Hi = "Who"

while True:
	ret, img = cam.read()
	img = cv2.flip(img, -1)
	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

	faces = faceCascade.detectMultiScale(
		gray,
		scaleFactor = 1.2,
		minNeighbors = 5,
		minSize = (int(minW), int(minH)),
		)

	for(x,y,w,h) in faces:
		cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
		id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
		if (confidence < 57):
			id = names[id]
			confidence = " {0}%".format(round(100 - confidence))
			cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)
			print 'Hi User!'
			Hi = "Hi"
			#doorLock open code
			GPIO.output(door,GPIO.HIGH)
                	time.sleep(0.5)
                	GPIO.output(door,GPIO.LOW)

			break

		elif(confidence < 100 and confidence > 57):
			id = "unknown"
			count += 1
			#print round(100-confidence)
			print count
			if (count%33 == 0):
				print 'Who are you?'
				Hi = "Hi"
				for i in range(1,50):
					g = str(i)
					if  os.path.exists("./Guestdata/Guest."+g+".jpg") == True:
						i+=1
					else:
						import dbGuest
						cv2.imwrite("./Guestdata/Guest."+g+".jpg", img)
						firebase = pyrebase.initialize_app(config)
                               			uploadfile = "Guestdata/Guest."+g+".jpg"
                                		s = os.path.splitext(uploadfile)[1]
                              			filename = g+".jpg"
                               			storage = firebase.storage()

	                       			storage.child("GuestList/"+filename).put(uploadfile)
        	                		fileUrl = storage.child("GuestList/"+filename).get_url(1)
						print (fileUrl)
						break
#	if Hi == 'Hi':
#		break
	#cv2.putText(img, str(id), (x+5, y-5), font, 1, (255,255,255), 2)
	cv2.imshow('camera', img)

	if Hi == 'Hi':
		break
	k = cv2.waitKey(10) & 0xff
	if k == 27:
		break

cam.release()
cv2.destroyAllWindows()
