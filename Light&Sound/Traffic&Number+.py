import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) #BOARD or BCM
pin1G = 4 #point to PIN#03 = GPIO2
pin1Y = 3
pin1R = 2
pin2G = 5 #point to PIN#03 = GPIO2
pin2Y = 6
pin2R = 7

setGPIOs1 = [8,9,10,11,12,13,14,15]
setGPIOs2 = [16,17,18,19,20,21,22,23]

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
         [0,0,0,0,0,0,0,0],   #no show
         [1,0,0,0,0,1,0,1],   #show n
         [1,0,0,0,1,1,1,1]]   #show o.

for i in range(0, 28, 1):
    GPIOS.append(i)
    GPIO.setup(GPIOS[i], GPIO.OUT)

ALLcount = 0

for ALLcount in range(2):
    GPIO.output(pin1R, True)
    GPIO.output(pin2R, True)
    for i in range(25):
        j = (25-i)/10
        k = (25-i)%10
        for l in range(0, len(setGPIOs1), 1):
            GPIO.output(GPIOS[setGPIOs1[l]], state[int(j)][l])
        for m in range(0, len(setGPIOs2), 1):
            GPIO.output(GPIOS[setGPIOs2[m]], state[k][m])
        
        if(i>=5 and i<15):
            GPIO.output(pin2R, False)
            GPIO.output(pin2G, True)        
        if(i>=15 and i<20):
            GPIO.output(pin2G, False)
            GPIO.output(pin2Y, True)
        if(i>=20):
            GPIO.output(pin2Y, False)
            GPIO.output(pin2R, True)
        for n in range(2):
            GPIO.output(GPIOS[setGPIOs2[4]], state[0][0])
            time.sleep(0.25)
            GPIO.output(GPIOS[setGPIOs2[4]], state[0][1])
            time.sleep(0.25)
    for l in range(0, len(setGPIOs1), 1):
        GPIO.output(GPIOS[setGPIOs1[l]], state[11][l])
    for m in range(0, len(setGPIOs2), 1):
        GPIO.output(GPIOS[setGPIOs2[m]], state[12][m])
    GPIO.output(pin1R, False)
    GPIO.output(pin2R, True)
    GPIO.output(pin1G, True)
    for n in range(20):
            GPIO.output(GPIOS[setGPIOs2[4]], state[0][0])
            time.sleep(0.25)
            GPIO.output(GPIOS[setGPIOs2[4]], state[0][1])
            time.sleep(0.25)
    GPIO.output(pin1G, False)
    GPIO.output(pin1Y, True)
    for n in range(10):
            GPIO.output(GPIOS[setGPIOs2[4]], state[0][0])
            time.sleep(0.25)
            GPIO.output(GPIOS[setGPIOs2[4]], state[0][1])
            time.sleep(0.25)
    GPIO.output(pin1Y, False)
    
for l in range(0, len(setGPIOs1), 1):
    GPIO.output(GPIOS[setGPIOs1[l]], state[10][l])
for m in range(0, len(setGPIOs2), 1):
    GPIO.output(GPIOS[setGPIOs2[m]], state[10][m])
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

