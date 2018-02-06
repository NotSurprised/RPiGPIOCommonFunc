#-*-coding:utf-8-*-

import Adafruit_DHT
import fbchat
import time
import smtplib
import mimetypes
import re
import json
import codecs
from pymongo import MongoClient
from bokeh.plotting import figure, output_file, show
from urllib.request import urlopen

sensor = Adafruit_DHT.DHT11
GPIO2 = 2
humiditylock=False

#FBlogin
client=fbchat.Client("*********@*******","*********")
friends=client.getUsers("Notsurprised")
friend=friends[0]

#DB
clientdb = MongoClient('localhost',27017)
db = clientdb.dht11
collect=db.detectdata

#areachart
time_forchart=[]
temperature_forchart=[]
humidity_forchart=[]

#IPinfo
reader = codecs.getreader("utf-8")
url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(reader(response))
IP=data['ip']
hostname=data['hostname']
city = data['city']
region=data['region']
country=data['country']
location=data['loc']
org=data['org']

try:
    sent=client.send(friend.uid,"Start detecting.")
    while True :
        #read and write
        fileCreatTime=int(time.time())
        fileCreatTimeRead =time.strftime("%H-%M-%S")
        f = open('%s.txt' % fileCreatTimeRead, 'w', encoding = 'UTF-8')

        currentTime=int(time.time())
        time_forchart[:]=[]
        temperature_forchart[:]=[]
        humidity_forchart[:]=[]
        while currentTime-fileCreatTime<60:
            currentTime=int(time.time())
            currentTimeRead =time.strftime("%H:%M:%S")
            timecount = (currentTime-fileCreatTime)/5
            humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO2)
            
            if temperature is not None and humidity is not None and humidity <= 100:
                print(currentTimeRead + ' from {2} at {3}\n\t-> temperature={0:0.1f}*C Humidity={1:0.1f}%'.format(temperature, humidity, org, location))
                f.write(currentTimeRead + ' from {2} at {3}\n\t-> temperature={0:0.1f}*C Humidity={1:0.1f}% \n'.format(temperature, humidity, org, location) + '\n')
                postintodb={"time":currentTimeRead,"temperature":temperature, "humidity":humidity,"location":str(org)+"("+str(location)+")"}
                post_id = collect.insert_one(postintodb).inserted_id
                
                time_forchart.append(int(timecount))
                temperature_forchart.append(float(temperature))
                humidity_forchart.append(float(humidity))
                
                if humidity >= 80 and humiditylock==False:
                    humiditylock=True
                    sent=client.send(friend.uid,"Mr.Wen,the Humidity is {0:0.1f}%, open your airconditioner!".format(temperature, humidity))
                    if sent:
                        print("Messages have been sent.")
                elif humidity<80 and humiditylock==True:
                    humiditylock=False
            elif humidity is not None and humidity >= 100:
                print("unexpect error, please wait...")
            else:
                print("something failed, please wait..." )
            time.sleep(2)
            
        f.close()
        
        output_file('%s.html' % fileCreatTimeRead, title="Mr.Wen's Temperature and Humidity Records")
        
        p=figure(title="Mr.Wen's Temperature and Humidity Records", x_axis_label='time(min.)', y_axis_label='values') 
        print (temperature_forchart)
        print (humidity_forchart)
        p.line(time_forchart,temperature_forchart,legend="Temp",line_width=2,line_color="red")
        p.line(time_forchart,humidity_forchart,legend="Humidity",line_width=2,line_color="blue")
        
        show(p)
        
except KeyboardInterrupt:
    pass
f.close()
print ("\n all the data in database \n")
for post in collect.find():
    print(post)
