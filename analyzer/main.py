import configparser
import time
from datetime import datetime

import board
import busio

import adafruit_ads1x15.ads1015 as ADS
from adafruit_ads1x15.analog_in import AnalogIn

import adafruit_mcp4725


i2c = busio.I2C(board.SCL, board.SDA)

# lood config setting
config = configparser.ConfigParser()
config.read('conf.ini')
ch1_set = float(config['SETTINGS']['ch1'])
ch2_set = float(config['SETTINGS']['ch2'])

# MFC set Channels
raw_range = 4095
ch1_dac = adafruit_mcp4725.MCP4725(i2c)
ch1_dac.normalized_value = 1.0
ch2_dac = adafruit_mcp4725.MCP4725(i2c, address=0x63)
ch2_dac.normalized_value = 1.0

# MFC read channels
ads = ADS.ADS1015(i2c)
ch1_adc = AnalogIn(ads, ADS.P1)
ch2_adc = AnalogIn(ads, ADS.P2)


while True:
  dt = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S (UTC)")
  ch1_dac.raw_value = int(raw_range * ch1_set)
  ch2_dac.raw_value = int(raw_range * ch2_set)
  ch1_read = ch1_adc.voltage / 5
  ch2_read = ch2_adc.voltage / 5
  print(f'{dt}\nChannel 1 Set: {ch1_set}, Read {ch1_read}\nChannel 2 Set: {ch2_set}, Read {ch2_read}')
  time.sleep(1)
