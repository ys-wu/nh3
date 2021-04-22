import sys, os, configparser
from time import sleep
from datetime import datetime
import json

import redis

import conf

from airrmonia import Airrmonia
from mfc import Mfc
from meassys import MeasSys

from helpers import (
  get_utc_time,
  is_new_start,
  status_setter,
  push_to_redis,
  command_handler
)


config = configparser.ConfigParser()
config.read('settings.ini')
AUTO_START = True if config['SETTINGS']['AUTO_START'] == 'True' else False
AUTO_PUBLISH = True if config['SETTINGS']['AUTO_PUBLISH'] == 'True' else False
AUTO_BACKUP = True if config['SETTINGS']['AUTO_BACKUP'] == 'True' else False
LOCAL_PUBLISH_INTERVAL = int(config['SETTINGS']['LOCAL_PUBLISH_INTERVAL'])
LOCAL_RECORD_INTERVAL = int(config['SETTINGS']['LOCAL_RECORD_INTERVAL'])
REMOTE_PUBLISH_INTERVAL = int(config['SETTINGS']['REMOTE_PUBLISH_INTERVAL'])
REMOTE_BACKUP_INTERVAL = int(config['SETTINGS']['REMOTE_BACKUP_INTERVAL'])

r = redis.Redis(
  host=conf.REDIS['HOST'],
  port=conf.REDIS['PORT'],
  db=conf.REDIS['DB'],
)

airrmonia = Airrmonia(conf.PORT)
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

if AUTO_START:
  print(get_utc_time(), 'auto start')
  meassys.start()

gen_local_pub = is_new_start(LOCAL_PUBLISH_INTERVAL)
gen_local_record = is_new_start(LOCAL_RECORD_INTERVAL)
gen_remote_pub = is_new_start(REMOTE_PUBLISH_INTERVAL)
gen_remote_backup = is_new_start(REMOTE_BACKUP_INTERVAL)


def main():
  while True:
    sleep(0.01)
    command_handler(r, meassys)
    status_setter(meassys, r)

    if next(gen_local_pub):
      dttm = get_utc_time()
      data = meassys.data

      if data is None:
        print(dttm, 'No data.')
        continue
      
      data, status, errors = data
      data = {'dttm': dttm, 'data': data, 'status': status, 'errors': errors}
      print(dttm, data['data']['Status'], data['status'])
      
      data = json.dumps(data)
      push_to_redis(r, 'data', data)


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
