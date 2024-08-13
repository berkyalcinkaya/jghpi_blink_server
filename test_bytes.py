from comm import SerialConnection

def construct_num_devices_command():
    # Construct the command header
    header = bytearray(8)
    header[0] = 0x01  # Start of frame
    header[1] = 0x00  # DIO command kind
    header[2] = 0x00  # Status (not used for sending)
    header[3] = 0x00  # Status (not used for sending)
    header[4] = 0x08  # Length of command data (1 byte for the action)
    header[5] = 0x00  # Reserved
    header[6] = 0x00  # Reserved
    header[7] = 0x00  # Reserved

    # Construct the command body
    body = bytearray(8)
    body[0] = 0x04  # Action: Num Devices
    body[1] = 0x00  # Bank (not relevant here)
    body[2] = 0x00  # Pin index (not relevant here)
    body[3] = 0x00  # State (not relevant here)
    body[4:8] = (0).to_bytes(4, byteorder='little')  # Edge count (not relevant)

    return header + body

if __name__ == "__main__":
    # Initialize the SerialConnection
    serial_conn = SerialConnection(device="/dev/ttyACM0", baud_rate=115200, timeout=1, verbose=True)
    
    # Construct the command to get the number of devices
    command = construct_num_devices_command()
    
    # Send the command and receive the response
    response = serial_conn.send_command(command, byte_mode=True, read=True)
    print(response)
    
    # # Parse the response to get the number of devices (if applicable)
    # if response and len(response) >= 8:
    #     # The response should include the status and the number of devices
    #     status = int.from_bytes(response[2:4], byteorder='little')
    #     num_devices = response[8]
    #     if status == 0x0000:  # Check if the command was successful
    #         print(f"Number of DIO banks available: {num_devices}")
    #     else:
    #         print(f"Command failed with status code: {status:#04x}")
    
    # Close the serial connection
    serial_conn.close_connection()