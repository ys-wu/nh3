import sys, os, configparser
from time import sleep
from datetime import datetime

import conf

from airrmonia import Airrmonia
from mfc import Mfc
from meassys import MeasSys

from helpers import is_new_start


config = configparser.ConfigParser()
config.read('settings.ini')
AUTO_START = True if config['SETTINGS']['AUTO_START'] == 'True' else False
AUTO_PUBLISH = True if config['SETTINGS']['AUTO_PUBLISH'] == 'True' else False
AUTO_BACKUP = True if config['SETTINGS']['AUTO_BACKUP'] == 'True' else False
LOCAL_PUBLISH_INTERVAL = int(config['SETTINGS']['LOCAL_PUBLISH_INTERVAL'])
LOCAL_RECORD_INTERVAL = int(config['SETTINGS']['LOCAL_RECORD_INTERVAL'])
REMOTE_PUBLISH_INTERVAL = int(config['SETTINGS']['REMOTE_PUBLISH_INTERVAL'])
REMOTE_BACKUP_INTERVAL = int(config['SETTINGS']['REMOTE_BACKUP_INTERVAL'])

airrmonia = Airrmonia(conf.PORT)
mfc_sample = Mfc(
  conf.MFC_SAMPLE['DAC'],
  conf.MFC_SAMPLE['ADC'],
  conf.MFC_SAMPLE['RANGE']
)
mfc_cal = Mfc(
  conf.MFC_CAL['DAC'],
  conf.MFC_CAL['ADC'],
  conf.MFC_CAL['RANGE']
)
meassys = MeasSys(airrmonia, mfc_sample, mfc_cal)

if AUTO_START:
  meassys.start()

gen_local_pub = is_new_start(LOCAL_PUBLISH_INTERVAL)
gen_local_record = is_new_start(LOCAL_RECORD_INTERVAL)
gen_remote_pub = is_new_start(REMOTE_PUBLISH_INTERVAL)
gen_remote_backup = is_new_start(REMOTE_BACKUP_INTERVAL)


def main():
  while True:
    sleep(0.01)
    dttm = datetime.utcnow()

    if next(gen_local_pub):
      data = meassys.data

      if data is None:
        print(dttm, 'No data.')
        continue

      data, status, errors = data
      print(dttm, (data, status, errors))


if __name__ == '__main__':
  try:
    main()
  except KeyboardInterrupt:
    meassys.stop()
    sleep(0.5)
    print(datetime.utcnow(), 'Interrupted')
    try:
      sys.exit(0)
    except SystemExit:
      os._exit(0)
