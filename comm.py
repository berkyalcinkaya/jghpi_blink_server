import time
import serial

def send_command_open_comm(command, device="/dev/ttyACM0", read=False, read_wait=0.5):
    print(command)
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
        print(e)
        return f"An error occurred: {e}"
    
class SerialConnection:
    def __init__(self, device="/dev/ttyACM0", baud_rate=115200, timeout=1, verbose=False, config_commands = ["dio mode DO_G0 source",
                                                                                                            "dio mode DI_G0 source"]):
        #assert(baud_rate in [115200, 230400, 460800, 921600, 1000000])
        self.device = device
        self.baud_rate = baud_rate
        self.timeout = timeout
        self.ser = None
        self.v=verbose
        self.open_connection()
        time.sleep(0.005)
        self.send_initial_command()
        time.sleep(0.005)
        if config_commands:
            if self.v:
                print("Running configuration commands")
            for config_command in config_commands:
                self.send_command(config_command)
                time.sleep(0.005)
        self.clear_buffer()
        time.sleep(0.005)
    
    def send_initial_command(self):
        self.ser.write(b"\r\n")
    
    def clear_buffer(self):
        self.ser.read(self.ser.inWaiting())

    def open_connection(self):
        if self.ser is None:
            try:
                self.ser = serial.Serial(self.device, self.baud_rate, timeout=self.timeout)
                if self.v:
                    print(f"Serial connection opened on {self.device} at {self.baud_rate} baud.")
            except Exception as e:
                if self.v:
                    print(f"Failed to open serial connection: {e}")

    def close_connection(self):
        if self.ser is not None:
            self.ser.close()
            self.ser = None
            if self.v:
                print("Serial connection closed.")

    def send_command(self, command, byte_mode=False, read=False, read_wait=0.5):
        if self.ser is None:
            if self.v:
                print("Serial connection is not open.")
            return None

        try:
            if byte_mode:
                if self.v:
                    print(f"Sending byte command: {command}")
                self.ser.write(command)
            else:
                if self.v:
                    print(f"Sending command: {command}")
                self.ser.write((command + '\n').encode())

            if read:
                time.sleep(read_wait)
                response = self.ser.read_all().decode()
                return response
            else:
                return None
        except Exception as e:
            if self.v:
                print(f"An error occurred while sending command: {e}")
            return f"An error occurred: {e}"
 

