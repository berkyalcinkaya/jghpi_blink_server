from board_utils import send_command
import time

def blink_pin(interval):
    """Blink the pin on and off with the given interval."""
    try:
        while True:
            send_command("dio set DO_G0 0 active")
            time.sleep(interval)
            send_command("dio set DO_G0 0 inactive")
            time.sleep(interval)
    except KeyboardInterrupt:
        print("Blinking stopped by user.")

if __name__ == "__main__":
    send_command("dio mode DO_G0 source")
    blink_interval = 1  # Blink once a second
    blink_pin(blink_interval)