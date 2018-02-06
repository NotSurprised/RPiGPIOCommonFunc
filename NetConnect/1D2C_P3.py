import socket
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT) #IN4
GPIO.setup(23, GPIO.OUT) #IN3
GPIO.setup(24, GPIO.OUT) #IN2
GPIO.setup(25, GPIO.OUT) #IN1


bind_ip = "192.168.0.100" #car p2
bind_port = 8888

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((bind_ip, bind_port))

try:
        

	while True:
		client.send("hi, I'm 192.168.0.102") #this car
		print("Listening on %s:%d" % (bind_ip, bind_port))
		data = client.recv(1024)

		if data == b'w': #wasd
			print ("receive[%s]" % data)
			GPIO.output(18, False)
			GPIO.output(23, True)
			GPIO.output(24, True)
			GPIO.output(25, False)
		elif data == b's': 
			print ("receive[%s]" % data)
			GPIO.output(18, True)
			GPIO.output(23, False)
			GPIO.output(24, False)
			GPIO.output(25, True)                       
		elif data == b'a': 
			print ("receive[%s]" % data)
			GPIO.output(18, True)
			GPIO.output(23, False)
			GPIO.output(24, True)
			GPIO.output(25, False)
		elif data == b'd': 
			print ("receive[%s]" % data)
			GPIO.output(18, False)
			GPIO.output(23, True)
			GPIO.output(24, False)
			GPIO.output(25, True)
		elif data == b'x':
			print ("receive[%s]" % data)
			GPIO.output(18, False)
			GPIO.output(23, False)
			GPIO.output(24, False)
			GPIO.output(25, False)
			
except KeyboardInterrupt:
        client.close()
        GPIO.cleanup()
