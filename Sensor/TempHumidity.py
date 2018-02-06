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

while True:
    currentTime = time.strftime("%H:%M:%S")
    humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO26)

    if humidity is not None and temperature is not None:
        heatstrokeformula = temperature + humidity * 0.1
        print(currentTime,'-> Temp={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity))
        print('%s -> coefficient={0:0.1f}'.format(heatstrokeformula) % currentTime)
        if (temperature >= 31):
            GPIO.output(pinG, False)
            GPIO.output(pinY, False)
            GPIO.output(pinR, True)
            GPIO27.start(50)
            GPIO27.ChangeFrequency(1046)
        if (temperature > 27 and temperature <=30):
            GPIO.output(pinG, False)
            GPIO.output(pinR, False)
            GPIO.output(pinY, True)
            GPIO27.stop()
        if (temperature > 20 and temperature <= 27):
            GPIO.output(pinY, False)
            GPIO.output(pinR, False)
            GPIO.output(pinG, True)
            GPIO27.stop()
    else:
        print('Failed to get reading. Try again!')
    time.sleep(2)

    


    
GPIO.output(pinG, False)
GPIO.output(pinY, False)
GPIO.output(pinR, False)
pinG.stop()
pinY.stop()
pinR.stop()
GPIO.cleanup()
