# -*- coding: utf-8 -*-

import json

import bluetooth
from flask import Flask, render_template

from proxy import ReverseProxied


app = Flask(__name__)
app.wsgi_app = ReverseProxied(app.wsgi_app)

MAX_HUMIDY = 1023
IDLE = 'IDLE'
WORKING = 'WORKING'

current_status = IDLE
addr = '00:15:FF:F2:11:2B'

app.sock = None


def get_sock():
    if not app.sock:
        app.sock = bluetooth.BluetoothSocket()
        app.sock.connect((addr, 1))

    return app.sock


@app.route('/')
def main():
    return render_template('main.html')


@app.route('/irrigate')
def irrigate():
    sock = get_sock()
    sock.send('i')
    #sock.close()

    response = True

    return json.dumps(response)


@app.route('/status')
def status():
    sock = get_sock()
    line = sock.recv(1024)

    while '\n' not in line:
        line = sock.recv(1024)

    line = line.split('\n')[-2].strip()
    #sock.close()

    humidity, status = line.split(',')
    humidity = int(humidity)
    current_status = IDLE if status == 'IDLE' else WORKING
    percent = humidity * 100 / MAX_HUMIDY

    response = {
        'status': current_status,
        'humidity': {'percent': percent, 'value': humidity}
    }

    return json.dumps(response)

