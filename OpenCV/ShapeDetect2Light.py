# import the necessary packages
# -*- coding: utf-8 -*-
import cv2
import numpy as np
from gtts import gTTS
import os
import speech_recognition as sr
import RPi.GPIO as GPIO

class ShapeDetector:
	def __init__(self):
		pass
 
	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)

		# if the shape is a triangle, it will have 3 vertices
		if len(approx) == 3:
			shape = "triangle"
 
		# return the name of the shape
		return shape

GPIO.setmode(GPIO.BCM) #BOARD or BCM
pin2 = 2 #point to PIN#02 = GPIO2
GPIO.setup(pin2, GPIO.OUT)
GPIO.output(pin2, False)

r = sr.Recognizer()
r.energy_threshold =  4000    # threshold for filtering noise

cap = cv2.VideoCapture(0)

missionComplete=0

while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    #Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(5,5),0)
    ret, thresh_img = cv2.threshold(blur,91,255,cv2.THRESH_BINARY)
    circles = cv2.HoughCircles(gray, cv2.cv.CV_HOUGH_GRADIENT, 1.2, 75)

    #in openCV2 cv2 only return 2 value but at openCV3 for 3
    #contours,_  will be _,contours,_
    contours,_ = cv2.findContours(thresh_img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    print ("there are "+str(len(contours))+"contours")
    cnt = contours[0]
    print ("there are "+str(len(cnt))+"points in contours[0]")
    sd = ShapeDetector()
    triangle=0
    circle=0
    if circles is not None:
        print("OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO")
        circle=1
    for c in contours:
        cv2.drawContours(frame,[c],-1,(0,255,0),3)
        shape = sd.detect(c)
        if shape=="triangle":
            print("3333333333333333333333333333333333333333333333333333333")
            triangle=1
    if triangle==1 and circle==1:
        os.system("mpg321 ask.mp3")
        with sr.Microphone() as source:
            audio = r.listen(source)
        try:
            my_stt = r.recognize_google(audio, language = "zh-TW")
            print(my_stt)
            text="打開"
            if my_stt.encode("utf8")==text:
                GPIO.output(pin2, True)
                os.system("mpg321 r1.mp3")
                missionComplete=1;
        except sr.UnknownValueError:
            print("google Speech Reconition could not understand your audio")
        except sr.RequestError as e:
            print("Could not request results from Google Speech Reconition service")
            
    if missionComplete==1:
        break
    #Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

## When everything done, release the capture
cap.release()
cv2.destroyAllWindows()    

