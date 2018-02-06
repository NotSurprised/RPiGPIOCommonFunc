import socket
import RPi.GPIO as GPIO
import time
import threading

class Right (threading.Thread):
    def run(self):
        while rightlock==True:
            GPIO.output(GPIOpinL, False)
            GPIO.output(GPIOpinR, True)
            time.sleep(1)
            GPIO.output(GPIOpinR, False)
            time.sleep(1)

class Left (threading.Thread):
    def run(self):
        while leftlock==True:
            GPIO.output(GPIOpinR, False)
            GPIO.output(GPIOpinL, True)
            time.sleep(1)
            GPIO.output(GPIOpinL, False)
            time.sleep(1)

class Back (threading.Thread):
    def run(self):
        while backlock==True:
            GPIO.output(GPIOpinR, True)
            GPIO.output(GPIOpinL, True)
            time.sleep(1)
            GPIO.output(GPIOpinR, False)
            GPIO.output(GPIOpinL, False)
            time.sleep(1)
            
class Song (threading.Thread):
    def run(self):
        while songlock==True:
            GPIOsong.start(50)
            for i in range(0, len(majorchord)):
                GPIOsong.ChangeFrequency(tone[majorchord[i]][3])
                if i != (len(majorchord)-1):
                    time.sleep(0.5)
                else:
                    GPIOsong.stop()
                    time.sleep(1)

GPIO.setmode(GPIO.BCM)

GPIOpinR = 2
GPIOpinL = 3
GPIOsong = 17

GPIO.setup(GPIOpinR, GPIO.OUT)
GPIO.setup(GPIOpinL, GPIO.OUT)
GPIO.setup(GPIOsong, GPIO.OUT)

GPIOsong = GPIO.PWM(GPIOsong, 440)

GPIO.setup(18, GPIO.OUT)    #IN4
GPIO.setup(23, GPIO.OUT)    #IN3
GPIO.setup(24, GPIO.OUT)    #IN2
GPIO.setup(25, GPIO.OUT)    #IN1

GPIO.output(GPIOpinR, False)
GPIO.output(GPIOpinL, False)

#audio frequency
tone = [[0,0,0,0,0],
        [66, 131, 262, 523, 1046], #Do
        [74, 147, 294, 587, 1175], #Re
        [83, 165, 330, 659, 1318], #Mi
        [88, 175, 349, 698, 1397], #Fa
        [98, 196, 392, 784, 1568], #So
        [110, 220, 440, 880, 1760],#La
        [124, 247, 494, 988, 1976]]#Si

majorchord = [1,1,5,5,6,6,5,5,
              4,4,3,3,2,2,1,1,
              5,5,4,4,3,3,2,2,
              5,5,4,4,3,3,2,2,
              1,1,5,5,6,6,5,5,
              4,4,3,3,2,2,1,1]

bind_ip = "192.168.0.100"
bind_port = 8888

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((bind_ip, bind_port))
server.listen(5)
print("Listening on %s : %d" % (bind_ip, bind_port))

try:
    client,addr = server.accept()
    print("Accepted connection from : %s : %d" % (addr[0], addr[1]))
    data = b'o'
    data_old = b'o'
    while True:
        data_old = data
        data = client.recv(1024)
        if data == b'z': #forwarding
            print("receive[%s]" % data)
            GPIO.output(GPIOpinR, False)
            GPIO.output(GPIOpinL, False)
            GPIO.output(18, True)
            GPIO.output(23, False)
            GPIO.output(24, True)
            GPIO.output(25, False)

            rightlock = False
            leftlock = False
            backlock = False
            songlock = True


            Right().deamon = True
            Right().start()
            Left().deamon = True
            Left().start()
            Back().deamin = True
            Back().start()

            GPIO.output(GPIOpinR, False)
            GPIO.output(GPIOpinL, False)

            if data_old == b's' or data_old == b'o':
                Song().start()

        elif data == b'x': #backward
            print("receive[%s]" % data)

            GPIO.output(18, False)
            GPIO.output(23, True)
            GPIO.output(24, False)
            GPIO.output(25, True)

            rightlock = False
            leftlock = False
            backlock = True
            songlock = True

            Right().deamon = True
            Right().start()
            Left().deamon = True
            Left().start()
            Back().start()

            if data_old == b's' or data_old == b'o':
                Song().start()

        elif data == b'c': #turn left
            print("receive[%s]" % data)
            GPIO.output(18, False)
            GPIO.output(23, True)
            GPIO.output(24, True)
            GPIO.output(25, False)

            rightlock = False
            leftlock = True
            backlock = False
            songlock = True

            
            Right().deamon = True
            Right().start()
            Left().start()
            Back().deamon = True
            Back().start()

            if data_old == b's' or data_old == b'o':
                Song().start()

        elif data == b'v': #turn right
            print("receive[%s]" % data)
            GPIO.output(18, True)
            GPIO.output(23, False)
            GPIO.output(24, False)
            GPIO.output(25, True)

            rightlock = True
            leftlock = False
            backlock = False
            songlock = True

            Right().start()
            Left().deamon = True
            Left().start()
            Back().deamon = True
            Back().start()

            if data_old == b's' or data_old == b'o':
                Song().start()

        elif data == b's': #stop
            print("receive[%s]" % data)
            GPIO.output(18, False)
            GPIO.output(23, False)
            GPIO.output(24, False)
            GPIO.output(25, False)

            rightlock = False
            leftlock = False
            backlock = False
            songlock = False

            Right().deamon = True
            Right().start()
            Left().deamon = True
            Left().start()
            Back().deamon = True
            Back().start()
            Song().deamon = True
            Song().start()

            GPIO.output(GPIOpinR, True)
            GPIO.output(GPIOpinL, True)

            GPIOsong.stop()

except KeyboardInterrupt:
    client.close()
    GPIOsong.stop()
    GPIO.cleanup()
