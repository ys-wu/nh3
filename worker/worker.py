import sys, os
from configparser import ConfigParser
from time import sleep
from datetime import datetime
import json

import redis

import conf

from airrmonia import Airrmonia
from mfc import Mfc
from meassys import MeasSys

from helpers import (
  SETTINGS,
  GENS,
  get_utc_time,
  setting_handler,
  is_auto_zero,
  status_setter,
  push_to_redis,
  command_handler,
  save_data,
)


r = redis.Redis(
  host=conf.REDIS['HOST'],
  port=conf.REDIS['PORT'],
  db=conf.REDIS['DB'],
)

airrmonia = Airrmonia(conf.PORT, r)
print(get_utc_time(), 'init Airrmonia.')
print(airrmonia)

mfc_sample = Mfc(
  conf.MFC_SAMPLE['NAME'],
  conf.MFC_SAMPLE['DAC'],
  conf.MFC_SAMPLE['ADC'],
  conf.MFC_SAMPLE['RANGE']
)
mfc_cal = Mfc(
  conf.MFC_CAL['NAME'],
  conf.MFC_CAL['DAC'],
  conf.MFC_CAL['ADC'],
  conf.MFC_CAL['RANGE']
)

meassys = MeasSys(airrmonia, mfc_sample, mfc_cal)

if SETTINGS['AUTO_START']:
  print(get_utc_time(), 'auto start')
  meassys.start()


def main():
  while True:
    sleep(0.01)
    command_handler(r, meassys)
    status_setter(meassys, r)
    setting_handler(r)

    if next(GENS['local_pub']):
      dttm = get_utc_time()
      data = meassys.data

      if data is None:
        print(dttm, 'No data.')
        continue
      
      data, status, errors = data
      data = {'dttm': dttm, 'data': data, 'status': status, 'errors': errors}
      print(dttm, data['data']['Status'], data['status'])
      
      json_data = json.dumps(data)
      push_to_redis(r, 'data', json_data)
    
      if next(GENS['local_record']):
        save_data(data)
      
      if meassys.status != 'Idle':
        if is_auto_zero():
          meassys.cal_gas_zero_start()
        else:
          meassys.cal_gas_zero_stop()


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    meassys.stop()
    sleep(0.5)
    print(' ')
    print(get_utc_time(), 'Interrupted')
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)
