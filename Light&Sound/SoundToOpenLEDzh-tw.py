from gtts import gTTS
import os
import speech_recognition as sr
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) #BOARD or BCM
pin2 = 2
GPIO.setup(pin2, GPIO.OUT)
pin3 = 3 
GPIO.setup(pin3, GPIO.OUT)
pin4 = 4
GPIO.setup(pin4, GPIO.OUT)

GPIO.output(pin2, False)
GPIO.output(pin3, False)
GPIO.output(pin4, False)

r = sr.Recognizer()
r.energy_threshold =  4000    # threshold for filtering noise
GPIO.output(pin2, False)
GPIO.output(pin3, False)
GPIO.output(pin433, False)
while True:
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        my_stt = r.recognize_google(audio, language = "zh-TW")
        print(my_stt)
        if my_stt =="打開紅色燈":
            GPIO.output(pin2, True)
            os.system("mpg321 r1.mp3")
        elif my_stt =="關閉紅色燈":
            GPIO.output(pin2, False)
            os.system("mpg321 r2.mp3")
        elif my_stt =="打開黃色燈":
            GPIO.output(pin3, True)
            os.system("mpg321 y1.mp3")
        elif my_stt =="關閉黃色燈":
            GPIO.output(pin3, False)
            os.system("mpg321 y2.mp3")
        elif my_stt =="打開� 色燈":
            GPIO.output(pin4, True)
            os.system("mpg321 g1.mp3")
        elif my_stt =="關閉� 色燈":
            GPIO.output(pin4, False)
            os.system("mpg321 g2.mp3")
    except sr.UnknownValueError:
        print("google Speech Reconition could not understand your audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Reconition service")
