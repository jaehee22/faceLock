import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
door = 23

GPIO.setup(door,GPIO.OUT,initial=GPIO.LOW)

try:
	while True:
		GPIO.output(door,GPIO.HIGH)
		time.sleep(0.5)
		GPIO.output(door,GPIO.LOW)
		time.sleep(0.5)
except KeyboardInterrupt:
	pass

GPIO.cleanup()
