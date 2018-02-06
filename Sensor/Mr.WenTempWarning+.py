#-*-coding:utf-8-*-
import RPi.GPIO as GPIO
import Adafruit_DHT
import fbchat
import time
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

client=fbchat.Client("*******@*******","*******")
friends=client.getUsers("NotSurprised")
friend=friends[0]

sensor = Adafruit_DHT.DHT11
GPIO26 = 26
humidityTrigger=False

try:
    while True :
        fileCreatTime=int(time.time())
        print(fileCreatTime)
        fileCreatTimeRead =time.strftime("%H:%M:%S")
        f = open("%s.txt"%fileCreatTimeRead, "w", encoding="UTF-8")
        currentTime=int(time.time())
        
        while currentTime-fileCreatTime <= 60:
            currentTime=int(time.time())
            currentTimeRead =time.strftime("%H:%M:%S")
            humidity, temperature = Adafruit_DHT.read_retry(sensor, GPIO26) 
            if temperature is not None and humidity is not None and humidity < 100:
                print(currentTimeRead,"-> Temp={0:0.1f}*C Humidity={1:0.1f}%".format(temperature, humidity))
                f.write(currentTimeRead+"-> Temp={0:0.1f}*C Humidity={1:0.1f}% \n".format(temperature, humidity))
                
                if humidity >= 80 and humidityTrigger==False:
                    humidityTrigger=True
                    sent=client.send(friend.uid,"Mr.Wen,the Humidity is {0:0.1f}%, open your airconditioner!".format(humidity))
                    if sent:
                        print("Messages have been sent.")
                        
                elif humidity < 80 and humidityTrigger==True:
                    humidityTrigger=False
            elif temperature is not None and humidity is not None and humidity >= 100:
                print("unexpect error, please wait...")
            else:
                print("something failed, please wait..." ) 
            time.sleep(2)
            
        f.close()
        
        #-- Email的收件人與寄件人address--
        emailfrom = "pftheater@gmail.com"
        emailto = "*******@*******"
        #--Email附件檔案Attachment--
        fileToSend = fileCreatTimeRead+'.txt'
        print("The file you are trying to send for is"+fileToSend)
        username=emailfrom #--寄信的SMTP的帳號--
        password="*******" #--寄信的SMTP的密碼--
        
        msg = MIMEMultipart()
        msg["From"]=emailfrom
        msg["To"]=emailto
        #--Email的主旨Subject--
        msg["Subject"]="From "+fileCreatTimeRead+" after 5min's Temp & Humi."
        
        #--Email的信件內容Message--
        contents=MIMEText("As Title.\n", _charset="UTF-8")
        msg.attach(contents)
        
        #---Test for Text Message---
        ctype, encoding = mimetypes.guess_type(fileToSend)
        if ctype is None or encoding is not None:
                ctype="application/octet-stream"
        maintype, subtype=ctype.split("/",1)
        
        fp = open(fileToSend,"rb")
        attachment = MIMEBase(maintype,subtype)
        attachment.set_payload(fp.read())
        fp.close()
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition","attachment",filename=fileToSend)
        msg.attach(attachment)
        
        #---寄件的Gmail SMTP mail server---
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.ehlo()
        server.starttls()
        
        server.login(username,password)
        server.sendmail(emailfrom,emailto,msg.as_string())
        server.quit()
        print("email have been sent.")
        
except KeyboardInterrupt:
	pass
f.close()
