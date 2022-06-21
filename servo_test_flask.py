from flask import Flask,render_template,request
from datetime import datetime
import RPi.GPIO as GPIO
import os
import time
from time import sleep
import keyboard

feedHour1=0
feedHour2=0
feedMinute1=0
feedMinute2=0


# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# Set pin 11 as an output, and set servo1 as pin 11 as PWM
GPIO.setup(11,GPIO.OUT)
servo1 = GPIO.PWM(11,50) # Note 11 is pin, 50 = 50Hz pulse

#start PWM running, but with value of 0 (pulse off)
servo1.start(0)

x=0
feedSecond1=0
feedSecond2=10
app=Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/feed",methods=["POST"])
def feeder():
    if request.method=='POST':
        feedHour1=int(request.form.get('feedHour1'))
        feedMinute1=int(request.form.get('feedMinute1'))
        feedHour2=int(request.form.get('feedHour2'))
        feedMinute2=int(request.form.get('feedMinute2'))
    def SetAngle(angle):
            duty=angle/18+2
            GPIO.output(11,True)
            servo1.ChangeDutyCycle(duty)
            sleep(1)
            GPIO.output(11,False)
            servo1.ChangeDutyCycle(0)
            print(angle)
    x=0
    while True:
        def feedFish(x):
            currentHour=time.strftime("%H")
            currentMinute=time.strftime("%M")
            currentSecond=time.strftime("%S")
            if((int(currentHour)==feedHour1)and(int(currentMinute)==feedMinute1)and(int(currentSecond)==feedSecond1)or
            (int(currentHour)==feedHour2)and(int(currentMinute)==feedMinute2)and(int(currentSecond)==feedSecond2)
            ):
                x=x+45
                SetAngle(x)
                if(x==180):
                    SetAngle(0)
            return x
        x=feedFish(x)
        if keyboard.is_pressed('q'):
            SetAngle(0)
            GPIO.cleanup()
            os._exit(0)
#    while(True):
if __name__=="__main__":
    app.run(debug=True)
