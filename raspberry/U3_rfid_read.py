# Manual: https://pimylifeup.com/raspberry-pi-rfid-rc522/
# RPi.GPIO is automatically installed when installing MFRC522 but its not supported on Pi5
# Uninstall RPi.GPIO and install rpi-lgpio instead

# (ue3env) admin@raspberrypi:~/Documents/sunfounder/ue3 $ pip list
# Package    Version
# ---------- -------
# lgpio      0.2.2.0
# mfrc522    0.0.7
# pip        23.0.1
# rpi-lgpio  0.6
# setuptools 66.1.1
# spidev     3.7

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        id, text = reader.read()
        print(id)
        print(text)
finally:
        GPIO.cleanup()
