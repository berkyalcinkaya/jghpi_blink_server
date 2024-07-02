import RPi.GPIO as GPIO

# Set up the GPIO mode
GPIO.setmode(GPIO.BCM)  # Use BCM pin numbering

# Define all digital output pins (DO0 to DO15) based on BCM numbering
output_pins = {
    "DO0": 17, "DO1": 27, "DO2": 22, "DO3": 23,
    "DO4": 24, "DO5": 10, "DO6": 9, "DO7": 25,
    "DO8": 11, "DO9": 5, "DO10": 6, "DO11": 13,
    "DO12": 19, "DO13": 26, "DO14": 21, "DO15": 20
}

# Set up output pins
for pin in output_pins.values():
    GPIO.setup(pin, GPIO.OUT)

# Function to power output pins
def power_outputs():
    for name, pin in output_pins.items():
        GPIO.output(pin, GPIO.HIGH)
        print(f"Power supplied to {name} (pin {pin})")

try:
    power_outputs()
    # Keep the script running to maintain the output state
    while True:
        pass

except KeyboardInterrupt:
    # Clean up GPIO settings on exit
    GPIO.cleanup()
