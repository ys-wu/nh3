import numpy as np
import pandas as pd
import os, glob, re
import datetime, time
import serial
import threading
import copy

import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["NH3"]
col = db["raw_data"]

from flask import Flask, render_template, jsonify, request
app = Flask(__name__)


CAL = {0: 0, 50: 381.6, 500: 1381.5} # 2018.06 calibration
COEF = 26 # liquid NH4+ (ppbm) to gas NH3 (pptv)
INTERVAL = 1 # samnpling time invteval


COMMANDS = {'Status': '?',
            'Mode': 'M',
            'Start': 'E',
            'Stop': 'S',
            'Error': '!',
            'Mem': 'C',
            'Reset': 'R',
            'Data': 'Y',
            'AirPump': 'A',
            'LiqPump': 'Q',
            'Valve': 'V',
            'Fan': 'F'}
    
CHARS = {'STX': '\x02',
         'LF': '\x0a',
         'CR': '\x0d',
         'Esc':'\x1b'}


STATUS_bits = {'AirPump': 0,
          'LiqPump': 1,
          'Fan': 2,
          'Heater': 3,
          'AutoStart': 4,
          'ErrorFlag': 5,
          'Bottle': 6,
          'DataMemory': 7,
          'CalMemory': 8}


def get_ports():
    return glob.glob('/dev/ttyUSB*')


def test_port(ports, baudrate=19200, timeout=0.1):
    for p in ports:
        ser = serial.Serial(p)
        ser.baudrate = 19200
        ser.timeout = 0.1
        time.sleep(2)
        while True:
            s = ser.read(1000)
            if s:
                break
        if s:
            while True: 
                s = ser.read(1000)
                if s:
                    return p


def init_port(port, baudrate=19200, timeout=0.5):
    ser = serial.Serial(port)
    ser.baudrate = baudrate
    ser.timeout = timeout
    return ser


def parse_data(string):
    if isinstance(string, bytes):
        try:
            string = string.decode('utf-8')
        except UnicodeDecodeError:
            return None
    sep = CHARS['CR'] + CHARS['LF']
    str_arr = string.split(sep)
    str_arr = str_arr[0:-1] # delete last element (empty or incomplete)
    print(str_arr)
    columns = ['Status', 'temperature', 'airflow', 'Detector1', 'Detector2', 'conductivity']
    pattern = 'Y;\d{5}.\d{5};\d{2};\d{1};\d{2};[a-zA-Z0-9]{4};\d{4};\d{3};\d{5};\d{5};.\d{4};.\d{4};.\d{4}'
    for s in str_arr:
        if s and s[0] == COMMANDS['Data'] and re.fullmatch(pattern, s): 
            x = s.split(';')
    if 'x' in locals():
        data = [x[5], int(x[6])/100, int(x[7])/100, int(x[8])/10, int(x[9])/10, int(x[10])/10]
        return dict(zip(columns, data))
    else:
        return None


def form_command(command, param=None, method='get'):
    if method == 'get':
        s = CHARS['Esc'] + command
    elif method == 'set':
        s = CHARS['STX'] + command + param + CHARS['CR']
    return s.encode('utf-8')


def get_data(ser):
    r = ser.read(10000)
    print(r)
    if r:
        return parse_data(r)
    else:
        return None


def send_command(ser, command, param=None, method='get'):
    ser.write(form_command(command, param, method))
    return get_data(ser)


def get_datetime(interval=10):
    t0 = int(datetime.datetime.utcnow().timestamp()/interval)
    while int(datetime.datetime.utcnow().timestamp()/interval) == t0:
        time.sleep(0.01)
    return datetime.datetime.utcnow()
             

def cal_func(cal_params):
    x = [v for v in cal_params.values()]
    y = [k for k in cal_params.keys()]
    z = np.polyfit(x, y, deg=2)
    return np.poly1d(z)


def get_status(status_hex, bits=STATUS_bits):
    code = bin(int(status_hex, 16))[2:].zfill(9)[::-1]
    status = {}
    for key, value in bits.items():
        status[key] = int(code[value])
    return status


def update_data():
    global data
    data = {}
    # print('------------- empyt data ---------------')
    # print(data)
    while True:
        date_time = get_datetime(1)
        raw_data = get_data(ser)
        print('-------------- raw data ---------------')
        print(raw_data)
        if raw_data:
            data = raw_data
            data['date_time'] = date_time
            data['NH4'] = func(data['conductivity']) # ppb(aq)
            data['Status'] = get_status(data['Status'])
            if data['Status']['AirPump']:
                data['NH3'] = data['NH4']*COEF/data['airflow'] # ppt(g)
            else:
                data['NH3'] = 0
            x = copy.deepcopy(data)
            col.insert_one(x)


func = cal_func(CAL)
ports = get_ports()
print(ports)
time.sleep(1)
port = test_port(ports)
print(port)
time.sleep(1)
ser = init_port(port)
print(ser)
time.sleep(2)
send_command(ser, COMMANDS['Start'])
time.sleep(2)

x = threading.Thread(target=update_data)
x.start()


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/update", methods=["POST"])
def update():
    # print('------------------data ---------------')
    # print(data)
    if data:
        return jsonify({'success': True, 'data': data})
    else:
        return jsonify({'success': False})


@app.route("/command", methods=["POST"])
def get_command():
    print('************************************')
    print('************************************')
    command = request.form.get("commands")
    on_off = request.form.get("on_off")
    print(command)
    print(type(command))
    print(on_off)
    print(type(on_off))
    send_command(ser, COMMANDS[command], on_off, 'set')
    print(command, on_off)
    print('************************************')
    print('************************************')
