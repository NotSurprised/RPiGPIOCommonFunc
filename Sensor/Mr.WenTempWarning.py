#-*-coding:utf-8-*-
import RPi.GPIO as GPIO
import time
import Adafruit_DHT
import fbchat

client=fbchat.Client("*******@*******","*******")
friends=client.getUsers("NotSurprised")
friend=friends[0]

sensor = Adafruit_DHT.DHT11
GPIO26 = 26
humidityTrigger=False

try:
    while True :
        currentTime =time.strftime("%H:%M:%S") 
        humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO26) 
        if humidity is not None and humidity < 100:
            print(currentTime, '-> Humidity={0:0.1f}%'.format(humidity))
            if humidity >= 80 and humidityTrigger==False:
                humidityTrigger=True
                sent=client.send(friend.uid,"Mr.Wen,the Humidity is {0:0.1f}%, open your airconditioner!".format(humidity))
                if sent:
                    print("Messages have been sent.")
            elif humidity<80 and humidityTrigger==True:
                humidityTrigger=False
        elif humidity is not None and humidity >= 100:
            print("unexpect error, please wait...")
        else:
            print("something failed, please wait..." )
        time.sleep(2)
        
except KeyboardInterrupt:
	pass
