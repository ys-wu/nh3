import configparser

import conf

from airrmonia import Airrmonia
from mfc import Mfc
from mesayss import meassys


config = configparser.ConfigParser()
config.read('settings.ini')
AUTO_START = True if config['SETTINGS']['AUTO_START'] == 'True' else False
AUTO_PUBLISH = True if config['SETTINGS']['AUTO_PUBLISH'] == 'True' else False
AUTO_BACKUP = True if config['SETTINGS']['AUTO_PUBLISH'] == 'True' else False
UPDATE_INTERVAL = int(config['SETTINGS']['AUTO_PUBLISH'])
RECORD_INTERVAL = int(config['SETTINGS']['AUTO_PUBLISH'])

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


