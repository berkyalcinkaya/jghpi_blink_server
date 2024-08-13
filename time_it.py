import time
from comm import SerialConnection
from board_utils import OutPin  # Adjust based on your project structure

def measure_round_trip_time(serial_connection, led_pin, byte_mode=False):
    mode = "Byte Mode" if byte_mode else "Regular Mode"
    print(f"Measuring round-trip time in {mode}...")

    # Measure the round-trip time for turning the LED on
    start_time = time.time()
    led_pin.on()
    end_time = time.time()
    round_trip_time_on = end_time - start_time
    print(f"Round-trip time for turning LED ON in {mode}: {round_trip_time_on:.6f} seconds")
    
    # Measure the round-trip time for turning the LED off
    start_time = time.time()
    led_pin.off()
    end_time = time.time()
    round_trip_time_off = end_time - start_time
    print(f"Round-trip time for turning LED OFF in {mode}: {round_trip_time_off:.6f} seconds")

    return round_trip_time_on, round_trip_time_off

if __name__ == "__main__":
    # Initialize the SerialConnection
    serial_conn = SerialConnection(device="/dev/ttyACM0", baud_rate=115200, timeout=1, verbose=True)
    
    # Initialize an LED pin (example pin number 0) in regular mode
    led_pin_regular = OutPin(pin=0, serial_connection=serial_conn, group=0, v=True, byte_mode=False)
    
    # Measure round-trip times in regular mode
    measure_round_trip_time(serial_connection=serial_conn, led_pin=led_pin_regular, byte_mode=False)
    time.sleep(1)

    # Initialize an LED pin (example pin number 0) in byte mode
    led_pin_byte = OutPin(pin=0, serial_connection=serial_conn, group=0, v=True, byte_mode=True)
    time.sleep(1)
    
    # Measure round-trip times in byte mode
    measure_round_trip_time(serial_connection=serial_conn, led_pin=led_pin_byte, byte_mode=True)
    time.sleep(1)

    # Close the serial connection when done
    serial_conn.close_connection()
