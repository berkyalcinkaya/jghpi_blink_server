'''
board_pins.py
6/19/24
Berk Yalcinkaya

Stores hardcoded pin input and output values as well as other neccessary constants
Configures Pins as input and outputs. Imported from board.py
'''
import serial
import time

def send_command(command, device="/dev/ttyACM0", read=False, read_wait=0.5):
    try:
        with serial.Serial(device, 115200, timeout=1) as ser:
            # Send the command
            ser.write((command + '\n').encode())
            if read:
                time.sleep(read_wait)  # Wait for the device to process the command
                response = ser.read_all().decode()
                return response
            else:
                return None
    except Exception as e:
        return f"An error occurred: {e}"
    
class OutPin():
    def __init__(self, pin, group = 0):
        self.pin_num = int(pin)
        self.group_num = group
        self.type = "DO"
        self.is_on = False
    
    def on(self):
        send_command(f"dio set {self.type}_G{self.group_num} {self.pin_num} active")
        self.is_on = True
    
    def off(self):
        send_command(f"dio set {self.type}_G{self.group_num} {self.pin_num} inactive")
        self.is_on = False
    
    def toggle(self):
        if self.is_on:
            self.off()
        else:
            self.on()


LED1 = OutPin(0)
LED2 = OutPin(1)
LED3 = OutPin(2)

# convenience list
leds = [LED1, LED2, LED3]