import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM) #BOARD or BCM
pin1G = 4 #point to PIN#03 = GPIO2
pin1Y = 3
pin1R = 2
pin2G = 18 #point to PIN#03 = GPIO2
pin2Y = 15
pin2R = 14
GPIO.setup(pin1G, GPIO.OUT)
GPIO.setup(pin1Y, GPIO.OUT)
GPIO.setup(pin1R, GPIO.OUT)
GPIO.setup(pin2G, GPIO.OUT)
GPIO.setup(pin2Y, GPIO.OUT)
GPIO.setup(pin2R, GPIO.OUT)
ALLcount = 0

for ALLcount in range(3):
    GPIO.output(pin1R, True)
    GPIO.output(pin2G, True)
    time.sleep(10)
    GPIO.output(pin2G, False)
    for Ycount in range(5):
        GPIO.output(pin2Y, True)
        time.sleep(0.5)
        GPIO.output(pin2Y, False)
        time.sleep(0.5)
    GPIO.output(pin2R, True)
    time.sleep(1)
    GPIO.output(pin1R, False)
    GPIO.output(pin1G, True)
    time.sleep(10)
    GPIO.output(pin1G, False)
    for Ycount in range(5):
        GPIO.output(pin1Y, True)
        time.sleep(0.5)
        GPIO.output(pin1Y, False)
        time.sleep(0.5)
    GPIO.output(pin1R, True)
    time.sleep(1)
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

