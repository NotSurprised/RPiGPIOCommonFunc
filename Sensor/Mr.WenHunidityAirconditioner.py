#-*-coding:utf-8-*-
import RPi.GPIO as GPIO
import time
import Adafruit_DHT

sensor = Adafruit_DHT.DHT11
GPIO2 = 2
humidityTrigger=False

GPIO.setmode(GPIO.BCM)
GPIO4 = 4
GPIO.setup(GPIO4, GPIO.OUT)

try:
    while True :
        currentTime =time.strftime("%H:%M:%S") 
        humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO2) 
        if humidity is not None and humidity < 100:
            print(currentTime, '-> Humidity={0:0.1f}%'.format(humidity))
            if humidity >= 80 and humidityTrigger==False:
                humidityTrigger=True
                print("Limit 5 dollers.")
                GPIO.output(GPIO4,False)
                time.sleep(20)
                GPIO.output(GPIO4,True)
                print("Limit has been reach.")
            elif humidity<80 and humidityTrigger==True:
                humidityTrigger=False
        elif humidity is not None and humidity >= 100:
            print("unexpect error, please wait...")
        else:
            print("something failed, please wait..." )
        time.sleep(2)
        
except KeyboardInterrupt:
	pass
