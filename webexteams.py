#!/usr/bin/python

import os
import time
from webexteamssdk import WebexTeamsAPI
import RPi.GPIO as GPIO

import logging
import sys

# setup three LEDs: green, red, white
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
green=4
red=18
white=25
GPIO.setup(red,GPIO.OUT)
GPIO.setup(green,GPIO.OUT)
GPIO.setup(white,GPIO.OUT)
Freq=100 #for PWM control
GREEN=GPIO.PWM(green,Freq)
RED=GPIO.PWM(red,Freq)
WHITE=GPIO.PWM(white,Freq)

# use the access token and personid from environment variables
# located in /lib/systemd/system/webexteams.service
api=WebexTeamsAPI()

mywebexid=os.environ.get('WEBEX_TEAMS_PERSONID')
api.people.get(personId=mywebexid).status

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# this is just to make the output look nice
formatter = logging.Formatter(fmt="%(asctime)s %(name)s.%(levelname)s: %(message)s", datefmt="%Y.%m.%d %H:%M:%S")

# configure log output file in webexteams.service file
handler = logging.StreamHandler(stream=sys.stdout)
handler.setFormatter(formatter)
logger.addHandler(handler)

try:
    while True:
        # Status codes include: active,inactive,DoNotDisturb,meeting,presenting,call,unknown(when disabled in privacy settings)
        status = api.people.get(personId=mywebexid).status
        if status == "active":
            #logger.info("active/green")
            GREEN.start(100)
            WHITE.stop()
            RED.stop()
            time.sleep (60)
        elif status == "call":
            #logger.info("call/red")
            GREEN.stop()
            RED.start(100)
            WHITE.stop()
            time.sleep (60)
        elif status == "inactive":
            #logger.info("inactive/white")
            GREEN.stop()
            RED.stop()
            WHITE.start(100)
            time.sleep (60)
        elif status == "OutOfOffice":
            #logger.info("ooo/all_off")
            GREEN.stop()
            RED.stop()
            WHITE.stop()
            time.sleep (360)
        elif status == "unknown":
            #logger.info("incognito/all_off")
            GREEN.stop()
            RED.stop()
            WHITE.stop()
            time.sleep (360)
        else:
            #logger.info("other/red")
            GREEN.stop()
            RED.start(100)
            WHITE.stop()
            time.sleep (60)

except KeyboardInterrupt:
    RED.stop()
    GREEN.stop()
    WHITE.stop()    
    GPIO.cleanup()
