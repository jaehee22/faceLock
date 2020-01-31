cnt1 = 0
cnt2 = 0
cnt3 = 0

import socket
from imp import reload
import os
import RPi.GPIO as GPIO
import time

HOST = "192.168.2.5"
PORT = 8888

global face_id

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('socket create')
s.bind ((HOST, PORT))
print ('socket bind complete')
s.listen(2)
print ('socket now listening')

def do_some(input_button):
	global cnt1
	global cnt2
	global cnt3
	global face_id
	while True:
		#도어락 제어
		if input_button == "open":
			input_button = "open"
			GPIO.setmode(GPIO.BCM)
			door = 24
			GPIO.setup(door,GPIO.OUT,initial=GPIO.LOW)
			GPIO.output(door,GPIO.HIGH)
                	time.sleep(0.5)
               		GPIO.output(door,GPIO.LOW)

		#새로운 사용자 등록
		elif input_button == "new":
			if cnt1 == 0:
				import newUser
				face_id = newUser.face_id
				print newUser.face_id
				cnt1 = 1
			else:
				global newUser
				reload(newUser)
				face_id = newUser.face_id
			input_button = "new"

		#얼굴인식	
		elif input_button == "recog":
			if cnt3 == 0:
                         	import UserRecognition
                                cnt3 = 1
 			else:
				global UserRecognition
                        	reload(UserRecognition)
			input_button = "server"

		return input_button

while True:
	conn, addr = s.accept()
	print ("Connected by ",addr)

	data = conn.recv(1024)

	data = data.decode("utf-8").strip()

	if not data: break
	print ("doit: "+ data)

	res = do_some(data)

	print ("do :" + res)
	conn.sendall(res.encode("utf-8"))

	conn.close()

s.close()
