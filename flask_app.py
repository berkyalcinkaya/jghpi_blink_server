from flask import Flask, request, jsonify
import json
import threading
import RPi.GPIO as GPIO
import time
from .utils import board_is_on, triggered_remote
from .board_utils import blink_all_three_multiples

app = Flask(__name__)

@app.route('/blink', methods=['POST'])
def handle_blink():
    if board_is_on() and not triggered_remote():
        return jsonify({'error': 'Board is on from the controller. Contact site to turn board off'}), 400
    
    data = request.json
    rate = data.get('freq')
    if rate is None or not isinstance(rate, int):
        return jsonify({'error': 'Invalid input, must provide an integer rate'}), 400
    


    

    