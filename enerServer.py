#!/usr/bin/env python3
from flask import Flask, render_template, redirect
import RPi.GPIO as GPIO
import time

app = Flask(__name__)

# Use these variables to name your sockets
# todo: convert to objects that store the pin output and name
socket1name = "Fan"
socket2name = "TV"
socket3name = "Speakers"
socket4name = "" # Currently unused

# set the pins numbering mode
GPIO.setmode(GPIO.BOARD)
# Select the GPIO pins used for the encoder K0-K3 data inputs
GPIO.setup(11, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)
# Select the signal used to select ASK/FSK
GPIO.setup(18, GPIO.OUT)
# Select the signal used to enable/disable the modulator
GPIO.setup(22, GPIO.OUT)
# Disable the modulator by setting CE pin lo
GPIO.output (22, False)
# Set the modulator to ASK for On Off Keying
# by setting MODSEL pin lo
GPIO.output (18, False)
# Initialise K0-K3 inputs of the encoder to 0000
GPIO.output (11, False)
GPIO.output (15, False)
GPIO.output (16, False)
GPIO.output (13, False)

@app.route('/')
def index():
    templateData = {
        'socket1name' : socket1name,
        'socket2name' : socket2name,
        'socket3name' : socket3name,
        'socket4name' : socket4name
    }
    return render_template('index.html', **templateData)

@app.route("/<deviceName>/<action>")
def action(deviceName, action):
    deviceName = deviceName.upper()
    action = action.upper()

    if deviceName == 'S1':
        GPIO.output (11, True)
        GPIO.output (15, True)
        GPIO.output (16, True)
    if deviceName == 'S2':
        GPIO.output (11, False)
        GPIO.output (15, True)
        GPIO.output (16, True)
    if deviceName == 'S3':
        GPIO.output (11, True)
        GPIO.output (15, False)
        GPIO.output (16, True)
    if deviceName == 'S4':
        GPIO.output (11, False)
        GPIO.output (15, False)
        GPIO.output (16, True)
    if deviceName == 'ALL':
        GPIO.output (11, True)
        GPIO.output (15, True)
        GPIO.output (16, False)

    if action == "ON":
        GPIO.output (13, True)
    if action == "OFF":
        GPIO.output (13, False)

    # let it settle, encoder requires this
    time.sleep(0.3)
    # Enable the modulator
    GPIO.output (22, True)
    # keep enabled for a period
    time.sleep(0.5)
    # Disable the modulator
    GPIO.output (22, False)

    templateData = {
    }

    return redirect ("/", code=302)
if __name__ == '__main__':
    app.run(debug=True, port=80, host='0.0.0.0')
