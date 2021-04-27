from time import sleep

import conf

from helpers import get_utc_time


class Mfc():

  def __init__(self, name, dac, adc, flow_range, raw_range=4095, volt_range=5.0):
    self.name = name
    self.dac = dac
    self.adc = adc
    self.flow_range = flow_range
    self.raw_range = raw_range
    self.volt_range = volt_range
    self.dac.normalized_value = 1.0

  def __str__(self):
    return f'MFC: 0-{self.flow_range} L/min, 0-{self.volt_range} volts'

  def set(self, value):
    value = value if value <= self.flow_range else self.flow_range
    self.dac.raw_value = int(self.raw_range * value / self.flow_range)
    print(f'{get_utc_time()} set {self.name} to {value} L/min')
  
  @property
  def flow(self):
    return round(self.adc.voltage / self.volt_range * self.flow_range, 3)


if __name__ == '__main__':

  mfc1 = Mfc(
    conf.MFC_SAMPLE['NAME'],
    conf.MFC_SAMPLE['DAC'],
    conf.MFC_SAMPLE['ADC'],
    conf.MFC_SAMPLE['RANGE']
  )
  mfc1.set(conf.MFC_SAMPLE['FLOW'])

  mfc2 = Mfc(
    conf.MFC_CAL['NAME'],
    conf.MFC_CAL['DAC'],
    conf.MFC_CAL['ADC'],
    conf.MFC_CAL['RANGE']
  )
  mfc2.set(conf.MFC_CAL['FLOW'])

  for i in range(60):
    sleep(1)
    print('mfc1', mfc1.flow)
    print('mfc2', mfc2.flow)
