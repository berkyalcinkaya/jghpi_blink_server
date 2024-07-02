import RPi.GPIO as GPIO

# Set up the GPIO mode
GPIO.setmode(GPIO.BOARD)  # Use BOARD pin numbering

# Define all digital output pins (DO0 to DO15) and VCC based on BOARD numbering
output_pins = {
    "VCC": 1,  # Pin 1 for 3.3V
    "DO0": 11, "DO1": 13, "DO2": 15, "DO3": 16,
    "DO4": 18, "DO5": 19, "DO6": 21, "DO7": 22,
    "DO8": 23, "DO9": 5, "DO10": 7, "DO11": 8,
    "DO12": 10, "DO13": 12, "DO14": 3, "DO15": 24
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
