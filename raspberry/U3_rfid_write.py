# Manual: https://pimylifeup.com/raspberry-pi-rfid-rc522/
# RPi.GPIO is automatically installed when installing MFRC522 but its not supported on Pi5
# Uninstall RPi.GPIO and install rpi-lgpio instead

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        text = input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
finally:
        GPIO.cleanup()