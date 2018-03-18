from flask import Flask
from flask_ask import Ask, statement, convert_errors
import RPi.GPIO as GPIO
import subprocess
import logging
import time


GPIO.setmode(GPIO.BCM)

app = Flask(__name__)
ask = Ask(app, '/')

logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.intent('GPIOControlIntent', mapping={'status': 'status', 'pin': 'pin'})
def gpio_control(status, pin):

    try:
        pinNum = int(pin)
    except Exception as e:
        return statement('Pin number not valid.')

    GPIO.setup(pinNum, GPIO.OUT)

    if status in ['on', 'high']:    GPIO.output(pinNum, GPIO.HIGH)
    if status in ['off', 'low']:    GPIO.output(pinNum, GPIO.LOW)

    return statement('Turning pin {} {}'.format(pin, status))

@ask.intent('LIRCPower', mapping={'power': 'power'})
def LIRCPower(power):

    if power in ['on', 'off']:
        #turn receiver on (Technics)
        #subprocess.call("irsend SEND_ONCE Panasonic_EUR644340 KEY_POWER", shell=True)
        #turn receiver on (Sony)
        #subprocess.call("irsend SEND_ONCE SONY_RM-U302 KEY_POWER", shell=True)
        #time.sleep (600.0 / 1000.0)
        subprocess.call("irsend SEND_ONCE SONY_RM-U302 KEY_INP_TVDBS", shell=True)
        #turn TV on
        subprocess.call("irsend SEND_ONCE Samsung_BN59-00678A KEY_POWER", shell=True)
        return statement('Switching power {}'.format(power))
    else:
        return statement('Unknown power status')
