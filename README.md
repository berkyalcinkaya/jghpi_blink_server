# Raspberry Pi LED Blinking API Documentation

## Overview

This API allows users to test the frame rate of their camera by blinking three LEDs at different frequencies. The server runs on a Raspberry Pi and can be accessed at the static IP: **http://10.2.44.165:5000**. The LEDs blink at intervals that correspond to the camera's frame rate (FPS). By observing the LEDs, users can verify if their camera is recording at, above, or below the intended frame rate.

## Purpose

The primary purpose of this setup is to help users verify the actual frame rate (frames per second) of a camera by recording LEDs blinking at known frequencies. The camera is tested by comparing the captured LED blink pattern with the expected blink frequencies. The server allows users to:

1. **Blink three LEDs simultaneously** at different frequencies derived from the specified frame rate.
2. **Control the LEDs** to turn them on, off, or run in test mode via API endpoints.
3. **Debug the system** by retrieving the current status of the board.

## API Endpoints

### 1. `/blink` - Start the LED blinking based on the provided frame rate (FPS)

**Description**: This endpoint allows you to specify a camera frame rate. The server will then blink the three LEDs at frequencies that are derived from the specified FPS.

- **Method**: `POST`
- **Request Body**:
    - `rate`: (float) The frame rate in FPS that you want to test.
  
- **Response**:
    - Returns a JSON object containing the test details, including the blink frequencies and periods in seconds and microseconds.

- **Example Request (curl)**:
```bash
curl -X POST http://10.2.44.165:5000/blink \
    -H "Content-Type: application/json" \
    -d '{"rate": 240}'
```

- **Example Request (Python)**:
```python
import requests

url = 'http://10.2.44.165:5000/blink'
payload = {'rate': 240}
headers = {'Content-Type': 'application/json'}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
```

- **Response Example**:
```json
{
    "message": "Testing Frame Rate: 240 fps | Blink Frequencies (Hz) Top to Bottom: 240.0, 120.0, 60.0 | Blink Periods (s): 0.004166666666666667, 0.008333333333333333, 0.016666666666666666 | Blink Periods (us): 4166, 8333, 16666",
    "freqs": [240.0, 120.0, 60.0],
    "status": "LEDs blinking"
}
```

### 2. `/off` - Turn off all LEDs

**Description**: This endpoint stops the LED blinking and turns off all LEDs. It also resets the board's status.

- **Method**: `GET`

- **Example Request (curl)**:
```bash
curl http://10.2.44.165:5000/off
```

- **Example Request (Python)**:
```python
import requests

url = 'http://10.2.44.165:5000/off'
response = requests.get(url)
print(response.text)
```

- **Response Example**:
```json
"Board Turned Off Successfully"
```

### 3. `/debug` - Retrieve current board status

**Description**: This endpoint returns the current status of the board, including the LED frequencies and whether the LEDs are currently blinking.

- **Method**: `GET`

- **Example Request (curl)**:
```bash
curl http://10.2.44.165:5000/debug
```

- **Example Request (Python)**:
```python
import requests

url = 'http://10.2.44.165:5000/debug'
response = requests.get(url)
print(response.json())
```

- **Response Example**:
```json
{
    "freqs": [240.0, 120.0, 60.0],
    "status": "LEDs blinking",
    "message": "Testing Frame Rate: 240 fps"
}
```

## How it Works

1. **LED Frequencies**: The LED frequencies are derived from the camera frame rate (FPS) you provide. For instance, if you test at 240 FPS, the LEDs blink as follows:
    - **Top LED**: Blinks at 240 Hz (fastest).
    - **Middle LED**: Blinks at 120 Hz (target FPS/2).
    - **Bottom LED**: Blinks at 60 Hz (slowest).

2. **Frame Rate Testing**: By observing the blinking LEDs, users can analyze their camera footage and determine if the camera is capturing at the expected rate:
    - If the middle LED's pattern matches the footage, the camera is capturing at the desired rate.
    - If the camera records the bottom LED blinking faster than expected, it may be underperforming.
    - If the top LED appears slower, the camera may be exceeding the target frame rate.

## System Configuration

- **LED Setup**: The board controls four LEDs, but only three (LED1, LED2, LED3) are used for blinking at multiple frequencies. The fourth LED (LED4) is turned on when improper requests are submitted.
- **PWM Configuration**: Pulse-width modulation (PWM) is used to control the blink intervals.
- **Minimum Rate**: The system does not accept frame rates below 50 FPS.

## Error Handling

- If an invalid `rate` is provided, the system will return an error response. The blue light will turn on in this case.
- If the board is already turned on by the controller, the system will override the settings and proceed with the test but issue a warning.

## Notes

- If making calls from outside the network *legacy*, the user will need to be on the VPN network. 
- Make sure the Raspberry Pi is connected to the network and the static IP **10.2.44.165** is accessible.
- For any hardware issues or troubleshooting, ensure that the board is properly powered and the LEDs are connected correctly.

## Development

The code is designed to be extensible. You can modify the LED blinking logic, add more LEDs, or adjust the frequency calculations based on your testing requirements.

### Development Instructions:
**Accessing the device**: plug in a monitor to the HDMI port on the Raspberry Pi and plug in a keyboard to any usb port on the device. You will need to unplug the device from power and plug it back in to establish an HDMI signal. After doing this, the device should boot-up and after a few seconds, the log-in screen should be displayed on the monitor. Log in with the following credentials:

**username**: ubuntu<br>
**password**: jghpi2024

The code for the server and input detection is located in the directory `/blink`. Here, you can fetch the latest changes using `git pull`. Upon pulling updates, you willl need to restart the server and board script. 

First, run ```python3 flask_app.py&```. To run the server and push it to the background (as signified by the `&` char). Press `Enter` and then run ```python3 board.py``` to start the main board script.

You can unplug the monitor and keyboard, and resume normal usage. 


