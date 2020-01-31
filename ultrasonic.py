import RPi.GPIO as gpio
import time
import socket

host = '192.168.2.5'
port = 8888

gpio.setmode(gpio.BCM)
trig = 13
echo = 19
gpio.setup(trig, gpio.OUT)
gpio.setup(echo, gpio.IN)
gpio.setwarnings(False)
count = 0
cnt=0
#start = 0
while True:
	while True:
		gpio.output(trig,False)
		time.sleep(0.5)
		gpio.output(trig,True)
		time.sleep(0.000001)
		gpio.output(trig,False)
		while gpio.input(echo) == 0:
			start = time.time()
		while gpio.input(echo) == 1:
			end = time.time()
		distance = (end - start) * 17000
		distance = round(distance,2)
		print 'Dist =', distance
		if distance < 50:
			count += 1
			if count% 20 == 0:
				client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
				client_socket.connect((host,port))
				print "connected"
				client_socket.sendall("recog".encode())
				print "send"
				data = client_socket.recv(1024)
				print 'Received',repr(data.decode())
				pass
		else:
			count = 0
			pass

#gpio.cleanup()
