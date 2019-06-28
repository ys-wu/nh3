import numpy as np
import pandas as pd
import os, glob, re
import datetime, time
import serial


COMMANDS = {'Status': '?',
            'Mode': 'M',
            'Satart': 'E',
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


def init_port(port, baudrate=19200, timeout=0.1):
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
    columns = ['Status', 'airflow', 'Detector1', 'Detector2', 'conductivity']
    pattern = 'Y;\d{5}.\d{5};\d{2};\d{1};\d{2};[a-zA-Z0-9]{4};\d{4};\d{3};\d{5};\d{5};\d{5};\d{5};\d{5}'
    for s in str_arr:
        if s[0] == COMMANDS['Data'] and re.fullmatch(pattern, s): 
            x = s.split(';')
    if 'x' in locals():
        data = [x[6], int(x[7])/100, int(x[8])/10, int(x[9])/10, int(x[10])/10]
        return dict(zip(columns, data))
    else:
        return None


def form_command(command, param=None, method='get'):
    if method == 'get':
        s = CHARS['Esc'] + COMMANDS[command]
    elif method == 'set':
        s = CHARS['STX'] + COMMANDS[command] + param + CHARS['CR']
    return s.encode('utf-8')


def get_data(ser):
    r = ser.read(10000)
    if r:
        return parse_data(r)
    else:
        return None


def send_command(ser, command, param=None, method='get'):
    ser.write(form_command(command, param, method))
    return get_data(ser)


def get_datetime(interval=10):
    t0 = int(datetime.datetime.now().timestamp()/interval)
    while int(datetime.datetime.now().timestamp()/interval) == t0:
        time.sleep(0.01)
    return datetime.datetime.now()
             

def cal_func(res, std=[0, 50, 500]):
    z = np.polyfit(x=res, y=std, deg=2)
    return np.poly1d(z)


if __name__ == '__main__':
    res = [0, 381.6, 1381.5] # 2018.06 cal

    ports = get_ports()
    print(ports)
    port = test_port(ports)
    print(port)
    ser = init_port(port)
    print(ser)
    f = cal_func(res)

    for i in range(10):
	    date_time = get_datetime(1)
	    data = get_data(ser)
	    if data:
	        NH4 = f(data['conductivity']) # ppb(aq)
	        try:
	            NH3 = NH4*26/data['airflow'] # ppt(g)
	        except ZeroDivisionError:
	            NH3 = 0
	        data['date_time'] = date_time
	        data['NH4'] = NH4
	        data['NH3'] = NH3
	        print(i, end='\t')
	        print(data['date_time'], end='\t')
	        print(data['conductivity'])