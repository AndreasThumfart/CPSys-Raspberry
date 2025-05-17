import lgpio
import sys
import time

LED_PIN = 13 

if len(sys.argv) != 2:
    print("Usage: led_control.py on|off")
    sys.exit(1)

command = sys.argv[1].strip().lower()

# Open a connection to the GPIO chip
h = lgpio.gpiochip_open(0)

# Set the pin as output
lgpio.gpio_claim_output(h, LED_PIN, 0)

if command == "on":
    lgpio.gpio_write(h, LED_PIN, 1)
    print("LED turned ON")
elif command == "off":
    lgpio.gpio_write(h, LED_PIN, 0)
    print("LED turned OFF")
else:
    print("Invalid command. Use 'on' or 'off'.")
    lgpio.gpiochip_close(h)
    sys.exit(1)

# Keep the state and close the chip (state persists)
lgpio.gpiochip_close(h)
