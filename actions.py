# -*- coding: utf-8 -*-

import json

from flask import Flask, render_template

import driver

app = Flask(__name__)


MAX_HUMIDY = 1023
IDLE = 'IDLE'
WORKING = 'WORKING'

current_status = IDLE

addr = '00:15:FF:F2:11:2B'
conn = driver.BluetoothConn(addr)
driver.logger = app.logger


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/irrigate')
def irrigate():
    with conn as sock:
        sock.send('i')

    return "true"


@app.route('/status')
def status():
    line = ''

    with conn as sock:
        while '\n' not in line:
            line = sock.recv(1024)

    line = line.split('\n')[-2].strip()

    humidity, status = line.split(',')
    humidity = int(humidity)
    current_status = IDLE if status == 'IDLE' else WORKING
    percent = humidity * 100 / MAX_HUMIDY

    response = {
        'status': current_status,
        'humidity': {'percent': percent, 'value': humidity}
    }

    return json.dumps(response)
