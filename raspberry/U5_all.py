import RPi.GPIO as GPIO
import time
from mfrc522 import SimpleMFRC522
from gpiozero import LED,MotionSensor

# GPIO setup
GPIO.setmode(GPIO.BCM)

# Pin configuration
PIR_PIN = 18
LED_BAR_PINS = [5,6,13,19,26,12,16,20,21,22]
BUZZER_PIN = 17

# Setup pins
GPIO.setup(BUZZER_PIN, GPIO.OUT)

# Motion sensor
pir = MotionSensor(PIR_PIN) 

# LEDS
leds = [LED(pin) for pin in LED_BAR_PINS]

# RFID reader
reader = SimpleMFRC522()

# Define correct RFID UID (replace with your actual UID)
CORRECT_UID = 856610833225

def play_tone(frequency, duration):
    pwm = GPIO.PWM(BUZZER_PIN, frequency)
    pwm.start(50)  # 50% duty cycle
    time.sleep(duration)
    pwm.stop()

def led_bar_on(duration=5):
    step_time = duration / len(LED_BAR_PINS)
    for led in leds:
        led.on()       # Turn on LED
        time.sleep(step_time)     # Delay for visual effect
def led_bar_off():
    for led in leds:
        led.off()


try:
    print("System ready. Waiting for motion...")
    while True:
        if pir.motion_detected:
            print("Motion detected!")
            print("Waiting for RFID card...")

            id, text = reader.read()
            led_bar_on(5)
            print(f"Card detected. UID: {id}")
            led_bar_off()

            if id == CORRECT_UID:
                print("Correct card!")
                play_tone(1000, 0.5)  # High tone
            else:
                print("Wrong card!")
                play_tone(500, 0.5)   # Low tone

            time.sleep(2)  # Cooldown before next detection
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Exiting program...")
    pass

finally:
    GPIO.cleanup()
