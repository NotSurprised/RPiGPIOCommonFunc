import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)#point to PIN#03 = GPIO2
pin1G = 4 #La
pin1Y = 3 #So
pin1R = 2 #Fa
pin2G = 5 #Mi
pin2Y = 6 #Re
pin2R = 7 #Do
GPIO17 = 17 #major chord

GPIOS = []
for i in range(0, 28, 1):
    GPIOS.append(i)
    GPIO.setup(GPIOS[i], GPIO.OUT)
    
GPIO17 = GPIO.PWM(GPIO17,440)
GPIO17.start(50)
#audio frequency
tone = [[0,0,0,0,0],
        [66, 131, 262, 523, 1046], #Do
        [74, 147, 294, 587, 1175], #Re
        [83, 165, 330, 659, 1318], #Mi
        [88, 175, 349, 698, 1397], #Fa
        [98, 196, 392, 784, 1568], #So
        [110, 220, 440, 880, 1760],#La
        [124, 247, 494, 988, 1976]]#Si

majorchord = [1,1,5,5,6,6,5,
              4,4,3,3,2,2,1,
              5,5,4,4,3,3,2,
              5,5,4,4,3,3,2,
              1,1,5,5,6,6,5,
              4,4,3,3,2,2,1]

for i in range(0, len(majorchord)): #Play tone
    if majorchord[i] == 1:
        GPIO.output(pin2R, True)
    elif majorchord[i] == 2:
        GPIO.output(pin2Y, True)
    elif majorchord[i] == 3:
        GPIO.output(pin2G, True)
    elif majorchord[i] == 4:
        GPIO.output(pin1R, True)
    elif majorchord[i] == 5:
        GPIO.output(pin1Y, True)
    elif majorchord[i] == 6:
        GPIO.output(pin1G, True)
    GPIO17.ChangeFrequency(tone[majorchord[i]][3])
    if (i+1)%7 == 0:
        time.sleep(0.5)
        GPIO17.ChangeFrequency(10)
        time.sleep(0.5)
    elif i !=(len(majorchord)-1):
        time.sleep(0.5) #delay a note for beat * 0.5s
    else:
        time.sleep(2) #control the temple
    GPIO.output(pin1G, False)
    GPIO.output(pin1Y, False)
    GPIO.output(pin1R, False)
    GPIO.output(pin2G, False)
    GPIO.output(pin2Y, False)
    GPIO.output(pin2R, False)
GPIO.output(pin1G, False)
GPIO.output(pin1Y, False)
GPIO.output(pin1R, False)
GPIO.output(pin2G, False)
GPIO.output(pin2Y, False)
GPIO.output(pin2R, False)
GPIO17.stop()
GPIO.cleanup()
