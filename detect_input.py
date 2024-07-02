import RPi.GPIO as GPIO
import time

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering

# Define all digital input pins (DI0 to DI15) based on BCM numbering
input_pins = {
    "DI0": 2, "DI1": 3, "DI2": 4, "DI3": 17,
    "DI4": 27, "DI5": 22, "DI6": 10, "DI7": 9,
    "DI8": 11, "DI9": 5, "DI10": 6, "DI11": 13,
    "DI12": 19, "DI13": 26, "DI14": 21, "DI15": 20
}

# Set up input pins with pull-up resistors
for pin in input_pins.values():
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to read inputs and print status
def read_inputs():
    for name, pin in input_pins.items():
        if GPIO.input(pin) == GPIO.LOW:  # Active low, meaning input is detected when the pin is LOW
            print(f"Input detected on {name} (pin {pin})")
        else:
            print(f"No input detected on {name} (pin {pin})")

try:
    while True:
        read_inputs()
        time.sleep(1)  # Adjust the delay as needed

except KeyboardInterrupt:
    # Clean up GPIO settings on exit
    GPIO.cleanup()
