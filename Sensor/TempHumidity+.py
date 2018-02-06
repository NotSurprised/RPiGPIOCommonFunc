import RPi.GPIO as GPIO
import Adafruit_DHT
import time

GPIO.setmode(GPIO.BCM) #BOARD or BCM
pinG = 4 #point to PIN#03 = GPIO2
pinY = 3
pinR = 2
GPIO27 = 27
GPIO26 = 26
GPIO.setup(pinG, GPIO.OUT)
GPIO.setup(pinY, GPIO.OUT)
GPIO.setup(pinR, GPIO.OUT)
GPIO.setup(GPIO27, GPIO.OUT)
GPIO27 = GPIO.PWM(GPIO27, 440)
GPIO27.stop
sensor = Adafruit_DHT.DHT11

GPIO.output(pinG, False)
GPIO.output(pinY, False)
GPIO.output(pinR, False)

setGPIOs1 = [8,9,10,11,12,13,14,15]
setGPIOs2 = [16,17,18,19,20,21,22,23]
GPIOS = []
for i in range(0, 28, 1):
    GPIOS.append(i)
    GPIO.setup(GPIOS[i], GPIO.OUT)

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

danger=0

while True:
    currentTime = time.strftime("%H:%M:%S")
    humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO26)

    if humidity is not None and temperature is not None:
        heatstrokeformula = temperature + humidity * 0.1
        print(currentTime,'-> Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
        print('%s -> coefficient={0:0.1f}'.format(heatstrokeformula) % currentTime)
        j = (heatstrokeformula)/10
        k = (heatstrokeformula)%10
        for l in range(0, len(setGPIOs1), 1):
            GPIO.output(GPIOS[setGPIOs1[l]], state[int(j)][l])
        for m in range(0, len(setGPIOs2), 1):
            GPIO.output(GPIOS[setGPIOs2[m]], state[int(k)][m])
        if (heatstrokeformula >= 40):
            GPIO.output(pinG, False)
            GPIO.output(pinY, False)
            danger=1
            GPIO27.start(50)
            GPIO27.ChangeFrequency(1046)
        if (heatstrokeformula >= 35 and heatstrokeformula <= 39):
            GPIO.output(pinG, False)
            GPIO.output(pinY, False)
            GPIO.output(pinR, True)
            GPIO27.stop()
            danger=0
        if (heatstrokeformula >= 30 and heatstrokeformula <= 34):
            GPIO.output(pinG, False)
            GPIO.output(pinR, False)
            GPIO.output(pinY, True)
            GPIO27.stop()
            danger=0
        if (heatstrokeformula <= 29):
            GPIO.output(pinY, False)
            GPIO.output(pinR, False)
            GPIO.output(pinG, True)
            GPIO27.stop()
            danger=0
    else:
        print('Failed to get reading. Try again!')
    
    if (danger==1):
        GPIO.output(pinR, True)
        time.sleep(0.5)
        GPIO.output(pinR, False)
        time.sleep(0.5)
    else:
        time.sleep(1)
    
GPIO.output(pinG, False)
GPIO.output(pinY, False)
GPIO.output(pinR, False)
pinG.stop()
pinY.stop()
pinR.stop()
GPIO.cleanup()
