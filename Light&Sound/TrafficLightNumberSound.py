import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) #BOARD or BCM
pin1G = 4 #point to PIN#03 = GPIO2
pin1Y = 3
pin1R = 2
pin2G = 5 #point to PIN#03 = GPIO2
pin2Y = 6
pin2R = 7
GPIO17 = 17

setGPIOs1 = [8,9,10,11,12,13,14,15]

GPIOS = []

state = [[0,1,1,1,1,1,1,1],   #show num. 0
         [0,0,0,1,1,1,0,0],   #show num. 1
         [1,0,1,1,1,0,1,1],   #show num. 2
         [1,0,1,1,1,1,1,0],   #show num. 3
         [1,1,0,1,1,1,0,0],   #show num. 4
         [1,1,1,0,1,1,1,0],   #show num. 5
         [1,1,1,0,1,1,1,1],   #show num. 6
         [0,0,1,1,1,1,0,0],   #show num. 7
         [1,1,1,1,1,1,1,1],   #show num. 8
         [1,1,1,1,1,1,0,0],   #show num. 9
         [0,0,0,0,0,0,0,0]]   #no show

for i in range(0, 28, 1):
    GPIOS.append(i)
    GPIO.setup(GPIOS[i], GPIO.OUT)

ALLcount = 0

GPIO17 = GPIO.PWM(GPIO17, 440)
GPIO17.start(50)

for ALLcount in range(3):
    GPIO17.ChangeFrequency(10)
    GPIO.output(pin1R, True)
    GPIO.output(pin2G, True)
    time.sleep(10)
    GPIO.output(pin2G, False)
    for i in range(5):
        for j in range(0, len(setGPIOs1), 1):
            GPIO.output(GPIOS[setGPIOs1[j]], state[5-i][j])
        GPIO.output(pin2Y, True)
        time.sleep(0.5)
        for j in range(0, len(setGPIOs1), 1):
            GPIO.output(GPIOS[setGPIOs1[j]], state[10][j])
        GPIO.output(pin2Y, False)
        time.sleep(0.5)
    GPIO.output(pin2R, True)
    for i in range(5):
        for j in range(i):
            GPIO17.ChangeFrequency(1046)
            k = (5-i)/5
            time.sleep(k-0.1)
            GPIO17.ChangeFrequency(10)
            time.sleep(0.1)
    GPIO.output(pin1R, False)
    GPIO.output(pin1G, True)
    time.sleep(10)
    GPIO.output(pin1G, False)
    for i in range(5):
        for j in range(0, len(setGPIOs1), 1):
            GPIO.output(GPIOS[setGPIOs1[j]], state[5-i][j])
        GPIO.output(pin1Y, True)
        time.sleep(0.5)
        for j in range(0, len(setGPIOs1), 1):
            GPIO.output(GPIOS[setGPIOs1[j]], state[10][j])
        GPIO.output(pin1Y, False)
        time.sleep(0.5)
    GPIO.output(pin1R, True)
    for i in range(5):
        for j in range(i):
            GPIO17.ChangeFrequency(1046)
            k = (5-i)/5
            time.sleep(k-0.1)
            GPIO17.ChangeFrequency(10)
            time.sleep(0.1)
    GPIO.output(pin2R, False)
GPIO.output(pin1G, False)
GPIO.output(pin1Y, False)
GPIO.output(pin1R, False)
GPIO.output(pin2G, False)
GPIO.output(pin2Y, False)
GPIO.output(pin2R, False)
pin1G.stop()
pin1Y.stop()
pin1R.stop()
pin2G.stop()
pin2Y.stop()
pin2R.stop()
GPIO.cleanup()

