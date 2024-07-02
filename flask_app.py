from flask import Flask, request, jsonify
import json
import threading
import RPi.GPIO as GPIO
import time
from utils import board_is_on, triggered_remote, update_json_file, get_json_dict
from board_utils import blink_all_three_multiples, get_interval_from_freq

RUN_LIGHTS = False # keep as false to test API alone

app = Flask(__name__)

@app.route('/blink', methods=['POST'])
def handle_blink():
    if board_is_on() and not triggered_remote():
        return jsonify({'error': 'Board is on from the controller. Contact site to turn board off'}), 400
    data = request.json
    rate = data.get('freq')
    if rate is None or not isinstance(rate, int):
        return jsonify({'error': 'Invalid input, must provide an integer rate with key name "freq"'}), 400
    
    interval = get_interval_from_freq(rate)
    intrvl_lst = [interval/2, interval, interval*2]
    freq_list = [1/i for i in intrvl_lst]
    update_json_file(1, intrvl_lst, True)

    if RUN_LIGHTS:
        blink_all_three_multiples(interval)
    return jsonify(get_json_dict()), 200
    


    
    
@app.route('/')
def hello_world():
    return 'Hello, World!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

    

    