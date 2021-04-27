import glob
import time

import serial
from pymongo import MongoClient

import board
import busio
import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import adafruit_mcp4725


# Redis
REDIS = {
  'HOST': 'localhost',
  'PORT': 6379,
  'DB': 0,
}

# MongoDB
mongdb = {
  'HOST': 'localhost',
  'PORT': 27017,
  'DB': 'nh3',
  'COL': 'data',
}

db = MongoClient(mongdb['HOST'], mongdb['PORT'])[mongdb['DB']]
COLLECTION = db[mongdb['COL']]


# AIRRMONIA
baudrate=19200
timeout=0.5

def get_port():
  ports = glob.glob('/dev/ttyUSB*')
  for p in ports:
    ser = serial.Serial(p)
    ser.baudrate = baudrate
    ser.timeout = timeout
    time.sleep(2)
    while ser.read(1000):
      return ser
  return None

PORT = get_port()

# CAL = {0: 0, 50: 381.6, 500: 1381.5}  # 2018.06 calibration
COEF = 26  # liquid NH4+ (ppbm) to gas NH3 (pptv)

COMMANDS = {
  'Status': '?',
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
  'Fan': 'F'
}

CHARS = {
  'STX': '\x02',
  'LF': '\x0a',
  'CR': '\x0d',
  'Esc': '\x1b'
}

STATUS_BITS = {
  'AirPump': 0,
  'LiqPump': 1,
  'Fan': 2,
  'Heater': 3,
  'AutoStart': 4,
  'ErrorFlag': 5,
  'Bottle': 6,
  'DataMemory': 7,
  'CalMemory': 8
}


# MFC
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1015(i2c)

# MFC_1 sample flow
MFC_SAMPLE = {
  'NAME': 'sample',
  'DAC': adafruit_mcp4725.MCP4725(i2c),
  'ADC': AnalogIn(ads, ADS.P1),
  'RANGE': 3.0,
  'FLOW': 1.0,
  'LOWER_LIMIT': 0.75,
  'UPPER_LIMIT': 1.25,
}

# MFC_2 zero air flow
MFC_CAL = {
  'NAME': 'cal',
  'DAC': adafruit_mcp4725.MCP4725(i2c, address=0x63),
  'ADC': AnalogIn(ads, ADS.P2),
  'RANGE': 5.0,
  'FLOW': 2.0,
  'LOWER_LIMIT': 1.5,
  'UPPER_LIMIT': 2.5,
}
