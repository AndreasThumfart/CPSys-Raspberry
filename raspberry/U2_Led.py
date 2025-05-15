# U2: LED MIT PYTHON STEUERN
#!/usr/bin/env python3
from gpiozero import LED
from time import sleep

# Initialize LED connected to GPIO pin 17
led = LED(17)
try:
    # Start an infinite loop to toggle the LED state.
    while True:
        # Turn on the LED
        led.on()
        print('...LED ON')
        # Wait for 0.5 seconds with
        sleep(0.5)
        # Turn off the LED
        led.off()
        print('LED OFF...')
        # Wait for 0.5 seconds
        sleep(0.5)
except KeyboardInterrupt:
    # handle a keyboard interrupt (Ctrl+C) by breaking the loop.
    pass
