import sys
import serial
import time

def send_command(command, device):
    try:
        with serial.Serial(device, 115200, timeout=1) as ser:
            # Send the command
            ser.write((command + '\n').encode())
            time.sleep(0.5)  # Wait for the device to process the command
            # Read the response
            response = ser.read_all().decode()
            return response
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    if len(sys.argv) != 3:
        print("Usage: python send_command.py <device> <command>")
        sys.exit(1)

    device = sys.argv[1]
    command = sys.argv[2]

    response = send_command(command, device)
    print("Response from device:")
    print(response)

if __name__ == "__main__":
    main()