# Sources: 
#     https://www.youtube.com/watch?v=l-cbSO3nhqo
#     https://stackoverflow.com/questions/4256107/running-bash-commands-in-python

import os
import subprocess
import RPi.GPIO as GPIO
import time
from timeit import default_timer as timer
from datetime import datetime

state = False

startCmd = 'wget -O- http://localhost:7999/1/detection/start'
pauseCmd = 'wget -O- http://localhost:7999/1/detection/pause'

# CHANGME Change variables depending on your situation
url = "https://discord.com/api/webhooks/<>"
camURL = "http://192.168.0.126:9081/"

startTime = timer() 
endTime = 0 
# amount of time to wait until next button detection
timeThreshold = 30
recordingTime = 30
recording = False

# Wait 30 seconds before starting to allow motioneye to initialize first
time.sleep(30)

process = subprocess.Popen(pauseCmd.split(), stdout=subprocess.DEVNULL)

def button_callback(channel):
    state = GPIO.input(channel)
   
    global recording
    global startTime
    global endTime

    # Do not detect button input if motion detection (recording) is in progress
    if not recording:
        if state == 0:
            if endTime == 0:
                #print("first pressed")
                endTime = timer() + 30
            else:
                #print("pressed")
                endTime = timer()
        
            # Start motion detection if enough time has elapsed between button presses
            if endTime - startTime >= timeThreshold:
                now = datetime.now()
                #subprocess.run(['wget', '-O-', startCmd], check=True, text=True)
                process = subprocess.Popen(startCmd.split(), stdout=subprocess.DEVNULL)
                #webhookProcess = subprocess.Popen(webhookCmd.split(), stdout=subprocess.DEVNULL)
                webhookMsg = "HEY THERE'S SOMEONE AT YOUR DOOR. GO SEE WHO '{}'".format(camURL)
                subprocess.Popen(['/home/pi/touchsensor/discordwebhook.sh', webhookMsg], stdout=subprocess.DEVNULL)

                #time.sleep(2)

                #file = '/home/pi/touchsensor/doorbellsounds/0-w7mZjDmjFew.mp3'
                #os.system("/usr/bin/ffplay -nodisp " + file)
                subprocess.Popen(['/home/pi/touchsensor/playdoorbellsound.sh'], stdout=subprocess.DEVNULL)
                #output, error = process.communicate()
                startTime = timer()
                recording = True
                #print("debug: starting recording")
    #else
    #    print("released")

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

GPIO.add_event_detect(13, GPIO.FALLING, callback=button_callback)
#message = input("press enter to quit\n\n")

# Wait for button input
while True:

    if recording:
        currTime = timer()

        # Stop recording after specified amount of recording time
        if currTime - startTime >= recordingTime:
            #subprocess.run(['wget', '-O-', pauseCmd], check=True, text=True)
            process = subprocess.Popen(pauseCmd.split(), stdout=subprocess.DEVNULL)
            #output, error = process.communicate()
            recording = False
            #print("debug: ending recording")


    time.sleep(0.25)
    # do nothing
    #pass

GPIO.cleanup()





